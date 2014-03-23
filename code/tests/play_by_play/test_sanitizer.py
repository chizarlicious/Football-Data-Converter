#!/usr/bin/env python3

import unittest

from raw_data_parsers.play_by_play.sanitizer import get_challenge_type, remove_challenge


class TestPlayByPlaySanitizer(unittest.TestCase):

    def __set_sanitizer_consts(self):
        """Set penalties to be used by the penalty tests."""
        # Turnovers
        self.challenges = (
            #
            "G. W. Bush up the middle for -2 yards (tackle by A. Gore ). G. W. Bush fumbles (forced by A. Gore ), recovered by W. Rehnquist at LOC -26 and returned for 74 yards, touchdown. Replay Assistant challenged the fumble ruling, and the play was upheld.",
            #
            "John Adams pass incomplete short middle intended for William Marbury is intercepted by John Marshall at LOC -17 and returned for 12 yards (tackle by John Adams ). Replay Assistant challenged the pass completion ruling, and the play was overturned. John Adams pass incomplete short middle intended for William Marbury (defended by John Marshall )",
            # Do nothing
            "C. J. Browne pass incomplete short right intended for D. P. Lindley . C. J. Browne fumbles, recovered by C. J. Browne at SEA -14",
        )
        # The result of running the sanitizer
        self.results = (
            "G. W. Bush up the middle for -2 yards (tackle by A. Gore ). G. W. Bush fumbles (forced by A. Gore ), recovered by W. Rehnquist at LOC -26 and returned for 74 yards, touchdown.",
            "John Adams pass incomplete short middle intended for William Marbury (defended by John Marshall )",
            "C. J. Browne pass incomplete short right intended for D. P. Lindley . C. J. Browne fumbles, recovered by C. J. Browne at SEA -14",
        )

    def test_get_challenge_type(self):
        self.__set_sanitizer_consts()
        # Successful
        self.assertEqual(get_challenge_type(self.challenges[0]), "upheld")
        self.assertEqual(get_challenge_type(self.challenges[1]), "overturned")
        self.assertEqual(get_challenge_type(self.challenges[2]), False)

    def test_remove_challenge(self):
        self.__set_sanitizer_consts()
        # Successful
        self.assertEqual(
                remove_challenge(self.challenges[0]),
                self.results[0]
                )
        self.assertEqual(
                remove_challenge(self.challenges[1]),
                self.results[1]
                )
        self.assertEqual(
                remove_challenge(self.challenges[2]),
                self.results[2]
                )


if __name__ == '__main__':
    unittest.main()
