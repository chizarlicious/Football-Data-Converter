#!/usr/bin/env python3

from errors.parsing_errors import GameClockError, FieldPositionError, TeamCodeError
from data_helpers.team_list import team_codes, pfr_codes, pfr_codes_to_code


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
