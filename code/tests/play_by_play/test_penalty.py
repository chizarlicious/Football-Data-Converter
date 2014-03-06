#!/usr/bin/env python3

import unittest

from raw_data_parsers.play_by_play.penalty import split_penalties, get_penalty_team, get_penalty_player, get_penalty_yards, get_penalty_type, get_penalty_name


class TestPlayByPlay(unittest.TestCase):

    def __set_penalty_consts(self):
        """Set penalties to be used by the penalty tests."""
        # Penalties
        self.penalties = (
            "Mercutio accepts duel (stabbed by Tybalt). Penalty on Romeo : Getting in the way (15 yards), 15 yards",
            "Ebenezer Scrooge avoids Christmas for no gain (tackle by Ghost of Christmas Future). Penalty on XMAS : Too many ghosts on the field, 5 yards (no play)",
            "Ugarte killed by Captain Louis Renault. Ugarte fumbles the letters of transit (forced by Captain Louis Renault), recovered by Rick Blaine at RCA (tackle by Illsa Lund). Penalty on Major Strasser : Being a Fascist, 5 yards, Penalty on Captain Louis Renault : Taking Bribes (Declined)",
            "Luke Skywalker shot on Deathstar no good. Penalty on Darth Vader: Illegal Formation (Declined)",
            "Operation Overlord beginning. Penalty on The Allies : Offensive Beach Storming, 100 yards (no play)",
            "Short in the LHC causes explosion! Penalty on Superconducting Interconnects : Illegal Contact, 137 yards",
            "I am not a penalty!"
        )
        # The result of running split_penalties on the penalties; also the
        # input for further test functions
        self.penalty_splits = (
            ["Penalty on Romeo : Getting in the way (15 yards), 15 yards"],
            ["Penalty on XMAS : Too many ghosts on the field, 5 yards (no play)"],
            [
                "Penalty on Major Strasser : Being a Fascist, 5 yards, ",
                "Penalty on Captain Louis Renault : Taking Bribes (Declined)"
            ],
            ["Penalty on Darth Vader: Illegal Formation (Declined)"],
            ["Penalty on The Allies : Offensive Beach Storming, 100 yards (no play)"],
            ["Penalty on Superconducting Interconnects : Illegal Contact, 137 yards"],
            []
        )

    def test_split_penalties(self):
        self.__set_penalty_consts()
        # Successful
        self.assertEqual(
                split_penalties(self.penalties[0]),
                self.penalty_splits[0]
                )
        self.assertEqual(
                split_penalties(self.penalties[1]),
                self.penalty_splits[1]
                )
        self.assertEqual(
                split_penalties(self.penalties[2]),
                self.penalty_splits[2]
                )
        self.assertEqual(
                split_penalties(self.penalties[3]),
                self.penalty_splits[3]
                )
        self.assertEqual(
                split_penalties(self.penalties[4]),
                self.penalty_splits[4]
                )
        self.assertEqual(
                split_penalties(self.penalties[5]),
                self.penalty_splits[5]
                )
        self.assertEqual(
                split_penalties(self.penalties[6]),
                self.penalty_splits[6]
                )

    def test_get_penalty_team(self):
        self.__set_penalty_consts()
        # Successful
        self.assertEqual(
                get_penalty_team(self.penalty_splits[0][0], '', '', '', ("Romeo"), ('')),
                "home"
                )
        self.assertEqual(
                get_penalty_team(self.penalty_splits[1][0], '', '', 'XMAS', (''), ('')),
                "away"
                )
        self.assertEqual(
                get_penalty_team(self.penalty_splits[2][0], '', '', '', ("Captain Louis Renault"), ("Major Strasser")),
                "away"
                )
        self.assertEqual(
                get_penalty_team(self.penalty_splits[2][1], '', '', '', ("Captain Louis Renault"), ("Major Strasser")),
                "home"
                )
        self.assertEqual(
                get_penalty_team(self.penalty_splits[3][0], '', '', '', ("Darth Vader"), ("Luke Skywalker")),
                "home"
                )
        self.assertEqual(
                get_penalty_team(self.penalty_splits[4][0], "away", '', '', '', ''),
                "away"
                )
        self.assertEqual(
                get_penalty_team(self.penalty_splits[5][0], "home", '', '', '', ''),
                "away"
                )

    def test_get_penalty_player(self):
        self.__set_penalty_consts()
        # Successful
        self.assertEqual(
                get_penalty_player(self.penalty_splits[0][0], '', ''),
                "Romeo"
                )
        self.assertEqual(
                get_penalty_player(self.penalty_splits[1][0], '', 'XMAS'),
                "team"
                )
        self.assertEqual(
                get_penalty_player(self.penalty_splits[2][0], '', ''),
                "Major Strasser"
                )
        self.assertEqual(
                get_penalty_player(self.penalty_splits[2][1], '', ''),
                "Captain Louis Renault"
                )
        self.assertEqual(
                get_penalty_player(self.penalty_splits[3][0], '', ''),
                "Darth Vader"
                )
        self.assertEqual(
                get_penalty_player(self.penalty_splits[4][0], '', ''),
                "The Allies"
                )
        self.assertEqual(
                get_penalty_player(self.penalty_splits[5][0], '', ''),
                "Superconducting Interconnects"
                )

    def test_get_penalty_yards(self):
        self.__set_penalty_consts()
        # Successful
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[0][0]),
                15
                )
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[1][0]),
                5
                )
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[2][0]),
                5
                )
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[2][1]),
                None
                )
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[3][0]),
                None
                )
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[4][0]),
                100
                )
        self.assertEqual(
                get_penalty_yards(self.penalty_splits[5][0]),
                137
                )
        # Failure
        self.assertRaises(ValueError, get_penalty_yards, "Ten yards")

    def test_get_penalty_type(self):
        self.__set_penalty_consts()
        # Successful
        self.assertEqual(get_penalty_type(self.penalty_splits[0][0]), "accepted")
        self.assertEqual(get_penalty_type(self.penalty_splits[1][0]), "no play")
        self.assertEqual(get_penalty_type(self.penalty_splits[2][0]), "accepted")
        self.assertEqual(get_penalty_type(self.penalty_splits[2][1]), "declined")
        self.assertEqual(get_penalty_type(self.penalty_splits[3][0]), "declined")
        self.assertEqual(get_penalty_type(self.penalty_splits[4][0]), "no play")
        self.assertEqual(get_penalty_type(self.penalty_splits[5][0]), "accepted")

    def test_get_penalty_name(self):
        self.__set_penalty_consts()
        # Successful
        self.assertEqual(
                get_penalty_name(self.penalty_splits[0][0]),
                "Getting in the way (15 yards)"
                )
        self.assertEqual(
                get_penalty_name(self.penalty_splits[1][0]),
                "Too many ghosts on the field"
                )
        self.assertEqual(
                get_penalty_name(self.penalty_splits[2][0]),
                "Being a Fascist"
                )
        self.assertEqual(get_penalty_name(self.penalty_splits[2][1]),
                "Taking Bribes"
                )
        self.assertEqual(get_penalty_name(self.penalty_splits[3][0]),
                "Illegal Formation"
                )
        self.assertEqual(get_penalty_name(self.penalty_splits[4][0]),
                "Offensive Beach Storming"
                )
        self.assertEqual(get_penalty_name(self.penalty_splits[5][0]),
                "Illegal Contact"
                )


if __name__ == '__main__':
    unittest.main()
