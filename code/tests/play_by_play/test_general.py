#!/usr/bin/env python3

import unittest

from raw_data_parsers.play_by_play.general import row_type, get_kicking_team


class TestPlayByPlay(unittest.TestCase):

    def test_row_type(self):
        # Successful
        self.assertEqual(row_type("End of Overtime 38 35 0 0"), 6)
        self.assertEqual(
                row_type("Quarter Time Down ToGo Location Detail RAV DEN EPB EPA"),
                -1
                )
        self.assertEqual(
                row_type("""OT 15:00 1 10 DEN 34R Player passes but there are
                    dinosaurs on the field! 35 35 3.31 3.04"""),
                0
                )
        self.assertEqual(row_type("Overtime"), 5)
        self.assertEqual(row_type("1st Quarter"), 1)
        self.assertEqual(row_type("2nd Quarter"), 2)
        self.assertEqual(row_type("3rd Quarter"), 3)
        self.assertEqual(row_type("4th Quarter"), 4)

    def test_get_kicking_team(self):
        # Successful
        self.assertEqual(get_kicking_team("DEN 35"), "DEN")
        self.assertEqual(get_kicking_team("DEN 50"), "DEN")
        self.assertEqual(get_kicking_team("DEN"), "DEN")
        # Failure
        self.assertRaises(KeyError, get_kicking_team, "PTC 35")


if __name__ == '__main__':
    unittest.main()
