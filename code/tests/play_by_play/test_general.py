#!/usr/bin/env python3

import unittest
import sys
import os

from raw_data_parsers.play_by_play.general import row_type, get_kicking_offense


class TestPlayByPlay(unittest.TestCase):

    def __set_kicking_consts(self):
        """Set play stings to be used by the kicking tests."""
        # Turnovers
        self.kicks = (
            "B. Simpson kicks off 70 yards, returned by M. Simpson for 20 yards (tackle by L. Simpson )",
            "Moe Howard kicks onside 12 yards, recovered by Shemp Howard . Larry Fine fumbles, recovered by Curly Howard at LOC -41",
            "Louis C.K. Kicks off.",
        )

    def test_row_type(self):
        # Successful
        self.assertEqual(row_type("End of Overtime 38 35 0 0"), 6)
        self.assertEqual(
                row_type(
                    "Quarter Time Down ToGo Location Detail RAV DEN EPB EPA"
                    ),
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

    def test_get_kicking_offense(self):
        self.__set_kicking_consts()
        # Successful
        self.assertEqual(
                get_kicking_offense(
                    "DEN 35", "", "DEN", "SEA", (), ()
                    ),
                "away"
                )
        self.assertEqual(
                get_kicking_offense(
                    "SEA 35", "", "DEN", "SEA", (), ()
                    ),
                "home"
                )
        self.assertEqual(
                get_kicking_offense(
                    "DEN 50", "", "DEN", "SEA", (), ()
                    ),
                "away"
                )
        self.assertEqual(
                get_kicking_offense("DEN", "", "DEN", "SEA", (), ()),
                "away"
                )
        self.assertEqual(
                get_kicking_offense(
                    "",
                    self.kicks[0],
                    "DEN",
                    "SEA",
                    ("B. Simpson", "L. Simpson"),
                    ("M. Simpson",)
                    ),
                "away"
                )
        self.assertEqual(
                get_kicking_offense(
                    "",
                    self.kicks[1],
                    "DEN",
                    "SEA",
                    ("Shemp Howard",),
                    ("Moe Howard", "Larry Fine", "Curly Howard")
                    ),
                "home"
                )
        # Failure
        self.assertRaises(
                KeyError,
                get_kicking_offense, "PTC 35", "", "", "", (), ()
                )
        # We squelch the warning from this test, we want the warning when
        # running on data, but not when testing
        with open(os.devnull, 'w') as f:
            oldstdout = sys.stdout
            f = open(os.devnull, 'w')
            sys.stdout = f
            # The squelched tests
            # Unknown kicker
            self.assertEqual(
                    get_kicking_offense("", self.kicks[2], "", "", (), ()),
                    None
                    )
            # Degenerate kicker
            self.assertEqual(
                    get_kicking_offense(
                        "", self.kicks[2], "", "", ("Player8",), ("Player8",)
                        ),
                    None
                    )
            # Unknown team
            self.assertEqual(
                    get_kicking_offense(
                        "DEN 35", self.kicks[2], "SEA", "SFO", (), ()
                        ),
                    None
                    )
            # Return stdout
            sys.stdout = oldstdout
            f.close()


if __name__ == '__main__':
    unittest.main()
