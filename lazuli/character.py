"""This module holds the Character class for the lazuli package.

Copyright 2022 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to `database.py` or the project wiki on GitHub for usage examples.
"""

from typing import Any
from lazuli.account import Account
from lazuli.inventory import Inventory
from lazuli.jobs import JOBS
import lazuli.utility as utils


class Character:
	"""`Character` object; models AzureMS characters.

	Using instance method `Lazuli::get_char_by_name(name)` will create a
	`Character` object instance with attributes identical to the character with
	IGN `name` in the connected AzureMS-based database. This class contains
	the appropriate getter and setter methods for said attributes.
	"""

	def __init__(
		self,
		char_stats: dict[str, Any],
		database_config: dict[str, str],
	) -> None:
		"""Emulates how the `Character` object is handled by a game server

		Not all character attributes are inherited, as the database
		table design in AzureMS is quite verbose

		Note that AzureMS uses a mixture of `utf8`, `latin1`, and `euckr` in its
		database - YMMV when attempting to expand attribute handling features.

		Args:

			char_stats (`dict`): Represents character stats, formatted in AzureMS style
			database_config (`dict`): Represents the protected attributes from a `Lazuli` object
		"""
		self._stats = char_stats
		self._database_config = database_config

		self._character_id: int = 0
		self._account_id: int = 0
		self._name: str = ""  # varchar 13
		self._level: int = 0
		self._exp: int = 0
		self._strength: int = 0
		self._dex: int = 0
		self._luk: int = 0
		self._inte: int = 0
		self._max_hp: int = 0
		self._max_mp: int = 0
		self._meso: int = 0
		self._job: int = 0
		self._skin: int = 0
		self._gender: int = 0
		self._fame: int = 0
		self._hair: int = 0
		self._face: int = 0
		self._ap: int = 0
		self._map: int = 0
		self._bl_slots: int = 0
		self._rebirths: int = 0
		self._ambition: int = 0
		self._insight: int = 0
		self._willpower: int = 0
		self._diligence: int = 0
		self._empathy: int = 0
		self._charm: int = 0
		self._honour: int = 0
		self._mute: str = ""  # Takes lower case String "true"/"false" but
		# is a varchar (45) and not a Bool

		self.init_stats()  # Assign instance variables

		# Create Account object instance via class constructor,
		# using details from Character object instance
		self._account = self.init_account()

	# fill with attributes from init
	def init_stats(self) -> None:
		"""Initialises `Character` instance attributes' values.

		Runs near the end of `Character::__init__(char_stats, database_config)`.
		Assign values contained in `char_stats` (a dictionary of
		character-related attributes from AzureMS's DB) to the `Character`
		object's corresponding attributes.
		"""
		self._character_id = self._stats['id']
		self._account_id = self._stats['accountid']
		self._name = self._stats['name']
		self._level = self._stats['level']
		self._exp = self._stats['exp']
		self._strength = self._stats['str']
		self._dex = self._stats['dex']
		self._luk = self._stats['luk']
		self._inte = self._stats['int']
		self._max_hp = self._stats['maxhp']
		self._max_mp = self._stats['maxmp']
		self._meso = self._stats['meso']
		self._job = self._stats['job']
		self._skin = self._stats['skincolor']
		self._gender = self._stats['gender']
		self._fame = self._stats['fame']
		self._hair = self._stats['hair']
		self._face = self._stats['face']
		self._ap = self._stats['ap']
		self._map = self._stats['map']
		self._bl_slots = self._stats['buddyCapacity']
		# Defaults to 0/false for non-Azure Odin-like DBs that don't have these:
		self._rebirths = self._stats.get("reborns", 0)
		self._ambition = self._stats.get("ambition", 0)
		self._insight = self._stats.get("insight", 0)
		self._willpower = self._stats.get("willpower", 0)
		self._diligence = self._stats.get("diligence", 0)
		self._empathy = self._stats.get("empathy", 0)
		self._charm = self._stats.get("charm", 0)
		self._honour = self._stats.get("innerExp", 0)  # Best guess - might be wrong!
		self._mute = self._stats.get("chatban", "false")

	def init_account(self) -> Account:
		"""Instantiate an `Account` object corresponding to the character

		Runs at the end of `Character::__init__(char_stats, database_config)`.
		Fetch the account ID associated with the `Character` instance; use the
		account ID to fetch the account attributes as a dictionary.
		Then use the `Account` class constructor to create a new `Account` object
		instance, with the relevant attributes from the database.

		Returns:

			`Account` object with attributes identical to its
			corresponding entry in the database
		Raises:
			Generic error on failure - handled by the
			`utility.get_db_first_hit()` method
		"""
		account_id: int = utils.get_db_first_hit(
			self._database_config,
			f"SELECT * FROM `characters` WHERE `id` = '{self.character_id}'"
		).get("accountid")
		# get_db() returns a Dictionary, so get() is used
		# to fetch only the account ID
		# The row index will always be 0 because there should be no characters
		# with the same character ID (Primary Key)

		account_info: dict[str, Any] = utils.get_db_first_hit(
			self._database_config,
			f"SELECT * FROM `accounts` WHERE `id` = '{account_id}'"
		)  # The row index will always be 0 because there should be no
		# accounts with the same account ID (Primary Key)

		account = Account(account_info, self._database_config)
		return account

	@property
	def character_id(self) -> int:
		"""`int`: Represents Primary Key for Character - Do **NOT** set manually

		This is an `int(11)` in the database.
		"""
		return self._character_id
		# Only getter, no setter; Primary Key must not be set manually!

	@property
	def account_id(self) -> int:
		"""`int`: Represents Primary Key for Account (FK) - Do **NOT** set manually

		This is an `int(11)` in the database.
		"""
		return self._account_id
		# Only getter, no setter; Primary Key must not be set manually!

	@property
	def level(self) -> int:
		"""`int`: Represents Character level

		Note that the setter does not allow `int` values outside `1` to `275`.
		YMMV if you're attempting to use Lazuli for older Odin-like servers
		that only support a level cap of 255, or for newer ones that support
		higher level caps.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._level

	@level.setter
	def level(self, x: int) -> None:
		if x > 275:
			raise ValueError("Level should not exceed 275!")
		elif x < 1:
			raise ValueError("Level should not be lower than 1!")
		else:
			self.set_stat_by_column("level", x)
			self._level = x

	def add_level(self, amount: int) -> None:
		"""Adds the specified amount to the current level count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the number of levels to be added to the current count
		"""
		new_level = int(self.level) + amount
		self.level = new_level

	@property
	def job(self) -> int:
		"""`int`: Represents the Job ID of the character

		Note that the setter does not allow arbitrary Job IDs not documented
		in SpiritSuite.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._job

	@job.setter
	def job(self, job_id: int) -> None:
		if str(job_id) not in JOBS:
			raise ValueError("Invalid Job ID!")
		else:
			self.set_stat_by_column("job", job_id)
			self._job = job_id

	def get_job_name(self) -> str:
		"""Returns the actual name of the job from job id

		Returns:
			A string representing the job name corresponding to a job ID
		"""
		return JOBS[str(self.job)]

	@property
	def name(self) -> str:
		"""`str`: Represents the character's IGN

		This is an `varchar(13)` in the database.
		The setter only accepts names that are up to 13 characters long, and
		does not check for names with special symbols, due to
		its use downstream being intended to be restricted to admin/staff only.
		Note that you may encounter encoding issues if you're attempting to set
		non-latin names, as Korean character support is not a priority for this
		module.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._name

	@name.setter
	def name(self, new_name: str) -> None:
		# Check length against max length in Azure DB
		length = len(str(new_name))
		if not length or length > 13:
			raise ValueError("Character names can only be 1 - 13 characters long!")
		# Check clashes
		data = utils.get_db_all_hits(
			self._database_config,
			f"SELECT * FROM `characters` WHERE `name` = '{new_name}'"
		)
		if not data:  # if the list of accounts with clashing names is not empty
			self.set_stat_by_column("name", new_name)  # set IGN in DB
			# Refresh character instance attributes in memory:
			self._name = new_name
		else:
			# Message to be passed along on failure:
			raise ValueError("That name is already taken!")

	@property
	def meso(self) -> int:
		"""`int`: Represents the character's wealth (aka Meso count)

		The setter only accepts values from 0 to 10 billion. YMMV if you're
		attempting to use Lazuli for older Odin-like servers that only supports
		32-bit signed `int` values for mesos.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._meso

	@meso.setter
	def meso(self, amount: int) -> None:
		if amount > 10000000000:
			raise ValueError("You should not try to set meso to more than 10b!")
		elif amount < 0:
			raise ValueError("You should not try to set meso to less than 0!")
		else:
			self.set_stat_by_column("meso", amount)
			self._meso = amount

	def add_mesos(self, amount: int) -> None:
		"""Adds the specified amount to the current meso count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of mesos to be added to the current count
		"""
		new_amount = int(self.meso) + amount
		self.meso = new_amount

	@property
	def fame(self) -> int:
		"""`int`: Represents the character's fame count

		The setter only accepts values that can be held using Java's signed
		`shorts` (-32768 - 32767).

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._fame

	@fame.setter
	def fame(self, amount: int) -> None:
		if amount > 32767:
			raise ValueError("You should not try to set fame to more than 32k!")
		elif amount < -32768:
			raise ValueError("You should not try to set fame to less than -32k!")
		else:
			self.set_stat_by_column("fame", amount)
			self._fame = amount

	def add_fame(self, amount: int) -> None:
		"""Adds the specified amount to the current fame count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the number of fames to be added to the current count
		"""
		new_fame = int(self.fame) + amount
		self.fame = new_fame

	@property
	def map(self) -> None:
		"""`int`: Represents the Map ID of the map that the character is in

		The setter only accepts map IDs ranging from 100,000,000 to 999,999,999.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._map

	@map.setter
	def map(self, map_id: int) -> None:
		# Best guess for map ID limits - might be wrong!
		if map_id < 100000000 or map_id > 999999999:
			raise ValueError("Wrong map ID!")
		else:
			self.set_stat_by_column("map", map_id)
			self._map = map_id

	@property
	def face(self) -> int:
		"""`int`: Represents the Face ID of the character

		The setter only accepts face IDs ranging from 20,000 to 29,999.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._face

	@face.setter
	def face(self, face_id: int) -> None:
		# Best guess for face ID limits - might be wrong!
		if face_id < 20000 or face_id > 29999:
			raise ValueError("Wrong face ID!")
		else:
			self.set_stat_by_column("face", face_id)
			self._face = face_id

	@property
	def hair(self) -> int:
		"""`int`: Represents the Hair ID of the character

		The setter only accepts hair IDs ranging from 30,000 to 49,999.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._hair

	@hair.setter
	def hair(self, hair_id: int) -> None:
		# Best guess for hair ID limits - might be wrong!
		if hair_id < 30000 or hair_id > 49999:
			raise ValueError("Wrong hair ID!")
		else:
			self.set_stat_by_column("hair", hair_id)
			self._hair = hair_id

	@property
	def skin(self) -> int:
		"""`int`: Represents the Skin ID of the character

		The setter only accepts skin IDs ranging from 0 to 16.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._skin

	@skin.setter
	def skin(self, skin_id: int) -> None:
		# Best guess for skin ID limits - might be wrong!
		if skin_id < 0 or skin_id > 16:
			raise ValueError("Wrong skin colour ID!")
		else:
			self.set_stat_by_column("skincolor", skin_id)
			self._skin = skin_id

	@property
	def gender(self) -> int:
		"""`int`: Represents the Gender ID of the character

		The setter only accepts skin IDs ranging from -1 to 1.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._gender

	@gender.setter
	def gender(self, gender_id: int) -> None:
		# Best guess for gender ID limits - might be wrong!
		if gender_id < -1 or gender_id > 1:
			raise ValueError("Wrong gender ID!")
		else:
			self.set_stat_by_column("gender", gender_id)
			self._gender = gender_id

	@property
	def exp(self) -> int:
		"""`int`: Represents the character's EXP

		This is a `bigint(20)` in the DB.
		The setter allows values that can be held in a `bigint`, but YMMV with
		large EXP values, subject to what the server can handle without
		overflows. The upper limits have not been tested. Negative values are
		allowed, for convenience of developers' testing.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._exp

	@exp.setter
	def exp(self, exp_amount: int) -> None:
		if exp_amount > 9223372036854775807:  # Azure DB uses Bigint for EXP
			raise ValueError(
				"You should not try to set EXP above 9.2 Quintillion!"
			)
		elif exp_amount < -9223372036854775808:
			raise ValueError(
				"You should not try to set EXP below -9.2 Quintillion!"
			)
		else:
			self.set_stat_by_column("exp", exp_amount)
			self._exp = exp_amount

	def add_exp(self, amount: int) -> None:
		"""Add the specified amount to the current existing EXP pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of EXP to be added to the current pool
		"""
		new_exp = int(self.exp) + amount
		self.exp = new_exp

	@property
	def strength(self) -> int:
		"""`int`: Represents the character's STR stat pool

		The setter only accepts values that can be held using Java's signed
		`shorts` (-32768 - 32767).

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._strength

	@strength.setter
	def strength(self, amount: int) -> None:
		# Azure DB uses Int (max 2.1b) for stats, but it may cause problems
		# with the client if one exceeds signed shorts (max 32k)
		if amount > 32767:
			raise ValueError("You should not try to set STR above 30k!")
		elif amount < -32768:
			raise ValueError("You should not try to set STR to less than -32k!")
		else:
			self.set_stat_by_column("str", amount)
			self._strength = amount

	def add_str(self, amount: int) -> None:
		"""Add the specified amount to the current existing STR pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of STR to be added to the current pool
		"""
		new_str = int(self.strength) + amount
		self.strength = new_str

	@property
	def dex(self) -> int:
		"""`int`: Represents the character's DEX stat pool

		The setter only accepts values that can be held using Java's signed
		`shorts` (-32768 - 32767).

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._dex

	@dex.setter
	def dex(self, amount: int) -> None:
		if amount > 32767:
			raise ValueError("You should not try to set DEX above 30k!")
		elif amount < -32768:
			raise ValueError("You should not try to set DEX to less than -32k!")
		else:
			self.set_stat_by_column("dex", amount)
			self._dex = amount

	def add_dex(self, amount: int) -> None:
		"""Add the specified amount to the current existing DEX pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of DEX to be added to the current pool
		"""
		new_dex = int(self.dex) + amount
		self.dex = new_dex

	@property
	def inte(self) -> int:
		"""`int`: Represents the character's INT stat pool

		The setter only accepts values that can be held using Java's signed
		`shorts` (-32768 - 32767).

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._inte

	@inte.setter
	def inte(self, amount: int) -> None:
		if amount > 32767:
			raise ValueError("You should not try to set INT above 30k!")
		elif amount < -32768:
			raise ValueError("You should not try to set INT to less than -32k!")
		else:
			self.set_stat_by_column("int", amount)
			self._inte = amount

	def add_inte(self, amount: int) -> None:
		"""Add the specified amount to the current existing INT pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of INT to be added to the current pool
		"""
		new_inte = int(self.inte) + amount
		self.inte = new_inte

	@property
	def luk(self) -> int:
		"""`int`: Represents the character's LUK stat pool

		The setter only accepts values that can be held using Java's signed
		`shorts` (-32768 - 32767).

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._luk

	@luk.setter
	def luk(self, amount: int) -> None:
		if amount > 32767:
			raise ValueError("You should not try to set LUK above 30k!")
		elif amount < -32768:
			raise ValueError("You should not try to set LUK to less than -32k!")
		else:
			self.set_stat_by_column("luk", amount)
			self._luk = amount

	def add_luk(self, amount: int) -> None:
		"""Add the specified amount to the current existing LUK pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of LUK to be added to the current pool
		"""
		new_luk = int(self.luk) + amount
		self.luk = new_luk

	def get_primary_stats(self) -> dict[str, int]:
		"""Returns str, int, dex, luk values in a dictionary

		Returns:
			A dictionary of the 4 primary stats
		"""
		primary_stats = {
			"str": self.strength,
			"dex": self.dex,
			"int": self.inte,
			"luk": self.luk
		}
		return primary_stats

	@property
	def max_hp(self) -> int:
		"""`int`: Represents the character's Max HP stat pool

		The setter only accepts values from 1 to 500,000. YMMV if you're using
		an older Odin-like server whose client can not support 500,000 max HP.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._max_hp

	@max_hp.setter
	def max_hp(self, amount: int) -> None:
		# Client-sided cap of 500k
		if amount > 500000:
			raise ValueError("You should not try to set Max HP above 500k!")
		elif amount < 1:
			raise ValueError("You should not try to set Max HP below 1!")
		else:
			self.set_stat_by_column("maxhp", amount)
			self._max_hp = amount

	def add_max_hp(self, amount: int) -> None:
		"""Add the specified amount to the current existing Max HP pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of Max HP to be added to the current pool
		"""
		new_hp = int(self.max_hp) + amount
		self.max_hp = new_hp

	@property
	def max_mp(self) -> int:
		"""`int`: Represents the character's Max MP stat pool

		The setter only accepts values from 1 to 500,000. YMMV if you're using
		an older Odin-like server whose client can not support 500,000 max MP.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._max_mp

	@max_mp.setter
	def max_mp(self, amount: int) -> None:
		# Client-sided cap of 500k
		if amount > 500000:
			raise ValueError("You should not try to set Max MP above 500k!")
		elif amount < 1:
			raise ValueError("You should not try to set Max MP below 1!")
		else:
			self.set_stat_by_column("maxmp", amount)
			self._max_mp = amount

	def add_max_mp(self, amount: int) -> None:
		"""Add the specified amount to the current existing Max MP pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of max MP to be added to the current pool
		"""
		new_mp = int(self.max_mp) + amount
		self.max_mp = new_mp

	@property
	def ap(self) -> int:
		"""`int`: Represents the character's free Ability Points (AP) pool

		The setter only accepts values that can be held using Java's signed
		`shorts` (-32768 - 32767). Negative values are allowed for developers'
		testing convenience.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._ap

	@ap.setter
	def ap(self, amount: int) -> None:
		# Azure DB uses Int (max 2.1b) for stats, but it may cause problems
		# with the client if one exceeds signed shorts (max 32k)
		if amount > 32767:
			raise ValueError("You should not try to set AP above 32k!")
		elif amount < -32768:
			raise ValueError("You should not try to set AP to less than -32k!")
		else:
			self.set_stat_by_column("ap", amount)
			self._ap = amount

	def add_ap(self, amount: int) -> None:
		"""Add the specified amount to the current existing free AP pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of free AP to be added to the current pool
		"""
		new_ap = int(self.ap) + amount
		self.ap = new_ap

	@property
	def bl_slots(self) -> int:
		"""`int`: Represents the character's Buddy List slots

		The setter only accepts values from 20 to 100.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._bl_slots

	@bl_slots.setter
	def bl_slots(self, amount: int) -> None:
		# Client-sided cap of 100
		if amount > 100:
			raise ValueError("You should not try to set BL slots above 100!")
		elif amount < 20:
			raise ValueError("You should not try to set BL slots below 20!")
		else:
			self.set_stat_by_column("buddyCapacity", amount)
			self._bl_slots = amount

	def add_bl_slots(self, amount: int) -> None:
		"""Add the specified amount to the current existing BL slots cap

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of BL slots to be added to the current limit
		"""
		new_amount = int(self.bl_slots) + amount
		self.bl_slots = new_amount

	@property
	def rebirths(self) -> int:
		"""`int`: Represents the character's rebirth count

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._rebirths

	@rebirths.setter
	def rebirths(self, amount: int) -> None:
		if amount > 2147483647:
			raise ValueError("You should not try to set rebirths above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set rebirths below 0!")
		else:
			self.set_stat_by_column("reborns", amount)
			self._rebirths = amount

	def add_rebirths(self, amount: int) -> None:
		"""Add the specified amount to the current existing rebirth count

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of rebirths to be added to the current count
		"""
		new_amount = int(self.rebirths) + amount
		self.rebirths = new_amount

	@property
	def ambition(self) -> int:
		"""`int`: Represents the character's Ambition pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._ambition

	@ambition.setter
	def ambition(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Ambition above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Ambition below 0!")
		self.set_stat_by_column("ambition", amount)
		self._ambition = amount

	def add_ambition(self, amount: int) -> None:
		"""Add the specified amount to the current existing Ambition pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of ambition exp to be added to the current pool
		"""
		new_amount = int(self.ambition) + amount
		self.ambition = new_amount

	@property
	def insight(self) -> int:
		"""`int`: Represents the character's Insight pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._insight

	@insight.setter
	def insight(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Insight above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Insight below 0!")
		self.set_stat_by_column("insight", amount)
		self._insight = amount

	def add_insight(self, amount: int) -> None:
		"""Add the specified amount to the current existing Insight pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of insight exp to be added to the current pool
		"""
		new_amount = int(self.insight) + amount
		self.insight = new_amount

	@property
	def willpower(self) -> int:
		"""`int`: Represents the character's Willpower pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._willpower

	@willpower.setter
	def willpower(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Willpower above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Willpower below 0!")
		self.set_stat_by_column("willpower", amount)
		self._willpower = amount

	def add_willpower(self, amount: int) -> None:
		"""Add the specified amount to the current existing Willpower pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of willpower exp to be added to the current pool
		"""
		new_amount = int(self.willpower) + amount
		self.willpower = new_amount

	@property
	def diligence(self) -> int:
		"""`int`: Represents the character's Diligence pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._diligence

	@diligence.setter
	def diligence(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Diligence above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Diligence below 0!")
		self.set_stat_by_column("diligence", amount)
		self._diligence = amount

	def add_diligence(self, amount: int) -> None:
		"""Add the specified amount to the current existing Diligence pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of diligence exp to be added to the current pool
		"""
		new_amount = int(self.diligence) + amount
		self.diligence = new_amount

	@property
	def empathy(self) -> None:
		"""`int`: Represents the character's Empathy pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._empathy

	@empathy.setter
	def empathy(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Empathy above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Empathy below 0!")
		self.set_stat_by_column("empathy", amount)
		self._empathy = amount

	def add_empathy(self, amount: int) -> None:
		"""Add the specified amount to the current existing Empathy pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of empathy exp to be added to the current pool
		"""
		new_amount = int(self.empathy) + amount
		self.empathy = new_amount

	@property
	def charm(self) -> int:
		"""`int`: Represents the character's Charm pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._charm

	@charm.setter
	def charm(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Charm above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Charm below 0!")
		self.set_stat_by_column("charm", amount)
		self._charm = amount

	def add_charm(self, amount: int) -> None:
		"""Add the specified amount to the current existing Charm pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of charm exp to be added to the current pool
		"""
		new_amount = int(self.charm) + amount
		self.charm = new_amount

	def get_personality_traits(self) -> dict[str, int]:
		"""Returns the 6 personality traits' values in a dictionary

		Returns:
			A dictionary of personality traits
		"""
		traits = {
			"ambition": self.ambition,
			"insight": self.insight,
			"willpower": self.willpower,
			"diligence": self.diligence,
			"empathy": self.empathy,
			"charm": self.charm,
		}
		return traits

	@property
	def honour(self) -> int:
		"""`int`: Represents the character's Honour pool

		The setter only accepts values from 0 to the upper limit for a 32-bit
		signed `int`. Note that we are unsure of the actual limitations in-game
		, so YMMV for large numbers. The current checks are based on the DB's
		limits.

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._honour

	@honour.setter
	def honour(self, amount: int) -> None:
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		if amount > 2147483647:
			raise ValueError("You should not try to set Honour above 2.1b!")
		elif amount < 0:
			raise ValueError("You should not try to set Honour below 0!")
		self.set_stat_by_column("innerExp", amount)
		self._honour = amount

	def add_honour(self, amount: int) -> None:
		"""Add the specified amount to the current existing Honour pool

		### CAN ONLY BE SET WHEN SERVER IS OFF!

		Args:

			amount (`int`): Represents the amount of honour exp to be added to the current pool
		"""
		new_amount = int(self.honour) + amount
		self.honour = new_amount

	@property
	def mute(self) -> str:
		"""`str`: Represents whether a character is chat-banned

		The setter only accepts string values "false", or "true".

		### CAN ONLY BE SET WHEN SERVER IS OFF!
		"""
		return self._mute

	@mute.setter
	def mute(self, status: str) -> None:
		if status in ("false", "true"):
			self.set_stat_by_column("chatban", status)
			self._mute = status
		else:
			raise ValueError("Invalid input! Stick to `true` or `false`!")

	@property
	def account(self) -> Account:
		"""`Account`: Represents the account associate with the character"""
		return self._account

	def currency(self) -> dict[str, int]:
		"""Returns the values of the currencies held, in a dictionary

		Returns:
			A dictionary of mesos, nx, maple points, vp, dp.
		"""
		currencies = {
			"mesos": self.meso,
			"nx": self.account.nx,
			"maplepoints": self.account.maple_points,
			"vp": self.account.vp,
			"dp": self.account.dp,
		}
		return currencies

	def get_deep_copy(self) -> list[str]:
		"""Returns all known info about the character as a list

		Returns:
			A dictionary of IGN, Char ID, Account ID, Job Name, RB count,
			Level, Mesos, Fame, Gender, HP, MP, Stats, AP, EXP, Honour,
			Traits, BL slots, Map ID, Mute Status, Login Status, Ban Status,
			Ban Reason, Total Char Slots, Free Char Slots, DP, VP, NX,
			and Maple Points.
		"""
		attributes = [
			f"Character {self.name}'s attributes:\n",
			f"Character ID: {self.character_id}, ",
			f"Account ID: {self.account_id}, ",
			f"Job: {self.get_job_name()}, ",
			f"Rebirth Count: {self.rebirths}, ",
			f"Level: {self.level}, ",
			f"Meso Count: {self.meso}, ",
			f"Fame: {self.fame}, ",
			f"Gender: {self.gender}, ",
			f"HP/MP: {self.max_hp}, {self.max_mp}, ",
			f"Stats: {self.get_primary_stats()}, ",
			f"Free AP Pool: {self.ap}, ",
			f"EXP Pool: {self.exp}, ",
			f"Honour: {self.honour}, ",
			f"Traits: {self.get_personality_traits()}, ",
			f"Total Buddy List Slots: {self.bl_slots}, ",
			f"Map ID: {self.map}, ",
			f"Mute Status: {self.mute}, ",
		]

		attributes.extend(self.account.get_deep_copy()[2:])

		return attributes

	def get_inv(self) -> Inventory:
		"""Create an `Inventory` instance from the Character ID attribute

		Uses the Character ID associated with the character, and the
		`Inventory` class constructor to create a new `Inventory` object instance,
		with the relevant inventory attributes from the database.

		Returns:
			An `Inventory` object instantiated with corresponding data from the
			connected database.
			Defaults to `None` if the operation fails.

		Raises:
			Generic error on failure - handled by the `get_db_first_hit()` method
		"""
		inventory = Inventory(self.character_id, self._database_config)
		return inventory

	def get_char_img(self) -> str:
		"""Generates a character avatar using `MapleStory.io`; PLEASE USE SPARINGLY!

		Returns:
			A string, a link to the generated avatar
		"""
		equipped_items = [self.face, self.hair]
		equipped_inv = self.get_inv().equipped_inv

		for item in equipped_inv:
			item_id = equipped_inv[item]["itemid"]
			equipped_items.append(item_id)

		url = f"https://maplestory.io/api/GMS/216/Character/200{self.skin}/{str(equipped_items)[1:-1]}/stand1/1".replace(" ", "")

		return url

	def set_stat_by_column(self, column: str, value: Any) -> None:
		"""Update a character's stats from column name in database

		Grabs the database attributes provided through the class constructor.
		Uses these attributes to attempt a database connection through
		`utility.write_to_db`. Attempts to update the field represented by the
		provided column in the characters table, with the provided value.
		**NOT** recommended to use this alone, as it won't update the
		character instance variables (in memory) post-change.

		### ONLY WORKS WHEN SERVER IS OFF!

		Args:

			value (`int`, `str`, or `datetime`): Represents the value to be set in the database
			column (`str`): Represents the column in the database that is to be updated

		Returns:
			A `bool` representing whether the operation was successful

		Raises:
			Generic error, handled in `utility.write_to_db`
		"""
		status = utils.write_to_db(
			self._database_config,
			f"UPDATE `characters` SET {column} = '{value}' "
			f"WHERE `name` = '{self.name}'"
		)
		if status:
			print(
				f"Successfully updated {column} value "
				f"for character: {self.name}."
			)
			self._stats[column] = value  # Update the stats in the dictionary
		return status

	def get_stat_by_column(self, column: str) -> Any:
		"""Fetches account attribute by column name

		Args:

			column (`str`): Represents column name in DB

		Returns:
			An `int`, `str`, or `datetime`, representing user attribute queried

		Raises:
			Generic error on failure, handled by `utils.get_stat_by_column`
		"""
		return utils.get_stat_by_column(self._stats, column)
