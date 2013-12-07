#!/usr/bin/env python3


def convert_time(time_string):
    """Takes in a string of the form 9:32pm and returns 21:32.

    args:
        time_string: A string of format type '%I:%M%p'

    returns:
        None if no sensible conversion exits, otherwise returns a string of the
        format '%H:%M'
    """
