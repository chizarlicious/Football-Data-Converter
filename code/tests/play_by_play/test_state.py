#!/usr/bin/env python3

import unittest

from raw_data_parsers.play_by_play.state import convert_int, convert_quarter, convert_game_clock, convert_field_position


class TestPlayByPlay(unittest.TestCase):

    def test_convert_int(self):
        # Successful
        self.assertEqual(convert_int("-9"), -9)
        self.assertEqual(convert_int("9"), 9)
        self.assertEqual(convert_int(''), None)
        # Failure
        self.assertRaises(ValueError, convert_int, "a")
        self.assertRaises(ValueError, convert_int, "nine")
        self.assertRaises(ValueError, convert_int, " ")

    def test_convert_quarter(self):
        # Successful
        self.assertEqual(convert_quarter("1"), 1)
        self.assertEqual(convert_quarter("2"), 2)
        self.assertEqual(convert_quarter("3"), 3)
        self.assertEqual(convert_quarter("4"), 4)
        self.assertEqual(convert_quarter("OT"), 5)
        # Failure
        self.assertRaises(ValueError, convert_quarter, "0")
        self.assertRaises(ValueError, convert_quarter, "5")
        self.assertRaises(ValueError, convert_quarter, "Five")

    def test_convert_game_clock(self):
        # Successful
        self.assertEqual(convert_game_clock("15:00", 1), 0)
        self.assertEqual(convert_game_clock("15:00", 2), 900)
        self.assertEqual(convert_game_clock("15:00", 5), 3600)
        self.assertEqual(convert_game_clock("0:24", 3), 2676)
        # Failure
        self.assertRaises(ValueError, convert_game_clock, "16:00", 1)
        self.assertRaises(ValueError, convert_game_clock, "14:61", 1)
        self.assertRaises(ValueError, convert_game_clock, "15:01", 1)
        self.assertRaises(ValueError, convert_game_clock, "-10:35", 1)
        self.assertRaises(ValueError, convert_game_clock, "-00:35", 1)
        self.assertRaises(ValueError, convert_game_clock, "00:35", 0)

    def test_convert_field_position(self):
        # Successful
        self.assertEqual(convert_field_position("DEN 35", "DEN"), 65)
        self.assertEqual(convert_field_position("MIN 35", "DEN"), 35)
        self.assertEqual(convert_field_position("50", "DEN"), 50)
        self.assertEqual(convert_field_position("", "DEN"), None)
        self.assertEqual(convert_field_position("MIN 35", ""), None)
        # Failure
        self.assertRaises(ValueError, convert_field_position, "DEN 51", "DEN")
        self.assertRaises(ValueError, convert_field_position, "DEN Inches", "DEN")
        self.assertRaises(ValueError, convert_field_position, "DEN 34", "FRN")
        self.assertRaises(KeyError, convert_field_position, "FRN 34", "DEN")


if __name__ == '__main__':
    unittest.main()
