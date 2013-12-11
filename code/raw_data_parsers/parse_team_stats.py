#!/usr/bin/env python3


def convert_rush_info(rush_string):
    """Takes a string of rushing statistics and returns a dictionary.

    args:
        rush_string: A string in the following format 'Rush-yards-TDs'

    returns:
        A dictionary of the form:  {"plays": 16, "yards": 34, "touchdowns": 0}.
        Failure returns None.
    """
    rush_split = rush_string.split('-')
    # Try to convert all to ints
    try:
        plays = int(rush_split[0])
        yards = int(rush_split[1])
        touchdowns = int(rush_split[2])
    except ValueError:  # Not an int!
        return None
    else:
        return {"plays": plays, "yards": yards, "touchdowns": touchdowns}


def convert_pass_info(pass_string):
    """Takes a string of passing statistics and returns a dictionary.

    args:
        pass_string: A string in the following format 'Comp-Att-Yd-TD-INT'

    returns:
        A dictionary of the form:
                {"plays": 18, "yards": 331, "touchdowns": 3,
                "interceptions": 0, "successful": 18}
            Failure returns None.
    """

def convert_sack_info(sack_string):
    """Takes a string of sack statistics and returns a dictionary.

    args:
        sack_string: A string in the following format 'Sacked-yards'

    returns:
        A dictionary of the form: {"plays": 1, "yards": -7}
            Failure returns None.
    """

def convert_fumble_info(fumble_string):
    """Takes a string of fumble statistics and returns a dictionary.

    args:
        fumble_string: A string in the following format 'Fumbles-lost'

    returns:
        A dictionary of the form: {"plays": 2, "lost": 1}
            Failure returns None.
    """

def convert_penalty_info(penalty_string):
    """Takes a string of penalty statistics and returns a dictionary.

    args:
        penalty_string: A string in the following format 'Penalties-yards'

    returns:
        A dictionary of the form: {"plays": 2, "yards": -15}
            Failure returns None.
    """
