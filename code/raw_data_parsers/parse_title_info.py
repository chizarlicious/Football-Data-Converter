#!/usr/bin/env python3

from time import strptime, strftime
from data_helpers.team_list import names_to_code


def convert_title_teams(title_string):
    """Takes in string of the form "Baltimore Ravens at Denver Broncos" and
    returns the team codes for each team.

    args:
        title_string: The teams part of the title in the form "Away Team at
        Home Team".

    returns:
        A tuple of team codes in the form (home_team, away_team).

    raises:
        KeyError if the team doesn't exist in names_to_code.
        IndexError if there is no " at " to break on.
    """
    away = title_string.split(' at ')[0].strip()
    home = title_string.split(' at ')[1].strip()
    away_code = names_to_code[away]
    home_code = names_to_code[home]
    return (home_code, away_code)


def convert_title_date(time_string):
    """Takes in string of the form "January 2nd, 2001" and returns the ISO 8601
    date.

    args:
        time_string: A string in the form "January 2nd, 2001".

    returns:
        A string of the date in ISO 8601 format ("%B %d, %Y").

    raises:
        ValueError if the time format isn't recognized.
    """
    # We need to strip the suffixes from dates. For example, from 1st.
    for suffix in ("st", "nd", "rd", "th"):
        time_string = time_string.replace(suffix, '')
    time_string = time_string.strip()
    # Now we convert to ISO 8601
    time_object = strptime(time_string, "%B %d, %Y")
    return strftime("%Y-%m-%d", time_object)
