#!/usr/bin/env python3

from data_helpers.team_list import team_codes, pfr_codes, pfr_codes_to_code


def convert_int(int_string):
    """Takes an int string and returns an integer.

    args:
        int_string: A string of an integer or ''.

    returns:
        An int, or None.

    raises:
        ValueError if the input is not an integer or ""
    """
    if not int_string:
        return None
    else:
        return int(int_string)


def convert_quarter(quarter_string):
    """Takes a quarter string and returns an integer.

    args:
        quarter_string: A string of 1-4, or "OT".

    returns:
        An int 1-5, with 5 indicating overtime.

    raises:
        ValueError if the input is not an integer [1, 4] or "OT"
    """
    if quarter_string == "OT":
        return 5
    else:
        quarter = int(quarter_string)
        if 1 <= quarter <= 4:
            return quarter
        else:
            raise ValueError("Quarter value is outside the permitted range.")


def convert_game_clock(time_string, quarter):
    """Takes a time_string and a quarter and returns seconds since the game
    began.

    args:
        time_string: A string in the following format: "MM:SS"
        quarter: An integer, 1-4 for normal play, 5 for the first overtime, 6
            for the second overtime, etc.

    returns:
        The number of seconds since the game began as an integer. A blank
            string returns None.

    raises:
        ValueError: If the game clock contains an invalid time format.
    """
    # For an empty string we return None
    if not time_string:
        return None
    # If it has a valid format, start parsing
    time_split = time_string.split(':')
    if time_split[0].startswith('-') or time_split[1].startswith('-'):
        raise ValueError("Game clock time is negative.")
    # Try to convert to ints
    try:
        minutes = int(time_split[0])
        seconds = int(time_split[1])
    except ValueError:  # Not an int!
        raise ValueError("Failed to convert minutes or seconds to an integer.")

    # Since the time on the game clock counts down in a quarter, we need to
    # subtract the time shown from 900 seconds (1 quarter) to find the time
    # since the quarter started
    mod_time = 900 - (minutes * 60 + seconds)

    if mod_time < 0:
        raise ValueError("Total time greater than 15:00")

    if (quarter < 1):
        raise ValueError("Quarter less than allowed value (1)")

    quarter_time = 900 * (quarter - 1)

    # Return total seconds played
    return quarter_time + mod_time


def convert_field_position(position_string, offense):
    """Takes a position_string and the team on offense and returns yards to the
    goal line.

    args:
        position_string: A string in the following format: "TEAM_CODE
            YARD_LINE", for example "DEN 34"
        offense: The team code of the team on offense.

    returns:
        The number of yards to the goal line as an integer. None if either
        input is blank.

    raises:
        ValueError: If the field position is invalid of the offense is not a
            valid team.
        KeyError: If the field position team marker is not a valid team.
    """
    # Skip if blank
    if not position_string or not offense:
        return None
    # Check that offense is valid
    if offense not in team_codes:
        raise ValueError("Invalid team code.")
    # If the position string is "50", it doesn't have a team code, but we know
    # the answer is 50.
    if position_string == "50":
        return 50
    # Parse the result
    position_split = position_string.split()
    pos_team_code_pfr = position_split[0]
    pos_team_code = pfr_codes_to_code[pos_team_code_pfr]
    # Make sure we have an integer as a field position
    yard = int(position_split[1])

    if yard > 50:
        raise ValueError("Yard line greater than allowed value (50)")
    elif yard < 1:
        raise ValueError("Yard line less than allowed value (1)")

    # If the offense and the position team code don't match, then we are on the
    # defense's side of the field and hence the answer is just the yard line.
    # Otherwise we are on the offense's side, and so the yard variables
    # contains the distance from the team's own goal, and hence the distance to
    # the opponent's goal is 100 - yard.
    if pos_team_code == offense:
        return 100 - yard
    else:
        return yard
