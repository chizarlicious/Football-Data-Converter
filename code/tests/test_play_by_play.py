#!/usr/bin/env python3

import unittest

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

    def test_get_play_type(self):
        # Successful
        self.assertEqual(
                get_play_type("""Sam Koch punts 52 yards, returned by Trindon
                    Holliday for -7 yards (tackle by Jimmy Smith )"""),
                "punt"
                )
        self.assertEqual(
                get_play_type("""Two Point Attempt: Jeff Garcia pass
                    incomplete, conversion fails. Penalty on SFO : Illegal
                    Touch Pass (Declined)"""),
                "two point conversion with incomplete pass"
                )
        self.assertEqual(
                get_play_type("""Two Point Attempt: Matthew Stafford pass
                    complete to Joseph Fauria , conversion succeeds"""),
                "two point conversion with complete pass"
                )
        self.assertEqual(
                get_play_type("""Two Point Attempt: Mark Brunell up the middle,
                    conversion succeeds"""),
                "two point conversion with run"
                )
        self.assertEqual(
                get_play_type("""Matt Prater kicks off 70 yards, muffed catch
                    by Jacoby Jones , recovered by Jacoby Jones and returned
                    for no gain"""),
                "kick off"
                )
        self.assertEqual(
                get_play_type("""Joe Flacco sacked by Von Miller and Elvis
                    Dumervil for -7 yards"""),
                "sack"
                )
        self.assertEqual(
                get_play_type("Matt Prater 52 yard field goal no good"),
                "field goal"
                )
        self.assertEqual(
                get_play_type("""Joe Flacco pass incomplete short middle
                    intended for Torrey Smith (defended by Champ Bailey ).
                    Penalty on Champ Bailey : Defensive Pass Interference, 9
                    yards (no play)"""),
                "incomplete pass"
                )
        self.assertEqual(
                get_play_type("""Peyton Manning pass complete short right to
                    Brandon Stokley for 9 yards (tackle by Corey Graham)"""),
                "complete pass"
                )
        self.assertEqual(
                get_play_type("Justin Tucker kicks extra point good"),
                "extra point"
                )
        self.assertEqual(
                get_play_type("Timeout #1 by Denver Broncos"),
                "timeout"
                )
        self.assertEqual(
                get_play_type("Peyton Manning kneels for -1 yards"),
                "kneel"
                )
        self.assertEqual(
                get_play_type("Randall Cunningham spiked the ball"),
                 "spike"
                )
        self.assertEqual(
                get_play_type("""Ray Rice up the middle for 11 yards (tackle by
                    Mike Adams)"""),
                "run"
                )

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
        self.assertEqual(convert_field_position("50", "DEN"), 50)
        self.assertEqual(convert_field_position("", "DEN"), None)
        self.assertEqual(convert_field_position("MIN 35", ""), None)
        # Failure returns None
        self.assertRaises(FieldPositionError, convert_field_position, "DEN 51", "DEN")
        self.assertRaises(FieldPositionError, convert_field_position, "DEN Inches", "DEN")
        self.assertRaises(TeamCodeError, convert_field_position, "DEN 34", "FRN")
        self.assertRaises(TeamCodeError, convert_field_position, "FRN 34", "DEN")

if __name__ == '__main__':
    unittest.main()
