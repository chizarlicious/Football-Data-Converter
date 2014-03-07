#!/usr/bin/env python3

import unittest

from raw_data_parsers.play_by_play.turnover import split_turnovers, get_turnover_type, get_turnover_recoverer, get_turnover_committer, get_turnover_teams


class TestPlayByPlayTurnover(unittest.TestCase):

    def __set_turnover_consts(self):
        """Set penalties to be used by the penalty tests."""
        # Turnovers
        self.turnovers = (
            # Fumbled with a tackle afterwards
            "Josiah Barlet for no gain. Josiah Barlet fumbles, recovered by Matt Santos at PLC -30 (tackle by Leo McGarry)",
            # Interception returned for a touchdonw
            "Tom Petty pass incomplete short right intended for Roy Orbison is intercepted by Bob Dylan at PLC -39 and returned for 39 yards, touchdown",
            # Forced fumble with tackle afterwards
            "Ugarte killed by Captain Louis Renault for no gain. Ugarte fumbles the letters of transit (forced by Captain Louis Renault), recovered by Rick Blaine at RCA (tackle by Illsa Lund). Penalty on Major Strasser : Being a Fascist, 5 yards, Penalty on Captain Louis Renault : Taking Bribes (Declined)",
            # Unforced fumble for a safety, penalty declined
            "James Moriarty for no gain. James Moriarty fumbles, recovered by Sherlock Holmes at BBF --8, safety. Penalty on James Moriarty : Illegal Motion (Declined)",
            # Interception to fumble
            "Robert De Niro pass incomplete short middle intended for Jean Reno is intercepted by Stellan Skarsgård at PLC -9 and returned for 31 yards (tackle by Jean Reno). Stellan Skarsgård fumbles (forced by Jean Reno ), recovered by Sean Bean at PLC -44 (tackle by Skipp Sudduth )",
            # Players with periods in their names
            "J.R. Oppenheimer says 'Now I am become death, the destroyer of worlds.' for no gain. R. P. Feynman fumbles, recovered by E. Fermi at LAL -20 (tackle by E. Lawrence)",
            # Fumble that is not recovered
            "Men Without Hats runs for 10 yards. Men Without Hats fumbles, safety",
            # Not a turnover
            "Sisyphus up the middle for no gain."
        )
        # The result of running split_turnovers on the turnovers; also the
        # input for further test functions
        self.turnover_splits = (
            ["Josiah Barlet fumbles, recovered by Matt Santos at PLC -30 (tackle by Leo McGarry)"],
            ["Tom Petty pass incomplete short right intended for Roy Orbison is intercepted by Bob Dylan at PLC -39 and returned for 39 yards, touchdown"],
            ["Ugarte fumbles the letters of transit (forced by Captain Louis Renault), recovered by Rick Blaine at RCA (tackle by Illsa Lund"],
            ["James Moriarty fumbles, recovered by Sherlock Holmes at BBF --8,"],
            [
                "Robert De Niro pass incomplete short middle intended for Jean Reno is intercepted by Stellan Skarsgård at PLC -9 and returned for 31 yards (tackle by Jean Reno",
                "Stellan Skarsgård fumbles (forced by Jean Reno ), recovered by Sean Bean at PLC -44 (tackle by Skipp Sudduth )"
            ],
            ["R. P. Feynman fumbles, recovered by E. Fermi at LAL -20 (tackle by E. Lawrence)"],
            ["Men Without Hats fumbles, safety"],
            []
        )

    def test_split_turnovers(self):
        self.__set_turnover_consts()
        # Successful
        self.assertEqual(
                split_turnovers(self.turnovers[0]),
                self.turnover_splits[0]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[1]),
                self.turnover_splits[1]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[2]),
                self.turnover_splits[2]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[3]),
                self.turnover_splits[3]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[4]),
                self.turnover_splits[4]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[5]),
                self.turnover_splits[5]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[6]),
                self.turnover_splits[6]
                )
        self.assertEqual(
                split_turnovers(self.turnovers[7]),
                self.turnover_splits[7]
                )

    def test_get_turnover_type(self):
        self.__set_turnover_consts()
        # Successful
        self.assertEqual(
                get_turnover_type(self.turnover_splits[0][0]),
                "fumble"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[1][0]),
                "interception"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[2][0]),
                "fumble"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[3][0]),
                "fumble"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[4][0]),
                "interception"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[4][1]),
                "fumble"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[5][0]),
                "fumble"
                )
        self.assertEqual(
                get_turnover_type(self.turnover_splits[6][0]),
                "fumble"
                )

    def test_get_turnover_recoverer(self):
        self.__set_turnover_consts()
        # Successful
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[0][0]),
                "Matt Santos"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[1][0]),
                "Bob Dylan"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[2][0]),
                "Rick Blaine"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[3][0]),
                "Sherlock Holmes"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[4][0]),
                "Stellan Skarsgård"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[4][1]),
                "Sean Bean"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[5][0]),
                "E. Fermi"
                )
        self.assertEqual(
                get_turnover_recoverer(self.turnover_splits[6][0]),
                False
                )

    def test_get_turnover_committer(self):
        self.__set_turnover_consts()
        # Successful
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[0][0]),
                "Josiah Barlet"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[1][0]),
                "Tom Petty"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[2][0]),
                "Ugarte"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[3][0]),
                "James Moriarty"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[4][0]),
                "Robert De Niro"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[4][1]),
                "Stellan Skarsgård"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[5][0]),
                "R. P. Feynman"
                )
        self.assertEqual(
                get_turnover_committer(self.turnover_splits[6][0]),
                "Men Without Hats"
                )

    def test_get_turnover_teams(self):
        self.__set_turnover_consts()
        # Successful
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[0][0],
                    ("Josiah Barlet", "Leo McGarry"),
                    ("Matt Santos",),
                    ),
                ("home", "away")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[1][0],
                    ("Tom Petty", "Roy Orbison"),
                    ("Bob Dylan",),
                    ),
                ("home", "away")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[2][0],
                    ("Ugarte", "Rick Blaine"),
                    ("Captain Louis Renault", "Major Strasser"),
                    ),
                ("home", "home")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[3][0],
                    ("James Moriarty",),
                    ("Sherlock Holmes",),
                    ),
                ("home", "away")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[4][0],
                    ("Robert De Niro", "Jean Reno", "Sean Bean"),
                    ("Stellan Skarsgård",),
                    ),
                ("home", "away")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[4][1],
                    ("Robert De Niro", "Jean Reno", "Sean Bean"),
                    ("Stellan Skarsgård",),
                    ),
                ("away", "home")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[5][0],
                    ("J.R. Oppenheimer", "R. P. Feynman"),
                    ("E. Fermi",),
                    ),
                ("home", "away")
                )
        self.assertEqual(
                get_turnover_teams(
                    self.turnover_splits[6][0],
                    ("Men Without Hats",),
                    ("Ivan Doroschuk",),
                    ),
                ("home", False)
                )


if __name__ == '__main__':
    unittest.main()
