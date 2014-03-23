#!/usr/bin/env python3

import re


def get_challenge_type(play_string):
    """Takes a string describing the play and returns the type of challenge.

    args:
        play_string: A string describing the play.

    returns:
        One of:
            "upheld", "overturned", or False (if not a challenge play)
    """
    if "challenged" not in play_string:
        return False
    elif "upheld" in play_string:
        return "upheld"
    elif "overturned" in play_string:
        return "overturned"


def remove_challenge(play_string):
    """Takes a string describing the play, and removes the information about
    any challenges, returning only the part of the play that was upheld.

    args:
        play_string: A string describing the play.

    returns:
        A string describing the play.
    """
    challenge_type = get_challenge_type(play_string)
    if not challenge_type:  # Not a challenge, do nothing
        return play_string
    elif challenge_type == "upheld":
        # We split on something that looks like:
        # team code + challenged, or "Replay Assistant challenged"
        split_regex = "[A-Z][A-Z][A-Z] challenged|Replay Assistant challenged"
        return re.split(split_regex, play_string)[0].strip()
    else:
        return play_string.split("overturned.")[1].strip()
