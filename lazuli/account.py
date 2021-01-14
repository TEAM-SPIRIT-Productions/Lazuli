"""This module holds the Account class for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""

import lazuli.utility as utils


class Account:
	"""Account object; models AzureMS accounts.

	Using instance method Lazuli::get_account_by_username(username) or
	the Lazuli::get_char_by_name(name).account getter will create an
	Account object instance with attributes identical to the account
	with username "username" (or IGN "name" for the latter) in
	the connected AzureMS-based database. This class contains the
	appropriate getter and setter methods for said attributes.

	Attributes:
		account_id:
			Integer, representing Primary Key for account - Do NOT set manually
		username:
			String, representing account username; varchar(64)
		logged_in:
			Integer, represents login status of the account;
			int(1) and not bool for some reason
		banned:
			Integer, represents ban status of the account;
			int(1) and not bool for some reason
		ban_reason:
			String, representing account ban reason; text
		nx:
			Integer, representing the amount of NX Prepaid the user has
		maple_points:
			Integer, representing the amount of Maple Points the user has
		vp:
			Integer, representing the amount of Vote Points the user has
		dp:
			Integer, representing the amount of Donation Points the user has
		char_slots:
			Integer, representing the number of character slots the user has
	"""

	def __init__(self, account_info, database_config):
		"""Emulates how account object is handled server-sided

		Args:
			account_info:
				dictionary of user attributes, formatted in AzureMS style
			database_config:
				dictionary of protected attributes from a Lazuli object
		"""

		self._account_info = account_info
		self._database_config = database_config

		self._account_id = 0  # Primary Key - Do NOT set
		self._username = ""  # varchar(64)
		self._logged_in = 0  # int(1) and not bool for some reason
		self._banned = 0  # int(1) and not bool for some reason
		self._ban_reason = ""  # text
		# The GM attribute has nothing to do with
		# in-game GM command level - excluded for now
		# self._gm = 0
		self._nx = 0
		self._maple_points = 0
		self._vp = 0
		self._dp = 0
		self._char_slots = 0

		self.init_account_stats()

	def init_account_stats(self):
		"""Initialises Account instance attributes' values.

		Runs near the end of Account::__init__(account_info, database_config).
		Assigns values contained in account_info (a dictionary of
		account-related attributes from AzureMS's DB) to the Account object's
		corresponding attributes.
		"""
		self._account_id = self._account_info['id']
		self._username = self._account_info['name']
		self._logged_in = self._account_info['loggedin']
		self._banned = self._account_info['banned']
		self._ban_reason = self._account_info['banreason']
		# self._gm = self._account_info['gm']  # See __innit__
		self._nx = self._account_info['nxCash']
		self._maple_points = self._account_info['mPoints']
		self._vp = self._account_info['vpoints']
		# 'realcash' corresponding to DP is a guess - Might be wrong!
		self._dp = self._account_info['realcash']
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
		# Check for length:
		if len(str(new_name)) > 64:
			# Message to be passed along on failure:
			raise ValueError("That name is too long!")
		else:
			# Check for clashes
			data = utils.get_db_all_hits(
				self.database_config,
				f"SELECT * FROM `accounts` WHERE `name` = '{new_name}'"
			)
			if not data:
				# if the list of accounts with clashing names is not empty
				self.set_stat_by_column("name", new_name)  # set name in DB
				# then refresh instance variable in memory:
				self._username = new_name
			else:
				# Message to be passed along on failure:
				raise ValueError("That name is already taken!")

	@property
	def logged_in(self):
		return self._logged_in

	@logged_in.setter
	def logged_in(self, value):
		try:
			if value > 127:  # DB only accepts 1-byte int
				raise ValueError(
					"That `logged_in` value is too large! "
					"Stick to either 0 or 1!")
			else:
				self.set_stat_by_column("loggedin", value)  # Use with caution!
				self._logged_in = value
		except Exception:
			raise ValueError("Invalid input! Stick to either 0 or 1!") from None

	@property
	def banned(self):
		return self._banned

	@banned.setter
	def banned(self, value):
		try:
			if value > 127:  # DB only accepts 1-byte int
				raise ValueError(
					"That `banned` value is too large! "
					"Stick to either 0 or 1!")
			else:
				self.set_stat_by_column("banned", value)  # Use with caution!
				self._banned = value
		except Exception:
			raise ValueError("Invalid input! Stick to either 0 or 1!") from None

	@property
	def ban_reason(self):
		return self._ban_reason

	@ban_reason.setter
	def ban_reason(self, value):
		self.set_stat_by_column("banreason", value)  # type `text`; 65k chars
		self._ban_reason = value

	@property
	def nx(self):
		return self._nx

	@nx.setter
	def nx(self, value):
		if value > 2147483647:
			raise ValueError("Invalid input! Please keep NX within 2.1b!")
		else:
			self.set_stat_by_column("nxCash", value)
			self._nx = value

	def add_nx(self, amount):
		"""Adds the specified amount to the current NX pool

		Args:
			amount:
				Int, representing the amount of NX to be added to the NX pool
		"""
		new_nx = int(amount) + self.nx
		self.nx = new_nx

	@property
	def maple_points(self):
		return self._maple_points

	@maple_points.setter
	def maple_points(self, value):
		if value > 2147483647:
			raise ValueError(
				"Invalid input! "
				"Please keep Maple Points within 2.1b!")
		else:
			self.set_stat_by_column("mPoints", value)
			self._maple_points = value

	def add_maple_points(self, amount):
		"""Adds the specified amount to the current Maple Points pool

		Args:
			amount:
				Int, representing the number of Maple Points
				to be added to the current pool
		"""
		new_maple_points = int(amount) + self.maple_points
		self.maple_points = new_maple_points

	@property
	def vp(self):
		return self._vp

	@vp.setter
	def vp(self, value):
		if value > 2147483647:
			raise ValueError(
				"Invalid input! "
				"Please keep Vote Points within 2.1b!")
		else:
			self.set_stat_by_column("vpoints", value)
			self._vp = value

	def add_vp(self, amount):
		"""Adds the specified amount to the current VP count

		Args:
			amount:
				Int, representing the number of vote points (VP) to be added
				to the current VP count
		"""
		new_vp = int(amount) + self.vp
		self.vp = new_vp

	@property
	def dp(self):
		return self._dp

	@dp.setter
	def dp(self, value):
		if value > 2147483647:
			raise ValueError("Invalid input! Please keep DPs within 2.1b!")
		else:
			self.set_stat_by_column("realcash", value)
			self._dp = value

	def add_dp(self, amount):
		"""Adds the specified amount to the current DP count

		Args:
			amount:
				Int, representing the number of DPs to be added
				to the current DP count
		"""
		new_dp = int(amount) + self.dp
		self.dp = new_dp

	@property
	def char_slots(self):
		return self._char_slots

	@char_slots.setter
	def char_slots(self, value):
		if value > 52:
			raise ValueError(
				"Invalid input! "
				"Please keep Character Slots within 52!")
		else:
			self.set_stat_by_column("chrslot", value)
			self._char_slots = value

	def add_char_slots(self, amount):
		"""Adds the specified amount to the current character slot count

		Args:
			amount:
				Int, representing the number of slots to be added
				to the current count
		"""
		new_count = int(amount) + self.char_slots
		self.char_slots = new_count

	def is_online(self):
		"""Checks if the 'loggedin' column is greater than 0

		Returns:
			Boolean, representing the online status of the account
		"""
		if int(self.logged_in) > 0:
			return True
		return False

	def unstuck(self):
		"""Sets loggedin column in database to 0

		This unstucks the account, since server checks loggedin value
		to decided whether they are "logged in"
		"""
		self.logged_in = 0

	def change_password(self, new_pass):
		"""Changes the current password to the given one.

		WARNING: INHERENTLY UNSAFE
		Azure316 does not hash passwords by default, so this function
		is technically functional for the open source version.

		Args:
			new_pass: string, representing the new password
		"""
		self.set_stat_by_column("password", new_pass)

	def get_stat_by_column(self, column):
		"""Fetches account attribute by column name

		Args:
			column: String, representing column name in DB

		Returns:
			Int or String, representing user attribute queried

		Raises:
			Generic error on failure, handled by utils.get_stat_by_column
		"""
		return utils.get_stat_by_column(self.account_info, column)

	def set_stat_by_column(self, column, value):
		"""Sets a account's attributes by column name in database

		Grabs the database attributes provided through the class constructor.
		Uses these attributes to attempt a database connection through
		utility.write_to_db. Attempts to update the field represented by
		the provided column in the accounts table, with the provided value.
		Not recommended to use this method on it's own, as it will not update
		the account instance variables (in memory) post-change.

		Args:
			value:
				int or string, representing the value to be set in the database
			column:
				string, representing the column in the database
				that is to be updated

		Returns:
			A boolean representing whether the operation was successful.

		Raises:
			Generic error, handled in utility.write_to_db
		"""
		status = utils.write_to_db(
			self._database_config,
			f"UPDATE `accounts` SET {column} = '{value}' "
			f"WHERE `id` = '{self.account_id}'"
		)
		if status:
			print(
				f"Successfully updated {column} value "
				f"for user id: {self.account_id}.")
			# Update the stats in the dictionary:
			self._account_info[column] = value
		return status
