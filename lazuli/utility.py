"""This module holds the utility functions and constants for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con

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


def get_inv_type_by_name(inv_string):
    inv_type = map_inv_types.get(inv_string)
    return inv_type


def get_inv_name_by_type(inv_type):  # Never used
    inv_name = get_key(map_inv_types, inv_type)
    return inv_name


def get_db_first_hit(config, query):
    """Generic top level function for fetching data (first hit) from DB using the provided DB config and query

    This method assumes that only one result is found - it always defaults to the first result.
    An effort has been made to convert this to a decorator so that it may also be applied to
    Character::set_stat_by_column() & Character::get_user_id(), which ultimately ended in failure.

    Args:
        config: dictionary, representing database config attributes
        query: String, representing SQL query

    Returns:
        String representing the result of the provided SQL query, using the provided DB connection attributes

    Raises:
        SQL Error 2003: Can't cannect to DB
        WinError 10060: No response from DB
        List index out of range: Wrong column name
        Generic error as a final catch-all
    """
    try:
        database = con.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['schema'],
            port=config['port']
        )
        cursor = database.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()[0]
        database.disconnect()

        return data

    except Exception as e:
        print("CRITICAL: Error encountered whilst attempting to connect to the database! \n", e)


def get_db_all_hits(config, query):
    """Generic top level function for fetching all matching data from DB using the provided DB config and query

    Args:
        config: dictionary, representing database config attributes
        query: String, representing SQL query

    Returns:
        List of objects, representing the result of the provided SQL query, using the provided DB connection attributes

    Raises:
        SQL Error 2003: Can't cannect to DB
        WinError 10060: No response from DB
        List index out of range: Wrong column name
        Generic error as a final catch-all
    """
    try:
        database = con.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['schema'],
            port=config['port']
        )
        cursor = database.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        database.disconnect()

        return data

    except Exception as e:
        print("CRITICAL: Error encountered whilst attempting to connect to the database! \n", e)


def has_item_in_inv_type(inv_type, item_id):
    """Checks whether the particular tab of the inventory has an item

    Generic top level function used by Inventory::has_item_in_XXX() methods, and the
    Inventory::is_equipping() method.
    Iterates through the dictionary of items associated with the specified tab, and check if
    the provided item ID can be found as a value.

    Args:
        inv_type: inventory object, representing inventory tab to search
        item_id: int, representing the ID of the item to search for

    Returns:
        Boolean, representing whether the specified item was found
    """
    for bag_index in inv_type:
        if inv_type[bag_index]['itemid'] == item_id:
            return True
    return False
