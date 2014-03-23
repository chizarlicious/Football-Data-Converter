#!/usr/bin/env python3

from data_helpers.team_list import pfr_codes_to_code


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


def get_kicking_offense(
        kick_text,
        play_text,
        home_team,
        away_team,
        home_players,
        away_players
        ):
    """Takes a field position, a string describing the play, the teams, and the
    plays, and returns the offense on a kickoff.

    args:
        kick_text: A string giving the field position.
        play_text: A string giving a description of the play.
        home_team, away_team: The team code for the home and away team,
            respectively.
        home_players, away_players: Iterables that support 'in' containing a
            list of all players on the home and away team, respectively.

    returns:
        A string of "home" or "away", or None.

    raises:
        KeyError if the team codes don't exist.
    """
    split_cols = kick_text.split()
    # It is easiest to get the kicking team from the field position, but
    # sometimes this isn't provided (often because of a penalty on the
    # kickoff).
    if split_cols:
        code = pfr_codes_to_code[split_cols[0]]
        # Remember, if the "home" team is kicking, the "away" team is on
        # offense
        if code == home_team:
            return "away"
        elif code == away_team:
            return "home"
        else:
            print("UNKNOWN KICKING TEAM", code, away_team, "at", home_team)
            return None
    # We now fall back to using the description of the play and looking at the
    # kicker
    else:
        kicker = play_text.split("kicks")[0].strip()
        is_home = (kicker in home_players)
        is_away = (kicker in away_players)
        if is_home and not is_away:
            return "away"
        elif is_away and not is_home:
            return "home"
        elif is_home and is_away:
            print("\tDEGENERATE KICKER!", kicker, away_team, 'at', home_team)
            return None
        else:
            print("\tUNKNOWN KICKER!", kicker, away_team, 'at', home_team)
            return None
