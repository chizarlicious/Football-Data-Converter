#!/usr/bin/env python3


def convert_penalty(detail_string, team):
    """Takes in the "detail" field as a string and returns a penalty
    dictionary.

    args:
        detail_string: The detail field from the raw data
        team: The team code of the team that committed the penalty

    returns:
        A dictionary of the form:
            {"type" : "Illegal Use of Hands", "on" : "DEN", "player" :
            "Terrence Cody", "yards" : -5, "no play": true}
    """

def convert_turnover(detail_string):
    """Takes in the "detail" field as a string and returns a turnover
    dictionary.

    args:
        detail_string: The detail field from the raw data

    returns:
        A dictionary of the form:
            {"type" : "interception", "recovered by" : "DEN"}

            type: one of 'interception', 'fumble'
            recovered by: team code
    """
