#!/usr/bin/env python3

import unittest
from raw_data_parsers.parse_play_by_play import convert_game_clock, convert_field_position
from errors.parsing_errors import GameClockError, FieldPositionError, TeamCodeError


class TestPlayByPlay(unittest.TestCase):

    def test_convert_game_clock(self):
        # Successful
        self.assertEqual(convert_game_clock("15:00", 1), 0)
        self.assertEqual(convert_game_clock("15:00", 2), 900)
        self.assertEqual(convert_game_clock("15:00", 5), 3600)
        self.assertEqual(convert_game_clock("0:24", 3), 2676)
        # Failure returns None
        self.assertRaises(GameClockError, convert_game_clock, "16:00", 1)
        self.assertRaises(GameClockError, convert_game_clock, "14:61", 1)
        self.assertRaises(GameClockError, convert_game_clock, "15:01", 1)
        self.assertRaises(GameClockError, convert_game_clock, "-10:35", 1)
        self.assertRaises(GameClockError, convert_game_clock, "-00:35", 1)
        self.assertRaises(GameClockError, convert_game_clock, "00:35", 0)

    def test_convert_field_position(self):
        # Successful
        self.assertEqual(convert_field_position("DEN 35", "DEN"), 65)
        self.assertEqual(convert_field_position("MIN 35", "DEN"), 35)
        # Failure returns None
        self.assertRaises(FieldPositionError, convert_field_position, "DEN 51", "DEN")
        self.assertRaises(FieldPositionError, convert_field_position, "DEN Inches", "DEN")
        self.assertRaises(TeamCodeError, convert_field_position, "DEN 34", "FRN")
        self.assertRaises(TeamCodeError, convert_field_position, "FRN 34", "DEN")

if __name__ == '__main__':
    unittest.main()
