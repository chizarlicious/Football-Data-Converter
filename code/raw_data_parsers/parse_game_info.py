#!/usr/bin/env python3


def convert_time(time_string):
    """Takes in a string of the form 9:32pm and returns 21:32.

    args:
        time_string: A string of format type '%I:%M%p'

    returns:
        None if no sensible conversion exits, otherwise returns a string of the
            format '%H:%M'
    """

def convert_weather(weather_string):
    """Takes in a string describing the weather and returns a dictionary of the
    information.

    args:
        weather_string: A string detailing the weather

    returns:
        A dictionary with keys: ["temperature", "relative humidity", "wind
            speed", "wind chill"] in Fahrenheit and miles per hour. Relative
            humidity is a number [0., 1.]. Any missing value is replaced with
            None. On failure, returns None instead of a dictionary.
    """
