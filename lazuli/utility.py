"""This module holds the utility functions and constants for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""


def get_key(dictionary, val):
    """Generic function to return the key for a given value

    Iterates through the dictionary, comparing values to see if it matches the desired value.
    If so, return the corresponding key. If no matches are found by the end, return False.
    This function short-circuits (i.e. returns with the first match found).
    Note: OrderedDict is no longer necessary for this as of Python 3.6, as order is preserved automagically.

    Args:
        dictionary: Dictionary, representing the dictionary to be searched
        val: Var, representing the desired/target value to search for

    Returns:
        Var, representing the corresponding key (if any); defaults to False, if none are found

    Raises:
        Generic error for any failures
    """
    try:
        for key, value in dictionary.items():
            if val == value:
                return key
        print("No corresponding key found")
        return False
    except Exception as e:
        print(f"Unexpected error encountered whilst attempting to perform dictionary search: {e}")
        return False


# Dictionary that maps inventory tabs' names to their corresponding index in the DB/source
map_inv_types = {
    'equipped': -1,
    'equip': 1,
    'eqp': 1,
    'use': 2,  # Default name for Lazuli purposes
    'consume': 2,  # name in WZ
    'etc': 4,
    'setup': 3,  # Default name for Lazuli purposes
    'install': 3,  # name in WZ
    'cash': 5
}
