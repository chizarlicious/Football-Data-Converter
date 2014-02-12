#!/usr/bin/env python3

import unittest
from raw_data_parsers.parse_title_info import convert_title_teams, convert_title_date


class TestGameInfo(unittest.TestCase):

    def test_convert_title_teams(self):
        # Successful
        self.assertEqual(
                convert_title_teams("St. Louis Rams at Seattle Seahawks"),
                ("SEA", "STL")
                )
        # Failure
        self.assertRaises(
                KeyError, convert_title_teams, "Rams at Seahawks"
                )
        self.assertRaises(
                IndexError, convert_title_teams,
                "St. Louis Rams @ Seattle Seahawks"
                )

    def test_convert_title_date(self):
        # Successful
        self.assertEqual(convert_title_date("January 2nd, 2012"), "2012-01-02")
        # Failure
        self.assertRaises(
                ValueError, convert_title_date, "February 45th, 2001"
                )
        self.assertRaises(
                ValueError, convert_title_date, "Notober 21nd, 2012"
                )
        self.assertRaises(
                ValueError, convert_title_date, "October 21teen, 2012"
                )

if __name__ == '__main__':
    unittest.main()
