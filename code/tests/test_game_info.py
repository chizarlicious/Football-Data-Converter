#!/usr/bin/env python3

import unittest
from raw_data_parsers.parse_game_info import convert_time, convert_weather


class TestGameInfo(unittest.TestCase):

    def test_convert_time(self):
        # Successful
        self.assertEqual(convert_time("09:32am"), "09:32")
        self.assertEqual(convert_time("1:59pm"), "13:59")
        # Failure raies a ValueError
        self.assertRaises(ValueError, convert_time, "The time is one o'clock.")
        self.assertRaises(ValueError, convert_time, "13:40pm")
        self.assertRaises(ValueError, convert_time, "11:65pm")

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
        # Failure returns dictionary full of None
        self.assertEqual(convert_weather("I have no idea what degree to get!"), None)
        self.assertRaises(ValueError, convert_weather, "twenty-eight degrees, wind five mph")

if __name__ == '__main__':
    unittest.main()
