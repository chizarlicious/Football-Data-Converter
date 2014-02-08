#!/usr/bin/env python3

from bs4 import BeautifulSoup, SoupStrainer


class Converter:

    def __init__(self, file_name):
        """Given the file name of a raw data file, opens it and converts it to
        JSON.

        args:
            file_name: A string containing the name of a file to open
        """
        # Initialize the dictionary to convert to JSON
        self.__init_json_dict()

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

    def __init_json_dict(self):
        """ Initialize the dictionary for the output JSON. """
        self.json_dict = {
                "home team": None,
                "away team": None,
                "venue": None,
                "datetime": None,
                "weather": None,
                "betting": None,
                "officials": None,
                "team stats": None,
                "plays": []
                }

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
        """ Set up the officials dictionary and add it to self.json_dict """
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

        # Insert the finished dictionary into the json_dict
        self.json_dict["officials"] = ref_dict

    def print_soups(self):
        """ Print out all the soups. """
        for key in self.soups:
            print("=====", key, "=====")
            print(self.soups[key].prettify())

    def __repr__(self):
        """ Method that returns a representation of the contents. """
        return self.json_dict.__repr__()

    def __str__(self):
        """ Method that returns a string of the contents for printing. """
        return self.json_dict.__str__()


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
