#!/usr/bin/env python3

import re

from data_helpers.team_list import pfr_codes_to_code, pfr_codes


def split_turnovers(col):
    """Takes a string describing the play, and splits it into a list of the
    turnovers.

    args:
        col: A string describing the play.

    returns:
        A list of strings.
    """
    final_list = []
    # Split on several different substring
    reg_list = (
            "\)\.",           # ').'
            " yards\.",       # ' yards.'
            " yard\.",        # ' yard.'
            " gain\.",        # ' gain.'
            " safety\.",      # ' safety.'
            " incomplete\.",  # ' incomplete.'
            " snap\.",        # ' snap.'
            "[0-9]\.",        # Number followed by period
            # Starting at 'intended for', match any word consisting of A
            # through Z (ignoring case) or a period until ' .'.
            # This is used for QB fumbles
            "intended for( [a-zA-Z.]+)* \."
            )
    regex = "|".join(reg_list)
    for item in re.split(regex, col):
        if item is not None:
            if "fumble" in item.lower() \
            or "intercepted" in item.lower() \
            or "muffed" in item.lower():
                final_list.append(item.strip())

    return final_list


def get_turnover_type(turnover_string):
    """Takes a string describing the play, and returns the type of turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.

    returns:
        A string indicating the type, or None if it can't be figured out
    """
    if "fumble" in turnover_string.lower():
        return "fumble"
    elif "intercept" in turnover_string.lower():
        return "interception"
    elif "muffed" in turnover_string.lower():
        return "muffed catch"
    else:
        out = "Unknown turnover type: '" + turnover_string + "'"
        print(out)
        return None


def get_turnover_recoverer(turnover_string):
    """Takes a string describing the play, and returns the player that
    recovered the turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.

    returns:
        A string indicating the player's name, or False if the ball was
            not recovered.
    """
    # Use the type to set the string to split on
    to_type = get_turnover_type(turnover_string)
    if to_type == "fumble":
        # Check to see if the fumble is recovered (some are fumbled out of
        # bounds for instance)
        if "recovered" not in turnover_string:
            return False
        r_split_string = "recovered by"
        l_split_string = " at "
    elif to_type == "interception":
        r_split_string = "intercepted by"
        l_split_string = " at "
    elif to_type == "muffed catch":
        r_split_string = "recovered by"
        l_split_string = " and "
    else:  # Unknown case, we can't do anything
        return None
    # Now split the string
    r_string = turnover_string.split(r_split_string)[1].strip()
    l_string = r_string.split(l_split_string)[0].strip()
    return l_string


def get_turnover_committer(turnover_string):
    """Takes a string describing the play, and returns the player that
    committed the turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.

    returns:
        A string indicating the player's name.
    """
    # Use the type to set the string to split on
    to_type = get_turnover_type(turnover_string)
    r_split_string = None
    if to_type == "fumble":
        l_split_string = "fumbles"
    elif to_type == "interception":
        l_split_string = "pass incomplete"
    elif to_type == "muffed catch":
        l_split_string = ", recovered by"
        r_split_string = "muffed catch by"
    else:  # Unknown case, we can't do anything
        return None
    # Now split the string
    l_string = turnover_string.split(l_split_string)[0].strip()
    if r_split_string:
        r_string = l_string.split(r_split_string)[1].strip()
        return r_string
    else:
        return l_string


def get_turnover_teams(turnover_string, home_players, away_players):
    """Takes a string describing the play, and returns the teams that lost and
    recovered the turnover.

    args:
        turnover_string: A string about the turnover, as returned by
            split_turnovers.
        home_players, away_players: Iterables that support 'in' containing a
            list of all players on the home and away team, respectively.

    returns:
        A tuple of (committing_team, recovering_team) with values "home",
            "away". False is used for the recovering team if there is no
            recovering team (for example, when the ball is fumbled out the end
            zone for a safety).
    """
    com = get_turnover_committer(turnover_string)
    rec = get_turnover_recoverer(turnover_string)
    com_uniq_home = (com in home_players and com not in away_players)
    com_uniq_away = (com in away_players and com not in home_players)
    rec_uniq_home = (rec in home_players and rec not in away_players)
    rec_uniq_away = (rec in away_players and rec not in home_players)
    # With an interception, we only need to get one team, because we know the
    # other by the fact that an interception only happens when possession
    # changes.
    if get_turnover_type(turnover_string) == "interception":
        if com_uniq_home or rec_uniq_away:
            return ("home", "away")
        elif com_uniq_away or rec_uniq_home:
            return ("away", "home")
    # Fumbles can be recovered by the same team, so we need both
    else:
        error_text = ""

        com_team = None
        if com_uniq_home:
            com_team = "home"
        elif com_uniq_away:
            com_team = "away"
        else:
            error_text += "\tTurnover committing player '"
            error_text += str(com) + "' not recognized!"

        # False is used to indicate that there is no recovering player
        if rec is not False:
            rec_team = None
            if rec_uniq_home:
                rec_team = "home"
            elif rec_uniq_away:
                rec_team = "away"
            else:
                error_text += "\tTurnover recovering player '"
                error_text += str(rec) + "' not recognized!"
        else:
            rec_team = False

        if error_text:
            print(error_text)

        return (com_team, rec_team)
