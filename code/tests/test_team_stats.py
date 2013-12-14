#!/usr/bin/env python3

import unittest
from raw_data_parsers.parse_team_stats import convert_rush_info, convert_pass_info, convert_sack_info, convert_fumble_info, convert_penalty_info


class TestTeamStats(unittest.TestCase):

    def test_convert_rush_info(self):
        # Successful
        self.assertEqual(convert_rush_info("16-34-0"),
                {"plays": 16, "yards": 34, "touchdowns": 0})
        # Failure returns None
        self.assertEqual(convert_rush_info("16-34 0"), None)
        self.assertEqual(convert_rush_info("14-5-C"), None)

    def test_convert_pass_info(self):
        # Successful
        self.assertEqual(convert_pass_info("18-34-331-3-0"),
                {"plays": 34, "yards": 331, "touchdowns": 3,
                "interceptions": 0, "successful": 18})
        # Failure returns None
        self.assertEqual(convert_pass_info("18 34-331-3-0"), None)
        self.assertEqual(convert_pass_info("2-1-1-1-E"), None)

    def test_convert_sack_info(self):
        # Successful
        self.assertEqual(convert_sack_info("1-7"), {"plays": 1, "yards": -7})
        # Failure returns None
        self.assertEqual(convert_sack_info("18 34"), None)
        self.assertEqual(convert_sack_info("2-A"), None)
        self.assertEqual(convert_sack_info("A-2"), None)

    def test_convert_fumble_info(self):
        # Successful
        self.assertEqual(convert_fumble_info("2-1"), {"plays": 2, "lost": 1})
        # Failure returns None
        self.assertEqual(convert_fumble_info("2 1"), None)
        self.assertEqual(convert_fumble_info("A-1"), None)
        self.assertEqual(convert_fumble_info("2-A"), None)

    def test_convert_penalty_info(self):
        # Successful
        self.assertEqual(convert_penalty_info("8-56"), {"plays": 8, "yards": -56})
        # Failure returns None
        self.assertEqual(convert_fumble_info("8 56"), None)
        self.assertEqual(convert_fumble_info("A-56"), None)
        self.assertEqual(convert_fumble_info("8-A"), None)

if __name__ == '__main__':
    unittest.main()
