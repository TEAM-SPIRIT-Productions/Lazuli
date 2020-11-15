"""This module holds the Account class for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con


class Account:
	"""Account object; models AzureMS accounts.

	Using instance method Lazuli::get_account_by_username(username) or the Lazuli::get_char_by_name(name).account getter
	will create an Account object instance with attributes identical to the account with username "username"
	(or IGN "name" for the latter) in the connected AzureMS-based database.
	This class contains the appropriate getter and setter methods for said attributes.

	Attributes:
		TO BE ADDED
	"""
	def __init__(self, account_info, database_config):
		"""Emulates how account object is handled server-sided

		Args:
			account_info: dictionary of user attributes, formatted in AzureMS style
			database_config: dictionary of protected attributes from a Lazuli object
		"""

		self._account_info = account_info
		self._database_config = database_config

		self._account_id = 0  # Primary Key - Do NOT set
		self._username = ""  # varchar(64)
		self._logged_in = 0  # int(1) and not bool for some reason
		self._banned = 0  # int(1) and not bool for some reason
		self._ban_reason = ""  # text
		# self._gm = 0  # There are conflicting values in character and accounts - ignored for now
		self._nx = 0
		self._maple_points = 0
		self._vp = 0
		self._dp = 0
		self._char_slots = 0

		self.init_account_stats()

	def init_account_stats(self):
		"""Given a dictionary of stats from AzureMS's DB we add them to Account object's attributes

		Runs near the end of Account::__init__(account_info, database_config).
		It assigns the account attributes in account_info to their respective protected attributes belonging to
		the Account object instance.
		"""
		self._account_id = self._account_info['id']
		self._username = self._account_info['name']
		self._logged_in = self._account_info['loggedin']
		self._banned = self._account_info['banned']
		self._ban_reason = self._account_info['banreason']
		# self._gm = self._account_info['gm']  # There are conflicting values in character and accounts - ignored for now
		self._nx = self._account_info['nxCash']
		self._maple_points = self._account_info['mPoints']
		self._vp = self._account_info['vpoints']
		self._dp = self._account_info['realcash']  # Best guess - Might be wrong!
		self._char_slots = self._account_info['chrslot']

	@property
	def account_info(self):
		return self._account_info

	@property
	def database_config(self):
		return self._database_config

	@property
	def account_id(self):
		return self._account_id  # Primary Key; DO NOT set

	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, new_name):
		self.set_stat_by_column("name", new_name)
		self._username = new_name

	@property
	def logged_in(self):
		return self._logged_in

	@logged_in.setter
	def logged_in(self, value):
		self.set_stat_by_column("loggedin", value)  # Use with caution!
		self._logged_in = value

	@property
	def banned(self):
		return self._banned

	@banned.setter
	def banned(self, value):
		self.set_stat_by_column("banned", value)  # Use with caution!
		self._banned = value

	@property
	def ban_reason(self):
		return self._ban_reason

	@ban_reason.setter
	def ban_reason(self, value):
		self.set_stat_by_column("banreason", value)
		self._ban_reason = value

	@property
	def nx(self):
		return self._nx

	@nx.setter
	def nx(self, value):
		self.set_stat_by_column("nxCash", value)
		self._nx = value

	@property
	def maple_points(self):
		return self._nx

	@maple_points.setter
	def maple_points(self, value):
		self.set_stat_by_column("mPoints", value)
		self._maple_points = value

	@property
	def vp(self):
		return self._vp

	@vp.setter
	def vp(self, value):
		self.set_stat_by_column("vpoints", value)
		self._vp = value

	@property
	def dp(self):
		return self._dp

	@dp.setter
	def dp(self, value):
		self.set_stat_by_column("realcash", value)
		self._dp = value

	@property
	def char_slots(self):
		return self._char_slots

	@char_slots.setter
	def char_slots(self, value):
		self.set_stat_by_column("chrslot", value)
		self._char_slots = value

	def get_stat_by_column(self, column):
		"""Fetches account attribute by column name

		Returns:
			Int or String, representing user attribute queried
		Raises:
			Generic error on failure
		"""
		try:
			return self.account_info[str(column)]
		except Exception as e:
			print("[ERROR] Error trying to obtain the given column for table users.", e)

	def set_stat_by_column(self, column, value):
		"""Sets a account's attributes by column name in database

		Grabs the database attributes provided through the class constructor.
		Uses these attributes to attempt a database connection.
		Attempts to update the field represented by the provided column in the accounts table, with the provided value.
		Not recommended to use this alone, as it won't update the account object which this was used from

		Args:
			value: int or string, representing the value to be set in the database
			column: string, representing the column in the database that is to be updated

		Returns:
			A boolean representing whether the operation was successful.

		Raises:
			SQL Error 2003: Can't cannect to DB
			WinError 10060: No response from DB
			List index out of range: Wrong column name
		"""
		host = self._database_config["host"]
		user = self._database_config["user"]
		password = self._database_config["password"]
		schema = self._database_config["schema"]
		port = self._database_config["port"]

		try:
			database = con.connect(host=host, user=user, password=password, database=schema, port=port)

			cursor = database.cursor(dictionary=True)
			cursor.execute(f"UPDATE accounts SET {column} = '{value}' WHERE id = '{self.account_id}'")
			database.commit()
			print(f"Successfully updated {column} value for user id: {self.account_id}.")
			self._account_info[column] = value  # Update the stats in the dictionary
			database.disconnect()
			return True
		except Exception as e:
			print("[ERROR] Error trying to set stats in database.", e)
			return False
