"""This module holds the utility functions and constants for the lazuli package.

Copyright 2022 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to `database.py` or the project wiki on GitHub for usage examples.
"""
from typing import Any
import mysql.connector as con

# CONSTANTS -------------------------------------------------------------------
# Dictionary that maps inventory tabs' names to
# their corresponding index in the DB/source
MAP_INV_TYPES = {
	'equipped': -1,
	'equip': 1,
	'eqp': 1,
	'use': 2,  # Default name for Lazuli purposes
	'consume': 2,  # name in WZ
	'etc': 4,
	'setup': 3,  # Default name for Lazuli purposes
	'install': 3,  # name in WZ
	'cash': 5,
}


# UTILITY FUNCTIONS -----------------------------------------------------------
def get_key(dictionary: dict, val: Any) -> Any:
	"""Generic function to return the key for a given value

	Iterates through the dictionary, comparing values to see if it matches
	the desired value. If so, return the corresponding key. If no matches are
	found by the end, return `False`.
	This function short-circuits (i.e. returns with the first match found).
	Note: OrderedDict is no longer necessary for this as of Python 3.6,
	as order is preserved automagically.
	Note2: This function does not check whether the value type provided matches 
	with the type of the value in the provided dictionary.

	Args:

		dictionary (`dict`): Represents the dictionary to be searched
		val (`any`): Represents the desired/target value to search for

	Returns:
		A variable of `any` type, representing the corresponding key (if any).
		Defaults to `False`, if none are found.

	Raises:
		A generic error for any failures
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


def get_db_all_hits(config: dict[str, str], query: str) -> list:
	"""Generic function for fetching all matching data from the DB

	Generic top level function for fetching all matching data from DB,
	using the provided DB config and query

	Args:

		config (`dict`): Represents the database config attributes
		query (`str`): Represents the SQL query to execute

	Returns:
		A `list` of objects, representing the result of the provided SQL query,
		using the provided DB connection attributes

	Raises:
		SQL Error 2003: Can't connect to DB
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


def get_db_first_hit(config: dict[str, str], query: str) -> Any:
	"""Generic function for fetching the first result from DB

	This function grabs the first hit from `get_db_all_hits`;
	errors handled in `get_db_all_hits`.

	Args:

		config (`dict`): Represents the database config attributes
		query (`str`): Represents the SQL query to execute

	Returns:
		A variable of `any` type, representing first result
	"""
	return get_db_all_hits(config, query)[0]


def get_stat_by_column(data: dict[str, Any], column: str) -> Any:
	"""Fetches dictionary attribute by key (wrapper)

	Args:

		data (`dict`): Represents the account or character attributes
		column (`str`): Represents the column name in DB

	Returns:
		An `int` or `str`, representing user attribute queried

	Raises:
		A generic error on failure
	"""
	try:
		return data[column]
	except Exception as e:
		print(
			f"ERROR: Unable to extract the given column for table users.\n{e}"
		)


def write_to_db(config: dict[str, str], query: str) -> bool:
	"""Performs write operations to DB using the provided DB config and query

	### CAN ONLY BE SET WHEN SERVER IS OFF!

	Args:

		config (`dict`): Represents the database config attributes
		query (`str`): Represents the SQL query to execute

	Returns:
		A `bool` representing whether the operation was successful

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


def get_inv_type_by_name(inv_string: str) -> int:
	"""`int`: Encode an inventory type using its common name"""
	inv_type = MAP_INV_TYPES.get(inv_string)
	return inv_type


def get_inv_name_by_type(inv_type: int) -> str:  # Never used
	"""`str`: Decode an inventory type using from its value"""
	inv_name = get_key(MAP_INV_TYPES, inv_type)
	return inv_name


def extract_name(player_list: list[dict[str, Any]]) -> list[str]:
	"""Extracts a `list` of players from SQL data, via the name column

	Args:

		player_list (`list[dict]`): Represents a list of all players

	Returns:
		A `list` of `str`, representing player names

	Raises:
		RuntimeError: Improperly formatted or empty player list
	"""
	if not player_list[0]['name']:  # if empty or null; sanity check
		raise RuntimeError("No players found!")

	else:
		players = []
		# player_list contains unnecessary data
		for player in player_list:
			players.append(player['name'])  # Only retrieve name
		return players


def extract_name_and_value(
	player_list: list[dict[str, Any]],
	column: str,
) -> list[tuple[str, Any]]:
	"""Extracts a `list` of players and their corresponding attribute

	Extracts a `list` of players and their corresponding attribute value from
	SQL data, via the name column and another provided column

	Args:

		player_list (`list[dict]`): Represents a list of all players
		column (`str`): Represents the column name to extract

	Returns:
		A `list` of `tuple`, representing player names and
		their corresponding values (e.g. level)

	Raises:
		RuntimeError: Improperly formatted or empty player list
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
