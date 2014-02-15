#!/usr/bin/env python3

from time import strptime, strftime
from datetime import datetime
from data_helpers.team_list import names_to_code


def convert_time(time_string):
    """Takes in a string of the form 9:32pm and returns 21:32.

    args:
        time_string: A string of format type '%I:%M%p'

    returns:
        A string of the format '%H:%M'.

    raises:
        ValueError if the input format is wrong.
    """
    # Thankfully the time module handles this case perfectly
    time_object = strptime(time_string, "%I:%M%p")
    return strftime("%H:%M", time_object)


def convert_duration(time_string):
    """Takes in a string of the form 4:11 and returns the number of seconds
    (15060).

    args:
        time_string: A string of format type '%H:%M'

    returns:
        A integer of the number of seconds.

    raises:
        ValueError if the input format is wrong.
    """
    # We use datetimes, a little overkill, but better than trying to parse on
    # our own. strptime returns hours and minutes from 1900-1-1:0:00, so we
    # subtract that off to get a timedelta.
    delta = datetime.strptime(time_string, "%H:%M") - datetime(1900, 1, 1, 0, 0)
    return delta.seconds


def convert_weather(weather_string):
    """Takes in a string describing the weather and returns a dictionary of the
    information.

    args:
        weather_string: A string detailing the weather

    returns:
        A dictionary as follows:
            {
                "temperature": 35,
                "relative humidity": 0.59,
                "wind speed": 10,
                "wind chill": 27
            }

            Where the units are, in order, Fahrenheit, unitless [0-1], miles
            per hour, and Fahrenheit. Any missing value is replaced with None.
            Returns just None if all values are None.

    raises:
        ValueError: If one of the numbers can not be converted to an integer.
    """
    # The dictionary we will return, we pre-fill it with None so that we only
    # have to set values if we find them
    out_dict = {
            "temperature": None,
            "relative humidity": None,
            "wind speed": None,
            "wind chill": None
            }
    # All quantities of interest are set off by commas, we go through each and
    # try to pull out the relevant data. If we can't match we just continue.
    split_string = weather_string.split(',')
    for string in split_string:
        if "degrees" in string:
            out_dict["temperature"] = int(string.split()[0])
        elif "wind chill" in string:
            out_dict["wind chill"] = int(string.split()[-1])
        elif "relative humidity" in string:
            percent = string.split()[-1].strip('%')
            out_dict["relative humidity"] = float(percent) / 100.
        elif "mph" in string:
            out_dict["wind speed"] = int(string.split()[1])
        elif "no wind" in string:
            out_dict["wind speed"] = 0
    # If all values are None, we return just None, otherwise we return the
    # dictionary
    all_none = False
    for value in out_dict.values():
        if value is not None:
            return out_dict
    # All values are None, so return None
    return None


def convert_overunder(ou_string):
    """Takes in a string of the form 44.5 (over) and returns a float.

    args:
        ou_string: A string of format type "float (over/under)", can also
            handle "float(over/under)". The over/under is ignored, it is
            redundant information about the outcome of the game.

    returns:
        A positive float.

    raises:
        ValueError if the input format is wrong.
    """
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '+']
    num = ""
    # We look through the string and pull out the number, but only if it is at
    # the start
    for char in ou_string:
        if char in chars:
            num += char
        else:
            break
    # If num isn't empty, return, else raise
    if num:
        return float(num)
    else:
        raise ValueError


def convert_vegas_line(vl_string):
    """Takes in a string of the form Denver Broncos -9.0 and returns a tuple of
    the team code and line: ("DEN", -9.0)

    args:
        vl_string: A string of the format "Full Team Name -float" or "Pick"

    returns:
        A tuple with the team code and the spread, or None and 0 if "Pick".

    raises:
        KeyError if the team name is wrong.
        IndexError if the input is missing the minus sign.
        ValueError if the number can't be parsed by int().
    """
    # Pick is used when
    if "Pick" in vl_string:
        return (None, 0.)
    else:
        team_name = vl_string.split('-')[0].strip()
        line = -1 * float(vl_string.split('-')[1].strip())
        team_code = names_to_code[team_name]
        return (team_code, line)


def convert_stadium(stadium_string):
    """Takes in a string of the form Metrodome (dome) and returns a tuple of
    the name and dome status.

    args:
        stadium_string: A string of the format "Stadium Name (dome)" with
            "(dome)" optional.

    returns:
        A tuple with the stadium name, and true/false for the dome.

    raises:
        ValueError if their is no name given.
        TypeError if vanue_string is not a string.
    """
    if not isinstance(stadium_string, str):
        raise TypeError
    # Pick is used when
    dome = False
    if "(dome)" in stadium_string:
        dome = True
        stadium_string = (stadium_string.replace("(dome)", '')).strip()
    if stadium_string:
        return (str(stadium_string), dome)
    else:
        raise ValueError
