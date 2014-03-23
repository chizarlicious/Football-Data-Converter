#!/usr/bin/env python3

import unittest
import sys
import os

from raw_data_parsers.play_by_play.play import get_play_type, get_scoring_type


class TestPlayByPlay(unittest.TestCase):

    def test_get_play_type(self):
        # Successful
        self.assertEqual(get_play_type("--"), None)
        self.assertEqual(
                get_play_type("""Isaac Newton punts 52 yards, returned by
                    Gottfried Wilhelm von Leibniz for -7 yards (tackle by Royal
                    Society)"""),
                "punt"
                )
        self.assertEqual(
                get_play_type("""Two Point Attempt: Saul Perlmutter pass
                    incomplete, conversion fails. Penalty on SFO : Illegal
                    Touch Pass (Declined)"""),
                "two point conversion with incomplete pass"
                )
        self.assertEqual(
                get_play_type("""Two Point Attempt: Wolfgang Amadeus Mozart
                    pass complete to Antonio Salieri, conversion succeeds"""),
                "two point conversion with complete pass"
                )
        self.assertEqual(
                get_play_type("""Two Point Attempt: Pheidippides up the middle,
                    conversion succeeds"""),
                "two point conversion with run"
                )
        self.assertEqual(
                get_play_type("""Julius Caesar kicks off 70 yards, muffed catch
                    by Mark Antony, recovered by Gaius Octavius and returned
                    for no gain"""),
                "kick off"
                )
        self.assertEqual(
                get_play_type("""Neville Chamberlain kicks onside, recovered by
                    the Axis."""),
                "onside kick"
                )
        self.assertEqual(
                get_play_type("""Nikolai Yezhov sacked by Joseph Stalin and
                    Ivan Serov for -7 yards"""),
                "sack"
                )
        self.assertEqual(
                get_play_type("Albert Einstein 52 yard field goal no good"),
                "field goal"
                )
        self.assertEqual(
                get_play_type("""Antinous pass incomplete short middle intended
                    for Penelope. (defended by Odysseus).  Penalty on Odysseus:
                    Defensive Pass Interference, 9 yards (no play)"""),
                "incomplete pass"
                )
        self.assertEqual(
                get_play_type("""Bill Gates pass complete short right to Steve
                    Ballmer for 9 yards (tackle by Steve Jobs)"""),
                "complete pass"
                )
        self.assertEqual(
                get_play_type("Bruce Springsteen kicks extra point good"),
                "extra point"
                )
        self.assertEqual(
                get_play_type("Timeout #1 by The E Street Band"),
                "timeout"
                )
        self.assertEqual(
                get_play_type("Superman kneels before Zod for -1 yards"),
                "kneel"
                )
        self.assertEqual(
                get_play_type("Arthur C. Clarke spiked the ball"),
                "spike"
                )
        self.assertEqual(
                get_play_type("Aborted snap. G. Khan fumbles, recovered by K. Tolui at EUR -23 (tackled by Ögödei Kahn )."),
                "aborted snap"
                )
        self.assertEqual(
                get_play_type("""Isaac Asimov up the middle for 11 yards
                    (tackle by Ray Bradbury)"""),
                "run"
                )
        # We squelch the warning from this test, we want the warning when
        # running on data, but not when testing
        with open(os.devnull, 'w') as f:
            oldstdout = sys.stdout
            f = open(os.devnull, 'w')
            sys.stdout = f
            self.assertEqual(
                    get_play_type("What are you even talking about?"),
                    None
                    )
            # Return stdout
            sys.stdout = oldstdout
            f.close()

    def test_get_score_type(self):
        # Successful
        self.assertEqual(
                get_scoring_type("""Edson Arantes do Nascimento (Pelé) kicks
                    extra point good"""),
                "extra point"
                )
        self.assertEqual(
                get_scoring_type("""Sauron punts 52 yards, returned by Frodo
                    for 90 yards, touchdown"""),
                "touchdown"
                )
        self.assertEqual(
                get_scoring_type("""Abraham Lincoln pass complete deep right to
                    Andrew Johnson for 59 yards, touchdown"""),
                "touchdown"
                )
        self.assertEqual(
                get_scoring_type("""Hephaestus for no gain. Ares fumbles,
                    recovered by Aphrodite at OLY --8, safety.  Penalty on
                    Hephaestus : Illegal Motion (Declined)"""),
                "safety"
                )
        self.assertEqual(
                get_scoring_type("""Two Point Attempt: George Washington pass
                    complete to John Adams, conversion succeeds"""),
                "two point conversion"
                )
        self.assertEqual(
                get_scoring_type("Perseus 31 yard field goal good"),
                "field goal"
                )
        # We squelch the warning from this test, we want the warning when
        # running on data, but not when testing
        with open(os.devnull, 'w') as f:
            oldstdout = sys.stdout
            f = open(os.devnull, 'w')
            sys.stdout = f
            self.assertEqual(
                    get_scoring_type("""Paul McCartney pass incomplete short
                        right intended for Ringo Starr (defended by George
                        Harrison).  Penalty on John Lennon : Defensive Pass
                        Interference, 4 yards (no play)"""),
                    None
                    )
            # Return stdout
            sys.stdout = oldstdout
            f.close()


if __name__ == '__main__':
    unittest.main()
