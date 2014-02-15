#!/usr/bin/env python3

import unittest
from raw_data_parsers.parse_team_stats import split_on_dashes, convert_rush_info, convert_pass_info, convert_sack_info, convert_fumble_info, convert_penalty_info


class TestTeamStats(unittest.TestCase):

    def test_split_on_dashes(self):
        # Successful
        self.assertEqual(
                split_on_dashes("1-2--3--4--5-6"),
                ("1", "2", "-3", "-4", "-5", "6")
                )
        self.assertEqual(split_on_dashes("-1--2"), ("-1", "-2"))
        self.assertEqual(split_on_dashes("1"), ("1",))
        self.assertEqual(split_on_dashes("-1"), ("-1",))
        self.assertEqual(split_on_dashes("-A"), ("-A",))
        self.assertEqual(split_on_dashes("-"), ())
        self.assertEqual(split_on_dashes("--"), ())

    def test_convert_rush_info(self):
        # Successful
        self.assertEqual(convert_rush_info("16-34-0"),
                {"plays": 16, "yards": 34, "touchdowns": 0}
                )
        self.assertEqual(convert_rush_info("16--34-0"),
                {"plays": 16, "yards": -34, "touchdowns": 0}
                )
        # Failure raises ValueError
        self.assertRaises(ValueError, convert_rush_info, "16-34 0")
        self.assertRaises(ValueError, convert_rush_info, "14-5-C")

    def test_convert_pass_info(self):
        # Successful
        self.assertEqual(convert_pass_info("18-34-331-3-0"),
                {"plays": 34, "yards": 331, "touchdowns": 3,
                "interceptions": 0, "successful": 18}
                )
        self.assertEqual(convert_pass_info("18-34--331-3-0"),
                {"plays": 34, "yards": -331, "touchdowns": 3,
                "interceptions": 0, "successful": 18}
                )
        # Failure raises ValueError
        self.assertRaises(ValueError, convert_pass_info, "18 34-331-3-0")
        self.assertRaises(ValueError, convert_pass_info, "2-1-1-1-E")

    def test_convert_sack_info(self):
        # Successful
        self.assertEqual(convert_sack_info("1-7"), {"plays": 1, "yards": -7})
        # Failure raises ValueError
        self.assertRaises(ValueError, convert_sack_info, "18 34")
        self.assertRaises(ValueError, convert_sack_info, "2-A")
        self.assertRaises(ValueError, convert_sack_info, "A-2")

    def test_convert_fumble_info(self):
        # Successful
        self.assertEqual(convert_fumble_info("2-1"), {"plays": 2, "lost": 1})
        # Failure raises ValueError
        self.assertRaises(ValueError, convert_fumble_info, "2 1")
        self.assertRaises(ValueError, convert_fumble_info, "2-A")
        self.assertRaises(ValueError, convert_fumble_info, "A-2")

    def test_convert_penalty_info(self):
        # Successful
        self.assertEqual(convert_penalty_info("8-56"),
                {"plays": 8, "yards": -56}
                )
        # Failure raises ValueError
        self.assertRaises(ValueError, convert_penalty_info, "2 1")
        self.assertRaises(ValueError, convert_penalty_info, "2-A")
        self.assertRaises(ValueError, convert_penalty_info, "A-2")

if __name__ == '__main__':
    unittest.main()
