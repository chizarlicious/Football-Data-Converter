#!/usr/bin/env python3


def split_on_dashes(dash_string):
    """Takes a string of numbers separated by '-' and splits it, assuming that
    '--' means a separator followed by a negative number.

    args:
        dash_string: A string of items separated by '-', with a '--' indicated
        a negative on the item following.

    returns:
        A tuple of strings.
    """
    out_list = dash_string.split('-')

    to_neg = []
    # Find all the '' entries created by splitting "--". Mark the next entry in
    # the list as negative.
    for i in range(len(out_list)):
        if not out_list[i] and not (i >= (len(out_list) - 1)):
            to_neg.append(i + 1)
    # Add a negative to marked entries
    for i in to_neg:
        out_list[i] = '-' + out_list[i]
    # Remove blank entries (which count as False for if tests) and '-' entries
    final_out_list = [x for x in out_list if (x and x != '-')]

    return tuple(final_out_list)


def convert_rush_info(rush_string):
    """Takes a string of rushing statistics and returns a dictionary.

    args:
        rush_string: A string in the following format 'Rush-yards-TDs'

    returns:
        A dictionary of the form:  {"plays": 16, "yards": 34, "touchdowns": 0}.

    raises:
        ValueError if the input can not be converted sensibly
    """
    rush_split = split_on_dashes(rush_string)
    plays = int(rush_split[0])
    yards = int(rush_split[1])
    touchdowns = int(rush_split[2])
    return {"plays": plays, "yards": yards, "touchdowns": touchdowns}


def convert_pass_info(pass_string):
    """Takes a string of passing statistics and returns a dictionary.

    args:
        pass_string: A string in the following format 'Comp-Att-Yd-TD-INT'

    returns:
        A dictionary of the form:
                {"plays": 18, "yards": 331, "touchdowns": 3,
                "interceptions": 0, "successful": 18}

    raises:
        ValueError if the input can not be converted sensibly
    """
    pass_split = split_on_dashes(pass_string)
    successful = int(pass_split[0])
    plays = int(pass_split[1])
    yards = int(pass_split[2])
    touchdowns = int(pass_split[3])
    interceptions = int(pass_split[4])
    return {"plays": plays, "yards": yards, "touchdowns": touchdowns,
            "interceptions": interceptions, "successful": successful}


def convert_sack_info(sack_string):
    """Takes a string of sack statistics and returns a dictionary.

    args:
        sack_string: A string in the following format 'Sacked-yards'

    returns:
        A dictionary of the form: {"plays": 1, "yards": -7}

    raises:
        ValueError if the input can not be converted sensibly
    """
    sack_split = split_on_dashes(sack_string)
    plays = int(sack_split[0])
    yards = -int(sack_split[1])
    return {"plays": plays, "yards": yards}


def convert_fumble_info(fumble_string):
    """Takes a string of fumble statistics and returns a dictionary.

    args:
        fumble_string: A string in the following format 'Fumbles-lost'

    returns:
        A dictionary of the form: {"plays": 2, "lost": 1}

    raises:
        ValueError if the input can not be converted sensibly
    """
    fumble_split = split_on_dashes(fumble_string)
    plays = int(fumble_split[0])
    lost = int(fumble_split[1])
    return {"plays": plays, "lost": lost}


def convert_penalty_info(penalty_string):
    """Takes a string of penalty statistics and returns a dictionary.

    args:
        penalty_string: A string in the following format 'Penalties-yards'

    returns:
        A dictionary of the form: {"plays": 2, "yards": -15}

    raises:
        ValueError if the input can not be converted sensibly
    """
    penalty_split = split_on_dashes(penalty_string)
    plays = int(penalty_split[0])
    yards = -int(penalty_split[1])
    return {"plays": plays, "yards": yards}
