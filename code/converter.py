#!/usr/bin/env python3

import json
from bs4 import BeautifulSoup, SoupStrainer
from copy import deepcopy
from os import getcwd, chdir, devnull, makedirs
from os.path import dirname, realpath, normpath
from subprocess import check_output, CalledProcessError

from raw_data_parsers.game_info import convert_time, convert_weather, convert_duration, convert_overunder, convert_vegas_line, convert_stadium
from raw_data_parsers.team_stats import convert_rush_info, convert_pass_info, convert_sack_info, convert_fumble_info, convert_penalty_info
from raw_data_parsers.title_info import convert_title_teams, convert_title_date, get_season, get_output_date

from data_helpers.rosters import rosters
from data_helpers.team_list import names_to_code, team_names

from play_by_play import PlayByPlay


class Converter:

    def __init__(self, file_name):
        """Given the file name of a raw data file, opens it and converts it to
        JSON.

        args:
            file_name: A string containing the name of a file to open
        """
        # Set up some internal variables
        self.home_team = None
        self.away_team = None
        self.home_players = set([])
        self.away_players = set([])
        self.season = None
        self.output_date = None

        # Initialize the dictionary to convert to JSON
        self.__init_json()

        # Set up Strainers
        self.__set_strainers()

        # Open the file and load the soup
        self.file_name = file_name
        self.soups = {}
        with open(self.file_name) as file_handle:
            cont = file_handle.read()

        # Make the Soups
        for key, value in self.strainers.items():
            self.soups[key] = BeautifulSoup(cont, parse_only=value)

        # Save the version of the parser code used to create the data file
        self.__set_version()

        # Parse the various tables
        self.__parse_title()
        self.__parse_officials()
        self.__parse_game_info()
        self.__parse_team_stats()

        # Parse all players onto teams, the starter list isn't enough
        self.__add_rosters()
        self.__parse_starter()
        self.__get_all_players()

        # Parse Play-by-play
        self.pbp = PlayByPlay(
                self.soups["pbp_data"],
                self.season,
                self.home_team,
                self.away_team,
                self.home_players,
                self.away_players
                )
        self.json["plays"] = self.pbp.json

    def __init_json(self):
        """ Initialize the dictionary for the output JSON. """
        self.json = {
                "team stats": {},
                "plays": []
                }
        self.json["venue"] = {}
        self.json["datetime"] = {}
        self.json["betting"] = {}
        self.json["players"] = {
                "home": {},
                "away": {}
                }
        self.json["_version"] = {}
        teamstats = {
                "rush": {},
                "pass": {},
                "sacks": {},
                "fumbles": {},
                "penalties": {}
                }
        # We use deep copy so that we can uniquely set values in each, instead
        # of having them linked.
        self.json["team stats"]["home"] = deepcopy(teamstats)
        self.json["team stats"]["away"] = deepcopy(teamstats)

    def __set_strainers(self):
        """ Set up a list of hard coded SoupStrainers. """
        self.strainers = {}
        self.strainers["title"] = SoupStrainer("title")
        self.strainers["game_info"] = SoupStrainer(id="game_info")
        self.strainers["ref_info"] = SoupStrainer(id="ref_info")
        self.strainers["team_stats"] = SoupStrainer(id="team_stats")
        self.strainers["pbp_data"] = SoupStrainer(id="pbp_data")
        self.strainers["starters"] = SoupStrainer("table", id="")
        self.strainers["def_stats"] = SoupStrainer("table", id="def_stats")
        self.strainers["off_stats"] = SoupStrainer("table", id="skill_stats")
        self.strainers["kick_stats"] = SoupStrainer("table", id="kick_stats")
        self.strainers["all_tables"] = SoupStrainer("table")

    def __set_version(self):
        """ Sets the valuse of the  _version tag with the hashes from the
        various git repos. """
        self.json["_version"]["parser"] = self.__get_parser_version()
        self.json["_version"]["raw"] = self.__get_raw_data_version()

    def __get_raw_data_version(self):
        """ Returns a string indicating the latest git commit from the raw
        data's git repository. """
        # Try to get the raw data version
        raw_dir = dirname(realpath(self.file_name))
        current_dir = getcwd()

        # Try to change dir
        try:
            chdir(raw_dir)
        except OSError:
            raw_version = "unknown"
        else:
            # Now that we're in the raw directory, look for git
            try:
                with open(devnull, "w") as fnull:
                    raw_version = check_output(['git', 'rev-parse', 'HEAD'], stderr=fnull)
            except CalledProcessError:
                raw_version = "unknown"
            else:
                # Having succeeded, we now clean up the output and save it
                raw_version = raw_version.decode("utf-8").strip()
            finally:
                # Always change back to the starting dir!
                chdir(current_dir)

        return raw_version

    def __get_parser_version(self):
        """ Returns a string indicating the latest git commit from the parser's
        git repository. """
        # Try to get the parser version
        try:
            with open(devnull, "w") as fnull:
                parser_version = check_output(
                        ['git', 'rev-parse', 'HEAD'],
                        stderr=fnull
                        )
        except CalledProcessError:
            parser_version = "unknown"
        else:
            # Having succeeded, we now clean up the output and save it
            parser_version = parser_version.decode("utf-8").strip()

        return parser_version

    def __parse_title(self):
        """ Parse the title tag from the HTML. This sets the two teams and the
        date."""
        soup = self.soups["title"]
        text = soup.find("title").get_text(strip=True)
        teams = text.split('-')[0]
        fulldate = text.split('-')[1]
        # Parse teams to codes
        (home, away) = convert_title_teams(teams)
        self.json["home team"] = home
        self.home_team = home
        self.json["away team"] = away
        self.away_team = away
        # Parse time
        self.json["datetime"]["date"] = convert_title_date(fulldate)
        self.season = get_season(fulldate)
        self.output_date = get_output_date(fulldate)

    def __parse_officials(self):
        """ Set up the officials dictionary and add it to self.json """
        ref_dict = {}
        soup = self.soups["ref_info"]
        # Find each row of the table
        rows = soup.find_all("tr")
        for row in rows:
            # Find each column of the table
            cols = row.find_all("td")
            if cols:  # This if removes the header
                # Extract the position and name of the referee
                tmp_pos = cols[0].get_text(strip=True)
                tmp_name = cols[1].get_text(strip=True)
                # Lowercase the position, and remove newlines in the name
                pos = tmp_pos.lower()
                name = tmp_name.replace('\n', ' ')
                # Insert into our dictionary
                ref_dict[pos] = name

        # Insert the finished dictionary into the json
        self.json["officials"] = ref_dict

    def __parse_team_stats(self):
        """ Set up the team stats dictionaries and add it to self.json """
        soup = self.soups["team_stats"]
        # Find each row of the table
        rows = soup.find_all("tr")
        home_dict = self.json["team stats"]["home"]
        away_dict = self.json["team stats"]["away"]
        for row in rows:
            # Find each column of the table
            cols = row.find_all("td")
            if cols:  # This if removes the header
                # Extract the key and both the home and away team values
                key = cols[0].get_text(strip=True)
                tmp_away = cols[1].get_text(strip=True)
                tmp_home = cols[2].get_text(strip=True)
                if key == "First downs":
                    away_dict["first downs"] = int(tmp_away)
                    home_dict["first downs"] = int(tmp_home)
                elif key == "Rush-yards-TDs":
                    away_dict["rush"] = convert_rush_info(tmp_away)
                    home_dict["rush"] = convert_rush_info(tmp_home)
                elif key == "Comp-Att-Yd-TD-INT":
                    away_dict["pass"] = convert_pass_info(tmp_away)
                    home_dict["pass"] = convert_pass_info(tmp_home)
                elif key == "Sacked-yards":
                    away_dict["sacks"] = convert_sack_info(tmp_away)
                    home_dict["sacks"] = convert_sack_info(tmp_home)
                elif key == "Fumbles-lost":
                    away_dict["fumbles"] = convert_fumble_info(tmp_away)
                    home_dict["fumbles"] = convert_fumble_info(tmp_home)
                elif key == "Penalties-yards":
                    away_dict["penalties"] = convert_penalty_info(tmp_away)
                    home_dict["penalties"] = convert_penalty_info(tmp_home)

    def __parse_game_info(self):
        """ Set up the game info dictionary and add it to self.json """
        soup = self.soups["game_info"]
        # Find each row of the table
        rows = soup.find_all("tr")
        for row in rows:
            # Find each column of the table
            cols = row.find_all("td")
            if cols:  # This if removes the header
                # Extract the key and value
                tmp_key = cols[0].get_text(strip=True)
                tmp_value = cols[1].get_text(strip=True)
                if tmp_key == "Stadium":
                    (stad, dome) = convert_stadium(tmp_value)
                    self.json["venue"]["stadium"] = stad
                    self.json["venue"]["dome"] = dome
                elif tmp_key == "Start Time":
                    self.json["datetime"]["start time"] = convert_time(tmp_value)
                elif tmp_key == "Surface":
                    self.json["venue"]["surface"] = tmp_value
                elif tmp_key == "Duration":
                    self.json["datetime"]["duration"] = convert_duration(tmp_value)
                elif tmp_key == "Attendance":
                    # We need to replace commas for int to work
                    self.json["venue"]["attendance"] = int(tmp_value.replace(',', ''))
                elif tmp_key == "Weather":
                    self.json["weather"] = convert_weather(tmp_value)
                elif tmp_key == "Vegas Line":
                    (team_code, line) = convert_vegas_line(tmp_value)
                    self.json["betting"]["spread"] = line
                    if team_code == self.home_team:
                        self.json["betting"]["winner"] = "home"
                    elif team_code == self.away_team:
                        self.json["betting"]["winner"] = "away"
                    else:  # We use None when no team is favored
                        self.json["betting"]["winner"] = None
                elif tmp_key == "Over/Under":
                    self.json["betting"]["over under"] = convert_overunder(tmp_value)

    def __parse_starter(self):
        """ Parse the list of starter and their positions. """
        soup = self.soups["starters"]
        # We get all the elements the match data-stat="pos", which is the table
        # element that has the words "Pos", which is unique to these tables.
        # Once we have these elements, we find their parents to get the whole
        # table.
        ths = soup.find_all("th", attrs={"data-stat": "pos"})
        for th in ths:
            table = th.parent.parent  # th.parent == row, row.parent == table
            for row in table.find_all("tr"):
                # We read through the rows in order. Since the header with the
                # name always comes before the players for a team, we can set
                # the dictionary at the first time we hit it and it will be
                # good for the rest of the table.

                # Header row with team name
                if "stat_total" in row["class"]:
                    team_name = row.get_text(' ', strip=True)
                    team_code = names_to_code[team_name]
                    # Set the working dictionary based on the team
                    if team_code == self.home_team:
                        p_dict = self.json["players"]["home"]
                        p_set = self.home_players
                    else:
                        p_dict = self.json["players"]["away"]
                        p_set = self.away_players
                # Normal rows have blank classes
                elif row["class"] == ['']:
                    cols = row.find_all("td")
                    player = cols[0].get_text(' ', strip=True).replace('\n', ' ')
                    position = cols[1].get_text(' ', strip=True).replace('\n', ' ')
                    # We try to add the player to the list, but if the list
                    # doesn't exist, we have to make it first
                    try:
                        p_dict[position].append(player)
                    except KeyError:
                        p_dict[position] = [player]
                    # We also add to our internal set used to get teams from
                    # players in playbyplay
                    p_set.add(player)

    def __get_all_players(self):
        """ Get all player names from the various tables and store them in the
        player sets. """
        l_soups = [self.soups["def_stats"]]
        l_soups.append(self.soups["off_stats"])
        l_soups.append(self.soups["kick_stats"])

        # Each soup is essentially the same, and we only care about the first
        # two columns
        for soup in l_soups:
            body = soup.find_all("tbody")
            for row in body[0].find_all("tr"):
                # The rows with players have blank classes
                if row["class"] == ['']:
                    cols = row.find_all("td")
                    player = cols[0].get_text(' ', strip=True).replace('\n', ' ')
                    team_code = cols[1].get_text(' ', strip=True).replace('\n', ' ')
                    # Assign by team code
                    if team_code == self.home_team:
                        self.home_players.add(player)
                    elif team_code == self.away_team:
                        self.away_players.add(player)

        # Now parse the soups from the general stats tables
        soup = self.soups["all_tables"]
        # The tables we are interested in have no id set, and have class =
        # ['stats_table', 'no_highlight'].
        team_set = None
        for table in soup.find_all("table"):
            if table.has_attr("class") and not table.has_attr("id") \
            and table["class"] == ['stats_table', 'no_highlight']:
                for metarow in table.find_all("tr"):
                    # If it is a row with a team name, use that to set the
                    # target set
                    team_name = metarow.get_text(' ', strip=True).replace('\n', ' ')
                    if team_name in team_names:
                        team_code = names_to_code[team_name]
                        if team_code == self.home_team:
                            team_set = self.home_players
                        elif team_code == self.away_team:
                            team_set = self.away_players
                        else:
                            team_set = None
                    # Otherwise we find the rows of player stats and pull out
                    # their names.
                    else:
                        for body in metarow.find_all("tbody"):
                            for row in body.find_all("tr"):
                                cols = row.find_all("td")
                                player = cols[0].get_text(' ', strip=True).replace('\n', ' ')
                                team_set.add(player)

    def __add_rosters(self):
        """Add the roster information to our player list"""
        # We add all players on the team from the pre-made list of players.
        # NOTE: Sometimes there are degenerate players, either because they
        # have the same name of one player played for both teams during the
        # season. TODO: Find an acceptable solution to this case.
        self.home_players = rosters[self.home_team][self.season].copy()
        self.away_players = rosters[self.away_team][self.season].copy()

    def print_soups(self):
        """ Print out all the soups. """
        for key in self.soups:
            print("=====", key, "=====")
            print(self.soups[key].prettify())

    def __repr__(self):
        """ Method that returns a representation of the contents. """
        return self.json.__repr__()

    def __str__(self):
        """ Method that returns a string of the contents for printing. """
        return self.json.__str__()


def json_unchanged(file_name, json_obj):
    """Takes a filename and a object that will be serialized into a json and
    tests their equality after stripping the _version hashes.

    args:
        file_name: A string containing the file to check
        json_obj: An object that will be serialized into a json

    returns:
        True if the json loaded from the file is the same as the one given to
            the function, after stripping the _version key and value. False
            otherwise.
    """
    # Try to open the target file, return false if it can't be opened for
    # reading, otherwise we continue trying to compare it
    try:
        with open(out_file_name, "r") as old_file:
            old_json = json.load(old_file)
    except IOError:
        return False
    else:
        # Deep copy to avoid mangling the input json
        new_json = deepcopy(json_obj)

        # Remove the _version key; if that is all that has changed,
        # we don't care and won't write the file
        try:
            del old_json["_version"]
        except KeyError:
            pass  # That's ok, we want to remove it anyway...
        try:
            del new_json["_version"]
        except KeyError:
            pass

        # If they are the same, don't write
        return old_json == new_json


def get_output_dir(spec_dir, season, do_not_sort=False):
    """ Returns the output directory for the file.

    args:
        spec_dir: User specified directory
        season: The season the game took place in
        do_not_sort: If true, do not make subdirectories for each season

    returns:
        A normalized directory location to save the file to. No checking is
            done to see if the directory is legal or exists.
    """
    if not do_not_sort:
        return normpath("{directory}/{season}/".format(
            directory=spec_dir, season=season
            ))
    else:
        return normpath("{directory}/".format(directory=spec_dir))


if __name__ == '__main__':
    # We only need to parse command line flags if running as the main script
    import argparse

    argparser = argparse.ArgumentParser(
            description="Convert an html file to a JSON file."
            )
    # The list of input files
    argparser.add_argument(
            "file",
            type=str,
            nargs="+",
            help="a raw data file (or files) to convert to JSON"
            )
    argparser.add_argument(
            "-o",
            "--output-directory",
            help="directory to save files to",
            default="../../data/reco/"
            )
    argparser.add_argument(
            "--do-not-sort",
            help="do not sort files into subdirectories by season",
            action="store_true"
            )
    argparser.add_argument(
            "--force-overwrite",
            help="overwrite files and update the '_version' hashes, even if nothing else has changed",
            action="store_true"
            )

    args = argparser.parse_args()

    for raw_file in args.file:
        # Try to convert the file
        try:
            converter = Converter(raw_file)
        # Continue if we fail
        except:
            continue
        # If we succeed, write it
        else:
            # Get the output directory, and try to make it
            output_dir = get_output_dir(
                    args.output_directory,
                    converter.season,
                    args.do_not_sort
                    )
            try:
                makedirs(output_dir, exist_ok=True)
            except OSError:
                err_string = "Failed to make directory '" + output_dir
                err_string += "'. Skipping file '" + raw_file + "'."
                print(err_string)
                continue
            # Now make the full file name
            tmp_out_file_name = "{output_dir}/{season}_{date}_{away}_at_{home}.json".format(
                    output_dir=output_dir,
                    season=converter.season,
                    date=converter.output_date,
                    away=converter.away_team,
                    home=converter.home_team
                )
            out_file_name = normpath(tmp_out_file_name)
            # If force_overwrite is not set, we test to make sure the file has
            # changed before writing. We do this so that it is easier to find
            # meaningful changes in git (otherwise every file changes every
            # time we make a new parser commit, even if the data is unchanged).
            if not args.force_overwrite:
                if json_unchanged(out_file_name, converter.json):
                    continue
            # Write our file
            with open(out_file_name, "w") as out_file:
                try:
                    json.dump(converter.json, out_file, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)
                except IOError:
                    err_string = "Failed to write '" + out_file_name + "'."
                    print(err_string)
                    continue
