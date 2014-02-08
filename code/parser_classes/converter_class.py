#!/usr/bin/env python3

from bs4 import BeautifulSoup, SoupStrainer


class Converter:

    def __init__(self, file_name):
        """Given the file name of a raw data file, opens it and converts it to
        JSON.

        args:
            file_name: A string containing the name of a file to open
        """
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

    def __set_strainers(self):
        """ Set up a list of hard coded SoupStrainers. """
        self.strainers = {}
        self.strainers["game_info"] = SoupStrainer(id="game_info")
        self.strainers["ref_info"] = SoupStrainer(id="ref_info")
        self.strainers["team_stats"] = SoupStrainer(id="team_stats")
        self.strainers["pbp_data"] = SoupStrainer(id="pbp_data")
        # Starters needs work; there is no easy tag to grab
        #self.strainers["starters"] = SoupStrainer(name="starters")

    def print_soups(self):
        """ Print out all the soups. """
        for key in self.soups:
            print("=====", key, "=====")
            print(self.soups[key].prettify())

if __name__ == '__main__':
    # We only need to parse commandline flags if running as the main script
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('file', type=str, nargs="+",
            help="a raw data file to convert to JSON")
    args = argparser.parse_args()

    for raw_file in args.file:
        converter = Converter(raw_file)
        converter.print_soups()
