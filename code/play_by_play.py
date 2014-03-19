#!/usr/bin/env python3

import json
from copy import deepcopy
from bs4 import BeautifulSoup, SoupStrainer

from raw_data_parsers.play_by_play.general import row_type, get_kicking_team
from raw_data_parsers.play_by_play.penalty import split_penalties, get_penalty_team, get_penalty_player, get_penalty_yards, get_penalty_type, get_penalty_name
from raw_data_parsers.play_by_play.play import get_play_type, get_scoring_type
from raw_data_parsers.play_by_play.state import convert_int, convert_quarter, convert_game_clock, convert_field_position
from raw_data_parsers.play_by_play.turnover import split_turnovers, get_turnover_type, get_turnover_recoverer, get_turnover_committer, get_turnover_teams
from raw_data_parsers.play_by_play.sanitizer import remove_challenge


class PlayByPlay:

    def __init__(self, soup, season, home_team, away_team, home_players, away_players):
        """Given a BeautifulSoup, parses the play-by-play data.

        args:
            file_name: A string containing the name of a file to open
        """
        # Save input variables
        self.soup = soup
        self.season = int(season)
        self.home = home_team
        self.away = away_team
        self.home_players = frozenset(home_players)
        self.away_players = frozenset(away_players)
        # Initialize the list to convert to JSON
        self.json = []
        self.last_play_info = {
                "time": 0,
                "quarter": 1,
                "offense": None,
                "home score": 0,
                "away score": 0,
                "description": '',
                "type": None
                }
        self.current_play_info = {
                "time": 0,
                "quarter": 1,
                "offense": None,
                "home score": 0,
                "away score": 0,
                "description": '',
                "type": None
                }
        self.is_pchange = False
        self.is_scoring = False
        self.is_penalty = False

        # Some years consider the possessing team on a kick off to be the
        # kicking team; this means that they set the "pos_change" flag in the
        # opposite manner as compared to all other years.
        self.kick_offense_years = {1999, 2013}

        # Parse the plays
        self.__parse_play()

    def __parse_play(self):
        """ Set up the team stats dictionaries and add it to self.json """
        soup = self.soup
        # Find each row of the table
        rows = soup.find_all("tr")
        for row in rows:
            # Deal with the different row types
            r_type = row_type(row.get_text(' ', strip=True))
            # When setting the quarter, we need a special case to handle
            # overtimes after the first
            if r_type == 5 and self.last_play_info["quarter"] >= 5:
                self.current_play_info["quarter"] = self.last_play_info["quarter"] + 1
            # Skip all other special rows
            if r_type != 0:  # 0 indicates a normal row
                self.last_play_info = deepcopy(self.current_play_info)
                continue

            # Set the play class, which is used to indicate scores, turnovers,
            # and penalties
            self.__set_class(row)

            # Find each column of the table
            cols = row.find_all("td")
            if cols:  # This if removes the header
                pbp_dict = {}

                # Extract the plain text description and store it, because it
                # is used so often
                description = cols[5].get_text(' ', strip=True).replace('\n', ' ')
                # Sanitize replay challenges that they only the final result is used
                sanitized_description = remove_challenge(description)
                self.current_play_info["description"] = sanitized_description

                # Assign offense
                # We correct the 1999, 2013 kick offs when setting is_pchange
                if self.is_pchange:
                    # For change of possession, we change the team with the
                    # ball
                    if self.last_play_info["offense"] == "home":
                        self.current_play_info["offense"] = "away"
                    else:
                        self.current_play_info["offense"] = "home"
                else:
                    self.current_play_info["offense"] = self.last_play_info["offense"]

                # Set current score
                pbp_dict["score"] = self.__set_score(cols)

                # Check the type of play
                pbp_dict["play"] = self.__set_play(cols)

                # Sometimes there are blank plays
                if pbp_dict["play"]["type"] is None:
                    self.last_play_info = deepcopy(self.current_play_info)
                    continue

                # On a kickoff, we make sure we have the team right
                if pbp_dict["play"]["type"] in {"kick off", "onside kick"}:
                    kick_text = cols[4].get_text(' ', strip=True).replace('\n', ' ')
                    kick_team = get_kicking_team(kick_text)
                    if kick_team == self.home:
                        self.current_play_info["offense"] = "away"
                    elif kick_team == self.away:
                        self.current_play_info["offense"] = "home"
                    else:  # Assume the last team with the ball is kicking
                        flipped_team = self.__flip(self.last_play_info["offense"])
                        self.current_play_info["offense"] = flipped_team

                # Set penalty
                if self.is_penalty:
                    pbp_dict["penalty"] = self.__set_penalty()

                # Parse state
                pbp_dict["number"] = int(cols[5].a["name"].split('_')[1]) - 1
                pbp_dict["state"] = self.__set_state(cols)
                turnovers = self.__set_turnover()
                if turnovers:
                    pbp_dict["turnovers"] = turnovers
                self.json.append(pbp_dict)

                # Set last play info to current play info
                self.last_play_info = deepcopy(self.current_play_info)
                #print(json.dumps(pbp_dict, sort_keys=True, indent=2, separators=(',', ': ')))

    def __set_class(self, row):
        """ Takes a BS4 row and extracts the class, using it to set internal
        variables.

        returns:
            Nothing, but sets self.is_scoring, self.is_penalty,
            self.is_pchange.
        """
        row_class = row["class"]
        self.is_scoring = ("is_scoring" in row_class)
        self.is_penalty = ("has_penalty" in row_class)
        # In some years the raw data considers the kicking team as the offense;
        # we correct for that here.
        if self.season in self.kick_offense_years \
        and self.last_play_info["type"] in {"kick off", "onside kick"}:
            # The 'not' is required because if a kick off results in a turn
            # over, the "pos_change" flag isn't set, as the kicking team still
            # has the ball (and was considered the offense).
            self.is_pchange = not ("pos_change" in row_class)
        else:
            self.is_pchange = ("pos_change" in row_class)

    def __set_state(self, cols):
        """ Takes a list of columns from an HTML table and sets the "state"
        dictionary for the play.

        returns:
            A state dictionary with the following fields:
                {"offense": "home", "down": 2, "yards to first down": 10,
                "yards to goal": 36, "time": 398}
        """
        state = {}

        # Down
        down = convert_int(cols[2].get_text(strip=True))
        if down is not None:
            state["down"] = down

        # Quarter (Used to set the time, also set in the __parse_play())
        if self.current_play_info["quarter"] < 5:
            quarter = convert_quarter(cols[0].get_text(strip=True))
            self.current_play_info["quarter"] = quarter
        else:
            quarter = self.current_play_info["quarter"]

        # Time
        time_string = cols[1].get_text(strip=True)
        time = convert_game_clock(time_string, quarter)
        if time is not None:
            self.current_play_info["time"] = time
        else:
            time = self.last_play_info["time"]
        state["time"] = time

        # Yards to go
        ytfd = convert_int(cols[3].get_text(strip=True))
        if ytfd is not None:
            state["yards to first down"] = ytfd

        # Offense
        state["offense"] = self.current_play_info["offense"]

        # Yards to goal
        offense = state["offense"]
        if offense == "home":
            team_code = self.home
        else:
            team_code = self.away
        ytg = convert_field_position(cols[4].get_text(strip=True), team_code)
        if ytg is not None:
            state["yards to goal"] = ytg

        return state

    def __set_score(self, cols):
        """ Takes a list of columns from an HTML table and sets the "score"
        dictionary for the play.

        returns:
            A score dictionary with the following fields:
                { "home": 7, "away": 14 }
        """
        score = {}
        score["away"] = int(cols[6].get_text(strip=True))
        self.current_play_info["away score"] = score["away"]
        score["home"] = int(cols[7].get_text(strip=True))
        self.current_play_info["home score"] = score["home"]

        return score

    def __set_play(self, cols):
        """ Takes a list of columns from an HTML table and sets the "play"
        dictionary for the play.

        args:
            cols: BS4 columns.

        returns:
            A score dictionary with the following fields:
                "play": { "type": "complete pass", "scoring":
                { "type": "touchdown", "team": "home" } }
        """
        play = {}

        # Set the type
        play["type"] = get_play_type(self.current_play_info["description"])
        self.current_play_info["type"] = play["type"]

        if not self.is_scoring:
            return play
        else:
            play["scoring"] = {}
            play["scoring"]["type"] = get_scoring_type(self.current_play_info["description"])

            # Assign team based on how the score changed
            home_scored = self.current_play_info["home score"] - self.last_play_info["home score"]
            if home_scored:
                play["scoring"]["team"] = "home"

            away_scored = self.current_play_info["away score"] - self.last_play_info["away score"]
            if away_scored:
                play["scoring"]["team"] = "away"

            return play

    def __set_turnover(self):
        """ Takes the description of a play from self with a turnover in it and
        sets the "turnover" dictionary for the play.

        returns:
            A turnover list with the following fields:
                "turnovers": [{ "type": "fumble", "by": "home", "recovered":
                "away" }, ...]
        """
        turnovers = []
        turnover = {}

        for turn_string in split_turnovers(self.current_play_info["description"]):
            t = deepcopy(turnover)
            # Set the name of the penalty
            t["type"] = get_turnover_type(turn_string)
            # Set the teams
            (com, rec) = get_turnover_teams(
                    turn_string,
                    self.home_players,
                    self.away_players
                    )
            if com:
                t["by"] = com
            if rec:
                t["recovered"] = rec

            # Fill in the full dictionary
            turnovers.append(t)

        return turnovers

    def __set_penalty(self):
        """ Takes the description of a play from self with a penalty in it and
        sets the "penalty" dictionary for the play.

        returns:
            A penalty dictionary with the following fields:
                "penalty": { "type": "Illegal Use of Hands",
                "on": "home", "player": "Terrence Cody", "yards": -5,
                "no play": True }
        """
        penalties = {
                "penalties": []
                }
        #TODO: What do we do when there are multiple penalties?
        # I think we can get the team the penalty was on by looking at the down
        # marker for the previous play and the current play. However, this
        # doesn't work if we have multiple penalties.
        no_play = False
        for pen_string in split_penalties(self.current_play_info["description"]):
            p = {}
            # Set the name of the penalty
            p["name"] = get_penalty_name(pen_string)
            # Set the yardage
            yards = get_penalty_yards(pen_string)
            if yards:
                p["yards"] = yards
            # Set the offending player
            p["offender"] = get_penalty_player(
                    pen_string,
                    self.home,
                    self.away
                    )
            # Set the team. On kick offs the NFL defines the offense as the
            # kicking team, but we define it as the defense
            if self.current_play_info["type"] in {"kick off", "onside kick"}:
                off_team = self.__flip(self.current_play_info["offense"])
            else:
                off_team = self.current_play_info["offense"]
            p["team"] = get_penalty_team(
                    pen_string,
                    off_team,
                    self.home,
                    self.away,
                    self.home_players,
                    self.away_players
                    )
            # Get type info
            p_type = get_penalty_type(pen_string)
            if p_type == "declined":
                p["accepted"] = False
            else:
                p["accepted"] = True
                if p_type == "no play":
                    no_play = True

            # Fill in the full dictionary
            penalties["penalties"].append(p)

        penalties["no play"] = no_play

        return penalties

    def __flip(self, team):
        """ Flip home to away, and vice versa. """
        if team == "home":
            return "away"
        elif team == "away":
            return "home"
        else:
            return None

    def __repr__(self):
        """ Method that returns a representation of the contents. """
        return json.dumps(self.json, sort_keys=True, indent=2, separators=(',', ': '))

    def __str__(self):
        """ Method that returns a string of the contents for printing. """
        return json.dumps(self.json, sort_keys=True, indent=2, separators=(',', ': '))
