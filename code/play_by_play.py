#!/usr/bin/env python3

import json
from copy import deepcopy
from bs4 import BeautifulSoup, SoupStrainer

from raw_data_parsers.parse_play_by_play.state import convert_int, convert_quarter, convert_game_clock, convert_field_position
from raw_data_parsers.parse_play_by_play.play import get_play_type, get_scoring_type
from raw_data_parsers.parse_play_by_play.general import row_type, get_kicking_team


class PlayByPlay:

    def __init__(self, soup, home_team, away_team, home_players, away_players):
        """Given a BeautifulSoup, parses the play-by-play data.

        args:
            file_name: A string containing the name of a file to open
        """
        # Save input variables
        self.soup = soup
        self.home_players = frozenset(home_players)
        self.away_players = frozenset(away_players)
        # Initialize the dictionary to convert to JSON
        self.json = []  # Used to store plays
        self.last_play_info = {
                "time": 0,
                "quarter": 1,
                "offense": None,
                "home score": 0,
                "away score": 0
                }
        self.current_play_info = {
                "time": 0,
                "quarter": 1,
                "offense": None,
                "home score": 0,
                "away score": 0
                }
        self.game_info = {
                "home": home_team,
                "away": away_team
                }
        self.is_pchange = False
        self.is_scoring = False
        self.is_penalty = False

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

                # Assign offense
                if self.is_pchange:
                    # For change of possession, we change the team with the
                    # ball
                    if self.last_play_info["offense"] == "home":
                        self.current_play_info["offense"] = "away"
                    else:
                        self.current_play_info["offense"] = "home"
                    #pbp_dict["turnover"] = self.__set_turnover()
                else:
                    self.current_play_info["offense"] = self.last_play_info["offense"]
                if self.is_scoring:
                    pass
                if self.is_penalty:
                    pass
                    #pbp_dict["penalty"] = self.__set_penalty(cols)

                # Set current score
                pbp_dict["score"] = self.__set_score(cols)

                # Check the type of play
                pbp_dict["play"] = self.__set_play(cols)
                # On a kickoff, we make sure we have the team right
                if pbp_dict["play"]["type"] == "kick off":
                    kick_team = get_kicking_team(cols)
                    if kick_team == self.game_info["home"]:
                        self.current_play_info["offense"] = "home"
                    else:
                        self.current_play_info["offense"] = "away"

                # Parse state
                pbp_dict["number"] = int(cols[5].a["name"].split('_')[1]) - 1
                pbp_dict["state"] = self.__set_state(cols)
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
        state["down"] = convert_int(cols[2].get_text(strip=True))

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
        state["yards to first down"] = convert_int(cols[3].get_text(strip=True))

        # Offense
        state["offense"] = self.current_play_info["offense"]

        # Yards to goal
        team_code = self.game_info[state["offense"]]
        state["yards to goal"] = convert_field_position(cols[4].get_text(strip=True), team_code)

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
        play["type"] = get_play_type(cols[5].get_text(' ', strip=True))

        if not self.is_scoring:
            return play
        else:
            play["scoring"] = {}
            play["scoring"]["type"] = get_scoring_type(cols)

            # Assign team based on how the score changed
            home_scored = self.current_play_info["home score"] - self.last_play_info["home score"]
            if home_scored:
                play["scoring"]["team"] = "home"

            away_scored = self.current_play_info["away score"] - self.last_play_info["away score"]
            if away_scored:
                play["scoring"]["team"] = "away"

            return play

    def __set_turnover(self, cols):
        """ Takes a list of columns from an HTML table and sets the "turnover"
        dictionary for the play.

        returns:
            A turnover dictionary with the following fields:
                "turnover": { "type": "fumble", "recovered by": "home" }
        """
        # TODO: How do we handle multiple tunrovers?
        pass

    def __set_penalty(self, cols):
        """ Takes a list of columns from an HTML table and sets the "penalty"
        dictionary for the play.

        returns:
            A penalty dictionary with the following fields:
                "penalty": { "type": "Illegal Use of Hands",
                "on": "home", "player": "Terrence Cody", "yards": -5,
                "no play": True }
        """
        #TODO: What do we do when there are multiple penalties?
        # I think we can get the team the penalty was on by looking at the down
        # marker for the previous play and the current play. However, this
        # doesn't work if we have multiple penalties.
        pass

    def __repr__(self):
        """ Method that returns a representation of the contents. """
        return json.dumps(self.json, sort_keys=True, indent=2, separators=(',', ': '))

    def __str__(self):
        """ Method that returns a string of the contents for printing. """
        return json.dumps(self.json, sort_keys=True, indent=2, separators=(',', ': '))
