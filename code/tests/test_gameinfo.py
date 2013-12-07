#!/usr/bin/env python3

import unittest
from  import verify_times
from parse_raw_data.parse_gameinfo import convert_time


class TestGameInfo(unittest.TestCase):

    def test_convert_time(self):
        # Successful
        self.assertEqual(convert_time("09:32am"), "09:32")
        self.assertEqual(convert_time("1:59pm"), "13:59")
        # Failure returns none
        self.assertEqual(convert_time("foobarbaz"), None)
        self.assertEqual(convert_time("1:61pm"), None)

if __name__ == '__main__':
    unittest.main()
