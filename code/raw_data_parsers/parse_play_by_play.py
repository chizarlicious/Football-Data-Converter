#!/usr/bin/env python3

from errors.parsing_errors import GameClockError, FieldPositionError, TeamCodeError
from data_helpers.team_list import team_codes


def convert_game_clock(time_string, quarter):
    """Takes a time_string and a quarter and returns seconds since the game
    began.

    args:
        time_string: A string in the following format: "MM:SS"
        quarter: An integer, 1-4 for normal play, 5 for the first overtime, 6
            for the second overtime, etc.

    returns:
        The number of seconds since the game began as an integer. Failure
            raises GameClockError.

    raises:
        GameClockError: If the game clock contains an invalid time format.
    """
    time_split = time_string.split(':')
    if time_split[0].startswith('-') or time_split[1].startswith('-'):
        raise GameClockError("Game clock time is negative.")
    # Try to convert to ints
    try:
        minutes = int(time_split[0])
        seconds = int(time_split[1])
    except ValueError:  # Not an int!
        raise GameClockError("Failed to convert minutes or seconds to an integer.")

    # Since the time on the game clock counts down in a quarter, we need to
    # subtract the time shown from 900 seconds (1 quarter) to find the time
    # since the quarter started
    mod_time = 900 - (minutes * 60 + seconds)

    if mod_time < 0:
        raise GameClockError("Total time greater than 15:00")

    if (quarter < 1):
        raise GameClockError("Quarter less than allowed value (1)")

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
        The number of yards to the goal line as an integer.

    raises:
        FieldPositionError: If the field position is invalid.
        TeamCodeError: If the offense is not a valid team, or the field
            position team marker is not a valid team.
    """
    position_split = position_string.split()
    pos_team_code = position_split[0]
    # Check that the listed teams are valid
    if offense not in team_codes:
        raise TeamCodeError("Offense not a valid team code.")
    elif pos_team_code not in team_codes:
        raise TeamCodeError("Field Position does not reference a valid team code.")
    # Make sure we have an integer as a field position
    try:
        yard = int(position_split[1])
    except ValueError:
        raise FieldPositionError("Invalid field position.")

    if yard > 50:
        raise FieldPositionError("Yard line greater than allowed value (50)")
    elif yard < 1:
        raise FieldPositionError("Yard line less than allowed value (1)")

    # If the offense and the position team code don't match, then we are on the
    # defense's side of the field and hence the answer is just the yard line.
    # Otherwise we are on the offense's side, and so the yard variables
    # contains the distance from the team's own goal, and hence the distance to
    # the opponent's goal is 100 - yard.
    if pos_team_code == offense:
        return 100 - yard
    else:
        return yard
