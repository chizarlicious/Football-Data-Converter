#!/usr/bin/env python3

from time import strptime, strftime


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
