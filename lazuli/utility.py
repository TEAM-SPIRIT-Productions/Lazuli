"""This module holds the utility functions and constants for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""


# Generic function to return the key for a given value
# Returns False if no key is found
def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key
    print("No corresponding key found")
    return False


# Dictionary that maps inventory tab name to their corresponding index in the DB/source
inv_types = {
    'equipped': -1,
    'equip': 1,
    'eqp': 1,
    'use': 2,
    'consume': 2,
    'etc': 4,
    'setup': 3,
    'install': 3,
    'cash': 5
}
