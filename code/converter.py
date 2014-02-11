#!/usr/bin/env python3

from bs4 import BeautifulSoup, SoupStrainer
from copy import deepcopy
from raw_data_parsers.parse_game_info import convert_time, convert_weather, convert_duration, convert_overunder, convert_vegas_line, convert_stadium


class Converter:

    def __init__(self, file_name):
        """Given the file name of a raw data file, opens it and converts it to
        JSON.

        args:
            file_name: A string containing the name of a file to open
        """
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

        # Parse the various tables
        self.__parse_officials()
        self.__parse_game_info()

    def __init_json(self):
        """ Initialize the dictionary for the output JSON. """
        self.json = {
                "home team": None,
                "away team": None,
                "venue": None,
                "datetime": None,
                "weather": None,
                "betting": None,
                "officials": None,
                "team stats": {},
                "plays": []
                }
        self.json["venue"] = {
                "stadium": None,
                "dome": None,
                "surface": None,
                "attendance": None
                }
        self.json["datetime"] = {
                "date": None,
                "start time": None,
                "duration": None
                }
        self.json["betting"] = {
                "winner": None,
                "speard": None,
                "over under": None
                }
        teamstats = {
                "first downs" : None,
                "rush" : {
                    "plays" : None,
                    "yards" : None,
                    "touchdowns" : None,
                    },
                "pass" : {
                    "plays": None,
                    "yards" : None,
                    "touchdowns" : None,
                    "successful" : None,
                    "interceptions" : None
                    },
                "sacks" : {
                    "plays" : None,
                    "yards" : None
                    },
                "fumbles" : {
                    "plays" : None,
                    "lost" : None
                    },
                "penalties" : {
                    "plays" : None,
                    "yards" : None
                    }
                }
        # We use deep copy so that we can uniquely set values in each, instead
        # of having them linked.
        self.json["team stats"]["home"] = deepcopy(teamstats)
        self.json["team stats"]["away"] = deepcopy(teamstats)

    def __set_strainers(self):
        """ Set up a list of hard coded SoupStrainers. """
        self.strainers = {}
        self.strainers["game_info"] = SoupStrainer(id="game_info")
        self.strainers["ref_info"] = SoupStrainer(id="ref_info")
        self.strainers["team_stats"] = SoupStrainer(id="team_stats")
        self.strainers["pbp_data"] = SoupStrainer(id="pbp_data")
        # Starters needs work; there is no easy tag to grab
        #self.strainers["starters"] = SoupStrainer(name="starters")

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
        pass

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
                    self.json["betting"]["winner"] = team_code
                    self.json["betting"]["speard"] = line
                elif tmp_key == "Over/Under":
                    self.json["betting"]["over under"] = convert_overunder(tmp_value)

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


if __name__ == '__main__':
    # We only need to parse commandline flags if running as the main script
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('file', type=str, nargs="+",
            help="a raw data file to convert to JSON")
    args = argparser.parse_args()

    for raw_file in args.file:
        converter = Converter(raw_file)
        print(converter)
