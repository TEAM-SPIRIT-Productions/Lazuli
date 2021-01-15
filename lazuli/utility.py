"""This module holds the utility functions and constants for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con

# CONSTANTS -------------------------------------------------------------------
# Dictionary that maps inventory tabs' names to
# their corresponding index in the DB/source
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


# UTILITY FUNCTIONS -----------------------------------------------------------
def get_key(dictionary, val):
	"""Generic function to return the key for a given value

	Iterates through the dictionary, comparing values to see if it matches
	the desired value. If so, return the corresponding key. If no matches are
	found by the end, return False.
	This function short-circuits (i.e. returns with the first match found).
	Note: OrderedDict is no longer necessary for this as of Python 3.6,
	as order is preserved automagically.

	Args:
		dictionary: Dictionary, representing the dictionary to be searched
		val: Var, representing the desired/target value to search for

	Returns:
		Var, representing the corresponding key (if any)
		Defaults to False, if none are found

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
		print(
			f"Unexpected error encountered whilst attempting "
			f"to perform dictionary search:\n{e}"
		)
		return False


def get_db_all_hits(config, query):
	"""Generic function for fetching all matching data from the DB

	Generic top level function for fetching all matching data from DB,
	using the provided DB config and query

	Args:
		config: Dictionary, representing database config attributes
		query: String, representing SQL query

	Returns:
		List of objects, representing the result of the provided SQL query,
		using the provided DB connection attributes

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
			port=config['port'],
			charset=config['charset']
		)
		cursor = database.cursor(dictionary=True)
		cursor.execute(query)
		data = cursor.fetchall()
		database.disconnect()

		return data

	except Exception as e:
		print(
			f"CRITICAL: Error encountered whilst attempting "
			f"to connect to the database! \n{e}"
		)


def get_db_first_hit(config, query):
	"""Generic function for fetching the first result from DB

	This function grabs the first hit from get_db_all_hits;
	errors handled in get_db_all_hits.

	Args:
		config: Dictionary, representing database config attributes
		query: String, representing SQL query

	Returns:
		Var, representing first result
	"""
	return get_db_all_hits(config, query)[0]


def get_stat_by_column(data, column):
	"""Fetches dictionary attribute by key (wrapper)

	Args:
		data: Dictionary, representing account or character attributes
		column: String, representing column name in DB

	Returns:
		Int or String, representing user attribute queried

	Raises:
		Generic error on failure
	"""
	try:
		return data[column]
	except Exception as e:
		print(
			f"ERROR: Unable to extract the given column for table users.\n{e}"
		)


def write_to_db(config, query):
	"""Performs write operations to DB using the provided DB config and query

	Args:
		config: Dictionary, representing database config attributes
		query: String, representing SQL query

	Returns:
		A Boolean representing whether the operation was successful

	Raises:
		SQL Error 2003: Can't connect to DB
		WinError 10060: No response from DB
		List index out of range: Wrong column name
	"""
	try:
		database = con.connect(
			host=config['host'],
			user=config['user'],
			password=config['password'],
			database=config['schema'],
			port=config['port'],
			charset=config['charset']
		)

		cursor = database.cursor(dictionary=True)
		cursor.execute(query)
		database.commit()
		database.disconnect()
		return True
	except Exception as e:
		print(f"ERROR: Unable to set stats in database.\n{e}")
		return False


def get_inv_type_by_name(inv_string):
	inv_type = map_inv_types.get(inv_string)
	return inv_type


def get_inv_name_by_type(inv_type):  # Never used
	inv_name = get_key(map_inv_types, inv_type)
	return inv_name


def has_item_in_inv_type(inv_type, item_id):
	"""Checks whether the particular tab of the inventory has an item

	Generic top level function used by Inventory::has_item_in_XXX() methods,
	and the Inventory::is_equipping() method. Iterates through the dictionary
	of items associated with the specified tab, and check if
	the provided item ID can be found as a value.

	Args:
		inv_type: Inventory object, representing inventory tab to search
		item_id: Int, representing the ID of the item to search for

	Returns:
		Boolean, representing whether the specified item was found
	"""
	for bag_index in inv_type:
		if inv_type[bag_index]['itemid'] == item_id:
			return True
	return False


def extract_name(player_list):
	"""Extracts a list of players from SQL data, via the name column

	Args:
		player_list: List of Dictionaries, representing list of all players

	Returns:
		List of Strings, representing player names
	"""
	if not player_list[0]['name']:  # if empty or null; sanity check
		raise RuntimeError("No players found!")

	else:
		players = []
		# player_list contains unnecessary data
		for player in player_list:
			players.append(player['name'])  # Only retrieve name
		return players


def extract_name_and_value(player_list, column):
	"""Extracts a list of players and their corresponding attribute

	Extracts a list of players and their corresponding attribute value from
	SQL data, via the name column and another provided column

	Args:
		player_list: List of Dictionaries, representing list of all players
		column: String, representing column name to extract

	Returns:
		List of Tuples, representing player names and
		their corresponding values (e.g. level)
	"""
	if not player_list[0]['name']:  # if empty or null; sanity check
		raise RuntimeError("No such players found!")

	else:
		players = []
		# player_list contains unnecessary data
		for player in player_list:
			players.append((player['name'], player[column]))
			# Only retrieve (name, value)
			# List of Tuples, as per Brandon's request
		return players
