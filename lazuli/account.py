"""This module holds the Account class for the lazuli package.

Copyright 2022 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to `database.py` or the project wiki on GitHub for usage examples.
"""

from typing import Any
import lazuli.utility as utils


class Account:
	"""`Account` object; models AzureMS accounts.

	Using instance method `Lazuli::get_account_by_username(username)` or
	the `Lazuli::get_char_by_name(name).account` getter will create an
	Account object instance with attributes identical to the account
	with username `username` (or IGN `name` for the latter) in
	the connected AzureMS-based database. This class contains the
	appropriate getter and setter methods for said attributes.
	"""

	def __init__(
		self,
		account_info: dict[str, Any],
		database_config: dict[str, str],
	) -> None:
		"""Emulates how the `Account` object is handled by a game server

		Args:

			account_info (`dict`):  Represents user attributes, formatted in AzureMS style
			database_config (`dict`): Represents the of protected attributes from a `Lazuli` object
		"""

		self._account_info = account_info
		self._database_config = database_config

		self._account_id: int = 0  # Primary Key - Do NOT set
		self._username: str = ""  # varchar(64)
		self._logged_in: int = 0  # int(1) and not bool for some reason
		self._banned: int = 0  # int(1) and not bool for some reason
		self._ban_reason: str = ""  # text
		# The GM attribute has nothing to do with
		# in-game GM command level - excluded for now
		# self._gm: int = 0
		self._nx: int = 0
		self._maple_points: int = 0
		self._vp: int = 0
		self._dp: int = 0
		self._char_slots: int = 0

		self.init_account_stats()

	def init_account_stats(self) -> None:
		"""Initialises `Account` instance attributes' values.

		Runs near the end of `Account::__init__(account_info, database_config)`.
		Assign values contained in `account_info` (a dictionary of
		account-related attributes from AzureMS's DB) to the `Account` object's
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
	def account_id(self) -> int:
		"""`int`: Represents Primary Key for account - Do **NOT** set manually"""
		return self._account_id  # Primary Key; DO NOT set

	@property
	def username(self) -> str:
		"""`str`: Represents account username

		This is a `varchar(64)` in the database.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._username

	@username.setter
	def username(self, new_name: str) -> None:
		# Check for length:
		if len(str(new_name)) > 64:
			# Message to be passed along on failure:
			raise ValueError("That name is too long!")
		else:
			# Check for clashes
			data = utils.get_db_all_hits(
				self._database_config,
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
	def logged_in(self) -> int:
		"""`int`: Represents the login status of the account

		Note that in the database, this is a `int(1)`,
		and not `bool`/`bit`/`char` for some reason.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._logged_in

	@logged_in.setter
	def logged_in(self, value: int) -> None:
		if value > 127:  # DB only accepts 1-byte int
			raise ValueError(
				"That `logged_in` value is too large! "
				"Stick to either 0 or 1!")

		else:
			self.set_stat_by_column("loggedin", value)  # Use with caution!
			self._logged_in = value

	@property
	def banned(self) -> int:
		"""`int`: Represents the ban status of the account

		Note that in the database, this is a `int(1)`,
		and not `bool`/`bit`/`char` for some reason.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._banned

	@banned.setter
	def banned(self, value: int) -> None:
		if value > 127:  # DB only accepts 1-byte int
			raise ValueError(
				"That `banned` value is too large! "
				"Stick to either 0 or 1!")
		else:
			self.set_stat_by_column("banned", value)  # Use with caution!
			self._banned = value

	@property
	def ban_reason(self) -> str:
		"""`str`: Represents the account ban reason

		This is a `text` in the database.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._ban_reason

	@ban_reason.setter
	def ban_reason(self, value: str) -> None:
		self.set_stat_by_column("banreason", value)  # type `text`; 65k chars
		self._ban_reason = value

	@property
	def nx(self) -> int:
		"""`int`: Represents the amount of NX Prepaid the user has

		Note that the setter does not allow `int` values larger than 32-bit
		signed `int`.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._nx

	@nx.setter
	def nx(self, value: int) -> None:
		if value > 2147483647:
			raise ValueError("Invalid input! Please keep NX within 2.1b!")
		else:
			self.set_stat_by_column("nxCash", value)
			self._nx = value

	def add_nx(self, amount: int) -> None:
		"""Adds the specified amount to the current NX pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of NX to be added to the NX pool
		"""
		new_nx = int(amount) + self.nx
		self.nx = new_nx

	@property
	def maple_points(self) -> int:
		"""`int`: Represents the amount of Maple Points the user has

		Note that the setter does not allow `int` values larger than 32-bit
		signed `int`.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._maple_points

	@maple_points.setter
	def maple_points(self, value: int) -> None:
		if value > 2147483647:
			raise ValueError(
				"Invalid input! "
				"Please keep Maple Points within 2.1b!")
		else:
			self.set_stat_by_column("mPoints", value)
			self._maple_points = value

	def add_maple_points(self, amount: int) -> None:
		"""Adds the specified amount to the current Maple Points pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the number of Maple Points to be added to the current pool
		"""
		new_maple_points = int(amount) + self.maple_points
		self.maple_points = new_maple_points

	@property
	def vp(self) -> int:
		"""`int`: Represents the amount of Vote Points the user has

		Note that the setter does not allow `int` values larger than 32-bit
		signed `int`.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._vp

	@vp.setter
	def vp(self, value: int) -> None:
		if value > 2147483647:
			raise ValueError(
				"Invalid input! "
				"Please keep Vote Points within 2.1b!")
		else:
			self.set_stat_by_column("vpoints", value)
			self._vp = value

	def add_vp(self, amount: int) -> None:
		"""Adds the specified amount to the current VP count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the number of vote points (VP) to be added to the current VP count
		"""
		new_vp = int(amount) + self.vp
		self.vp = new_vp

	@property
	def dp(self) -> int:
		"""`int`: Represents the amount of Donation Points the user has

		Note that the setter does not allow `int` values larger than 32-bit
		signed `int`.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._dp

	@dp.setter
	def dp(self, value: int) -> None:
		if value > 2147483647:
			raise ValueError("Invalid input! Please keep DPs within 2.1b!")
		else:
			self.set_stat_by_column("realcash", value)
			self._dp = value

	def add_dp(self, amount: int) -> None:
		"""Adds the specified amount to the current DP count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the number of DPs to be added to the current DP count
		"""
		new_dp = int(amount) + self.dp
		self.dp = new_dp

	@property
	def char_slots(self) -> int:
		"""`int`: Represents the number of character slots the user has

		Note that the setter does not allow `int` values larger than `52`.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._char_slots

	@char_slots.setter
	def char_slots(self, value: int) -> None:
		if value > 52:
			raise ValueError(
				"Invalid input! "
				"Please keep Character Slots within 52!")
		else:
			self.set_stat_by_column("chrslot", value)
			self._char_slots = value

	def add_char_slots(self, amount: int) -> None:
		"""Adds the specified amount to the current character slot count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the number of slots to be added to the current count
		"""
		new_count = int(amount) + self.char_slots
		self.char_slots = new_count

	def _get_char_list(self) -> list[dict[str, Any]]:
		"""Fetch all rows with the same account ID, from DB

		Returns:
			`list`, representing all characters in the same account.
			Defaults to False in the event of an error during execution

		Raises:
			A generic error on failure
		"""
		data = utils.get_db_all_hits(
			self._database_config,
			f"SELECT * FROM `characters` WHERE `accountid` = {self.account_id}"
		)
		return data

	@property
	def characters(self) -> list[str]:
		"""`list[str]`: Represents the IGN of all characters in the same account

		Returns:
			A `list`, containing character names of all characters
			in the same account.
			Defaults to False in the event of an error during execution

		Raises:
			A generic error on failure
		"""
		char_data = self._get_char_list()
		if not char_data:  # empty list
			return char_data
		return utils.extract_name(char_data)

	@property
	def free_char_slots(self) -> int:
		"""`int`: Represents the number of free character slots the user has"""
		total_slots = self._char_slots
		used_slots = len(self._get_char_list())  # count the number of chars
		return total_slots - used_slots

	def is_online(self) -> bool:
		"""Checks if the `loggedin` column is greater than `0`

		Returns:
			A `bool`, representing the online status of the account
		"""
		if int(self.logged_in) > 0:
			return True
		return False

	def unstuck(self) -> None:
		"""Sets `loggedin` column in database to `0`

		This un-stucks the account, since server checks the `loggedin` value
		to decided whether they are "logged in".

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		self.logged_in = 0

	def change_password(self, new_pass: str) -> None:
		"""Changes the current password to the given one.

		- **WARNING**: DEPRECATED!
		- **WARNING**: INHERENTLY UNSAFE!

		Azure316 now hashes passwords, as of [5dc6d6e](https://github.com/SoulGirlJP/AzureV316/commit/5dc6d6e2439195618337d02593512c515ab5de58).

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			new_pass (`str`): Represents the new password
		"""
		self.set_stat_by_column("password", new_pass)

	def get_deep_copy(self) -> list[str]:
		"""Returns all known info about the `Account` as a list"""
		attributes = [
			f"Username {self.username}'s attributes:\n",
			f"Account ID: {self.account_id}, ",
			f"Login Status: {self.is_online()}, ",
			f"Ban Status: {self.banned}, ",
			f"Ban Reason: {self.ban_reason}, ",
			f"Total Character Slots: {self.char_slots}, ",
			f"Free Character Slots: {self.free_char_slots}, ",
			f"DP: {self.dp}, ",
			f"VP: {self.vp}, ",
			f"NX: {self.nx}, ",
			f"Maple Points: {self.maple_points}",
		]
		return attributes

	def get_stat_by_column(self, column:str) -> Any:
		"""Fetches account attribute by column name

		Args:

			column (`str`): Represents column name in the DB

		Returns:
			`Any` type (likely `str`, `int`, or `datetime`), representing user attribute queried

		Raises:
			A generic error on failure, handled by `utils.get_stat_by_column`
		"""
		return utils.get_stat_by_column(self._account_info, column)

	def set_stat_by_column(self, column: str, value: Any) -> bool:
		"""Sets an account's attributes by column name in database

		### ONLY WORKS WHEN SERVER IS OFF!

		Grabs the database attributes provided through the class constructor.
		Uses these attributes to attempt a database connection through
		`utility.write_to_db`. Attempts to update the field represented by
		the provided column in the accounts table, with the provided value.
		**NOT** recommended to use this method on its own, as it will not update
		the account instance variables (in memory) post-change.

		Args:

			value (`int` or `str`): Represents the value to be set in the database
			column (`str`): Represents the column in the database that is to be updated

		Returns:
			A `bool` representing whether the operation was successful.

		Raises:
			A generic error, handled in `utility.write_to_db`
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
