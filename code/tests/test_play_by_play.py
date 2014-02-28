#!/usr/bin/env python3

import unittest
import sys
import os

from raw_data_parsers.parse_play_by_play.state import convert_int, convert_quarter, convert_game_clock, convert_field_position
from raw_data_parsers.parse_play_by_play.play import get_play_type, get_scoring_type
from raw_data_parsers.parse_play_by_play.general import row_type, get_kicking_team

from errors.parsing_errors import GameClockError, FieldPositionError, TeamCodeError


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

    def test_get_play_type(self):
        # Successful
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
        self.assertEqual(convert_field_position("50", "DEN"), 50)
        self.assertEqual(convert_field_position("", "DEN"), None)
        self.assertEqual(convert_field_position("MIN 35", ""), None)
        # Failure
        self.assertRaises(FieldPositionError, convert_field_position, "DEN 51", "DEN")
        self.assertRaises(FieldPositionError, convert_field_position, "DEN Inches", "DEN")
        self.assertRaises(TeamCodeError, convert_field_position, "DEN 34", "FRN")
        self.assertRaises(TeamCodeError, convert_field_position, "FRN 34", "DEN")

if __name__ == '__main__':
    unittest.main()
