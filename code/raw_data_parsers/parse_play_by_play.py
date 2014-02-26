#!/usr/bin/env python3

from errors.parsing_errors import GameClockError, FieldPositionError, TeamCodeError
from data_helpers.team_list import team_codes, pfr_codes, pfr_codes_to_code


def row_type(row):
    """Takes a row of plain text and returns the type.

    args:
        row: A row from BrautifulSoup, filtered with soup.find_all("tr") and
        parsed with get_text(' ', strip=True)

    returns:
        An integer indicating the type of row:
            -1: Header
            0: Normal Row
            1: 1st Quarter
            2: 2nd Quarter
            3: 3rd Quarter
            4: 4th Quarter
            5: New Overtime
            6: End of Game/Overtime
    """
    if "Quarter Time Down" in row:
        return -1
    elif "1st Quarter" in row:
        return 1
    elif "2nd Quarter" in row:
        return 2
    elif "3rd Quarter" in row:
        return 3
    elif "4th Quarter" in row:
        return 4
    elif "End" in row:
        return 6
    elif "Overtime" in row:
        return 5
    else:
        return 0


def get_teams(header_soup):
    """Takes a BeautifulSoup4 row and returns the home and away teams.

    args:
        header_soup: A BS4 row containing the play-by-play header information.

    returns:
        A tuple of (home, away)

    raises:
        KeyError if the team codes don't exist, or if the header can't be split
            correctly.
    """
    cols = header_soup.find_all("th")
    home = pfr_codes_to_code[cols[7].get_text(strip=True)]
    away = pfr_codes_to_code[cols[6].get_text(strip=True)]
    return (home, away)


def get_kicking_team(cols_soup):
    """Takes a BeautifulSoup4 row and returns the kicking team on kickoff.

    args:
        cols_soup: A BS4 list of columns containing the play-by-play
        information for a kickoff.

    returns:
        A string of the kicking team's code.

    raises:
        KeyError if the team codes don't exist.
    """
    split_cols = cols_soup[4].get_text(strip=True).split()
    return pfr_codes_to_code[split_cols[0]]


def get_play_type(pt):
    """Takes a string and returns the play type

    args:
        pt: A string containing the play-by-play information.

    returns:
        A string from the following list:
            "punt", "kick off", "complete pass", "incomplete pass", "run",
            "sack",
    """
    pt = pt.replace('\n', ' ')
    pt = pt.lower()
    # Punts
    if "punt" in pt:
        return "punt"
    # Two point conversion
    elif "two point attempt:" in pt or "conversion" in pt:
        if "incomplete" in pt:
            return "two point conversion with incomplete pass"
        elif "complete" in pt:
            return "two point conversion with complete pass"
        else:
            return "two point conversion with run"
    elif "kicks off" in pt:
        return "kick off"
    # Sacks
    elif "sack" in pt:
        return "sack"
    # Field Goal
    elif "field goal" in pt:
        return "field goal"
    # Pass
    elif "pass incomplete" in pt:
        return "incomplete pass"
    elif "pass complete" in pt:
        return "complete pass"
    # Extra point
    elif "extra point" in pt:
        return "extra point"
    # Time Out
    elif "timeout" in pt:
        return "timeout"
    # Kneel
    elif "kneel" in pt:
        return "kneel"
    # Spike
    elif "spiked" in pt:
        return "spike"
    # Penalty before snap
    elif pt.split()[0] == "penalty":
        return "penalty"
    # Run
    elif "for" in pt and ("yard" in pt or "no gain" in pt):
        return "run"
    # Unmatched!!!!
    else:
        print("Unmatched play type!", pt)
        return None


def get_scoring_type(cols_soup):
    """Takes a BeautifulSoup4 row and returns the scoring type

    args:
        cols_soup: A BS4 list of columns containing the play-by-play
        information.

    returns:
        A string from the following list:
            "touchdown", "field goal", "two point conversion", "safety",
            "extra point"
    """
    pt = cols_soup[5].get_text(' ', strip=True)
    pt = pt.replace('\n', ' ')
    pt = pt.lower()
    if "extra point" in pt:
        return "extra point"
    elif "touchdown" in pt:
        return "touchdown"
    elif "safety" in pt:
        return "safety"
    elif "two point" in pt:
        return "two point conversion"
    elif "field goal" in pt:
        return "field goal"
    else:
        print("Unmatched Score type!", pt)
        return None


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
        ValueError if the input is not an integer or "OT"
    """
    if quarter_string == "OT":
        return 5
    else:
        return int(quarter_string)


def convert_game_clock(time_string, quarter):
    """Takes a time_string and a quarter and returns seconds since the game
    began.

    args:
        time_string: A string in the following format: "MM:SS"
        quarter: An integer, 1-4 for normal play, 5 for the first overtime, 6
            for the second overtime, etc.

    returns:
        The number of seconds since the game began as an integer. Failure
            raises GameClockError. A blank string returns None.

    raises:
        GameClockError: If the game clock contains an invalid time format.
    """
    # For an empty string we return None
    if not time_string:
        return None
    # If it has a valid format, start parsing
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
        The number of yards to the goal line as an integer. None if either
        input is blank.

    raises:
        FieldPositionError: If the field position is invalid.
        TeamCodeError: If the offense is not a valid team, or the field
            position team marker is not a valid team.
    """
    # Skip if blank
    if not position_string or not offense:
        return None
    # If the position string is "50", it doesn't have a team code, but we know
    # the answer is 50.
    if position_string == "50":
        return 50
    # Parse the result
    position_split = position_string.split()
    pos_team_code_pfr = position_split[0]
    if pos_team_code_pfr not in pfr_codes:
        raise TeamCodeError("Field Position does not reference a valid team code.")
    else:
        pos_team_code = pfr_codes_to_code[pos_team_code_pfr]
    # Check that the listed teams are valid
    if offense not in team_codes:
        raise TeamCodeError("Offense not a valid team code.")
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
