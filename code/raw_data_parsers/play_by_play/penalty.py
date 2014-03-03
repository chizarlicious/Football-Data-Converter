#!/usr/bin/env python3


def split_penalties(col):
    """Takes a string describing the play, and splits it into a list of the
    penalties.

    args:
        col: A string describing the play.

    returns:
        A list of strings.
    """
    # 'Penalty on' is common to all the strings, and marks the start of one, so
    # we split on this and then add it back before returning
    s_list = col.split("Penalty on")
    out_list = []
    for line in s_list[1:]:
        out_list.append("Penalty on" + line)
    return out_list


def get_penalty_team(
        penalty_string,
        home_team,
        away_team,
        home_players,
        away_players
        ):
    """Takes a string describing the penalty and returns "home" or "away" for
    the committing team.

    args:
        penalty_string: A string about the penalty, as returned by
            split_penalties.
        home_team, away_team: The team code for the home and away team,
            respectively.
        home_players, away_players: Iterables that support 'in' containing a
            list of all players on the home and away team, respectively.

    returns:
        "home" or "away"
    """
    infractor = penalty_string.split("Penalty on")[1].split(":")[0].strip()
    if infractor == home_team or infractor in home_players:
        return "home"
    elif infractor == away_team or infractor in away_players:
        return "away"
    else:
        print(infractor)


def get_penalty_player(penalty_string, home_team, away_team):
    """Takes a string describing the penalty and returns the name of the player
    that committed the penalty.

    args:
        penalty_string: A string about the penalty, as returned by
            split_penalties.
        home_team, away_team: The team code for the home and away team,
            respectively.

    returns:
        The name, or "team" if it is a team penalty.
    """
    infractor = penalty_string.split("Penalty on")[1].split(":")[0].strip()
    if infractor == home_team or infractor == away_team:
        return "team"
    else:
        return infractor


def get_penalty_yards(penalty_string):
    """Takes a string describing the penalty and returns the amount of yards
    assessed.

    args:
        penalty_string: A string about the penalty, as returned by
            split_penalties.

    returns:
        An integer indicating the number of yards, or None if the penalty was
            declined.

    raises:
        ValueError if the word before yards is not an int.
    """
    # If the penalty is "declined" then no yards are counted.
    if "declined" in penalty_string.lower():
        return None
    # We find the last instance of the word "yards" and then the item before it
    # is the yardage. We use the last instance because some penalties have
    # multiple severities, and these are listed as "Penalty Name (15 yards),
    # 15 yards".
    s_string = penalty_string.split()
    s_string.reverse()
    for i in range(len(s_string)):
        if s_string[i] == "yards" or s_string[i] == "yards,":
            return int(s_string[i + 1])


def get_penalty_type(penalty_string):
    """Takes a string describing the penalty and returns whether it was
    declined, and if there is no play.

    args:
        penalty_string: A string about the penalty, as returned by
            split_penalties.

    returns:
        "no play" if accepted and the play was voided, "declined" if the play
        was declined, "accepted" otherwise.
    """
    if "declined" in penalty_string.lower():
        return "declined"
    elif "no play" in penalty_string.lower():
        return "no play"
    else:
        return "accepted"


def get_penalty_name(penalty_string):
    """Takes a string describing the penalty and returns the name.

    args:
        penalty_string: A string about the penalty, as returned by
            split_penalties.

    returns:
        A string indicating the penalty name.
    """
    first_split = penalty_string.split(':')[1].strip()
    # Most names end with a ',', but if they are declined then they end with
    # (Declined).
    if "declined" in first_split.lower():
        return first_split.split("(Declined)")[0].strip()
    else:
        return first_split.split(",")[0].strip()
