#!/usr/bin/env python3

import unittest
from raw_data_parsers.parse_game_info import convert_time, convert_weather, convert_duration, convert_overunder, convert_vegas_line, convert_stadium


class TestGameInfo(unittest.TestCase):

    def test_convert_time(self):
        # Successful
        self.assertEqual(convert_time("09:32am"), "09:32")
        self.assertEqual(convert_time("1:59pm"), "13:59")
        # Failure raises a ValueError
        self.assertRaises(ValueError, convert_time, "The time is one o'clock.")
        self.assertRaises(ValueError, convert_time, "13:40pm")
        self.assertRaises(ValueError, convert_time, "11:65pm")

    def test_convert_duration(self):
        # Successful
        self.assertEqual(convert_duration("4:11"), 15060)
        self.assertEqual(convert_duration("00:11"), 660)
        self.assertEqual(convert_duration("13:11"), 47460)
        # Failure raises a ValueError
        self.assertRaises(ValueError, convert_duration, "The game lasted 2 hours.")
        self.assertRaises(ValueError, convert_duration, "13:40pm")
        self.assertRaises(ValueError, convert_duration, "11:65")

    def test_convert_weather(self):
        # Successful
        self.assertEqual(
                convert_weather("13 degrees, relative humidity 62%, wind 8 mph"),
                {"temperature": 13, "relative humidity": 0.62, "wind speed": 8, "wind chill": None}
                )
        self.assertEqual(
                convert_weather("35 degrees, relative humidity 59%, wind 10 mph, wind chill 27"),
                {"temperature": 35, "relative humidity": 0.59, "wind speed": 10, "wind chill": 27}
                )
        self.assertEqual(
                convert_weather("72 degrees, no wind"),
                {"temperature": 72, "relative humidity": None, "wind speed": 0, "wind chill": None}
                )
        self.assertEqual(
                convert_weather("28 degrees, wind 1 mph"),
                {"temperature": 28, "relative humidity": None, "wind speed": 1, "wind chill": None}
                )
        # Failure returns dictionary full of None, or a ValueError
        self.assertEqual(convert_weather("I have no idea what degree to get!"), None)
        self.assertRaises(ValueError, convert_weather, "twenty-eight degrees, wind five mph")

    def test_convert_overunder(self):
        # Successful
        self.assertEqual(convert_overunder("44.5(over)"), 44.5)
        self.assertEqual(convert_overunder("0 (under)"), 0.)
        self.assertEqual(convert_overunder("32 (under)"), 32.)
        self.assertEqual(convert_overunder("32"), 32.)
        self.assertEqual(convert_overunder("35 under"), 35.)
        # Failure raises a ValueError
        self.assertRaises(ValueError, convert_overunder, "five (under)")
        self.assertRaises(ValueError, convert_overunder, "under 70")

    def test_convert_vegas_line(self):
        # Successful
        self.assertEqual(convert_vegas_line("Arizona Cardinals -9.0"), ("ARI", -9))
        self.assertEqual(convert_vegas_line("New York Giants -19.5"), ("NYG", -19.5))
        # Failure raises various errors
        self.assertRaises(IndexError, convert_vegas_line, "Minnesota Vikings 10.5")
        self.assertRaises(IndexError, convert_vegas_line, "San Diego Chargers +4.5")
        self.assertRaises(ValueError, convert_vegas_line, "San Diego Chargers -four")
        self.assertRaises(KeyError, convert_vegas_line, "Pallet Town Charizards -10.")

    def test_convert_stadium(self):
        # Successful
        self.assertEqual(
                convert_stadium("Hubert H. Humphrey Metrodome (dome)"),
                ("Hubert H. Humphrey Metrodome", True)
                )
        self.assertEqual(
                convert_stadium("Candlestick Park"),
                ("Candlestick Park", False)
                )
        # Failure raises various errors
        self.assertRaises(TypeError, convert_stadium, 123)
        self.assertRaises(ValueError, convert_stadium, "")
        self.assertRaises(ValueError, convert_stadium, "(dome)")

if __name__ == '__main__':
    unittest.main()
