#!/usr/bin/env python3

from datetime import datetime
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
        ValueError if there is no " at " or " vs. " to break on.
    """
    # Determine if the teams are separated by at or vs.
    if " at " in title_string:
        split_key = " at "
    elif " vs. " in title_string:
        split_key = " vs. "
    else:
        raise ValueError
    # Split and try to assign a code
    away = title_string.split(split_key)[0].strip()
    home = title_string.split(split_key)[1].strip()
    away_code = names_to_code[away]
    home_code = names_to_code[home]
    return (home_code, away_code)


def convert_title_date(time_string):
    """Takes in string of the form "January 2nd, 2001" and returns the ISO 8601
    date.

    args:
        time_string: A string in the form "January 2nd, 2001".

    returns:
        A string of the date in ISO 8601 format "%Y-%m-%d".

    raises:
        ValueError if the time format isn't recognized.
    """
    # We need to strip the suffixes from dates. For example, from 1st.
    for suffix in ("st", "nd", "rd", "th"):
        time_string = time_string.replace(suffix, '')
    time_string = time_string.strip()
    # Now we convert to ISO 8601
    time_object = datetime.strptime(time_string, "%B %d, %Y")
    return time_object.strftime("%Y-%m-%d")


def get_season(time_string):
    """Takes in string of the form "January 2nd, 2001" and returns the NFL
    season year.

    args:
        time_string: A string in the form "January 2nd, 2001".

    returns:
        An int indicating the season year.

    raises:
        ValueError if the time format isn't recognized.
    """
    # We need to strip the suffixes from dates. For example, from 1st.
    for suffix in ("st", "nd", "rd", "th"):
        time_string = time_string.replace(suffix, '')
    time_string = time_string.strip()
    # Make a date object
    dt_object = datetime.strptime(time_string, "%B %d, %Y")
    year = dt_object.year
    start = datetime(year, 6, 1)
    end = datetime(year + 1, 3, 1)
    if start < dt_object < end:
        return year
    else:
        return year - 1


def get_output_date(time_string):
    """Takes in string of the form "January 2nd, 2001" and returns the date in
    the form "%Y%m%d".

    args:
        time_string: A string in the form "January 2nd, 2001".

    returns:
        A string of the date in ISO 8601 format "%Y%m%d"

    raises:
        ValueError if the time format isn't recognized.
    """
    iso_date = convert_title_date(time_string)
    time_object = datetime.strptime(iso_date, "%Y-%m-%d")
    return time_object.strftime("%Y%m%d")
