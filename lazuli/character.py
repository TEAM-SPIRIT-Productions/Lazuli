"""This module holds the Character class for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""

from lazuli import JOBS
from lazuli.account import Account
from lazuli.inventory import Inventory
import lazuli.utility as utils


class Character:
	"""Character object; models AzureMS characters.

	Using instance method Lazuli::get_char_by_name(name) will create a
	Character object instance with attributes identical to the character with
	IGN "name" in the connected AzureMS-based database. This class contains
	the appropriate getter and setter methods for said attributes.

	Attributes:
		character_id: Integer, representing Primary Key for Character; int(11)
		account_id: Integer, representing Primary Key for Account (FK); int(11)
		name: String, representing Character IGN; varchar(13)
		level: Integer, representing Character level
		exp: Integer, representing Character EXP; bigint(20)
		strength: Integer, representing Character STR stat pool
		dex: Integer, representing Character DEX stat pool
		luk: Integer, representing Character LUK stat pool
		inte: Integer, representing Character INT stat pool
		max_hp: Integer, representing Character Max HP stat pool
		max_mp: Integer, representing Character Max MP stat pool
		meso: Integer, representing character wealth (aka Meso count)
		job: Integer, representing Job ID of the character
		skin: Integer, representing Skin ID of the character
		gender: Integer, representing Gender ID of the character
		fame: Integer, representing Character fame count
		hair: Integer, representing Hair ID of the character
		face: Integer, representing Face ID of the character
		ap: Integer, representing Character free Ability Points (AP) pool
		map: Integer, representing Map ID of the map that the character is in
		bl_slots: Integer, representing Character Buddy List slots
		rebirths: Integer, representing Character rebirth count
		ambition: Integer, representing Character Ambition pool
		insight: Integer, representing Character Insight pool
		willpower: Integer, representing Character Willpower pool
		diligence: Integer, representing Character Diligence pool
		empathy: Integer, representing Character Empathy pool
		charm: Integer, representing Character Charm pool
		honour: Integer, representing Character Honour pool
		mute: String, representing whether a character is chat-banned
	"""

	def __init__(self, char_stats, database_config):
		"""Emulates how character object is handled server-sided

		Not all character attributes are inherited, as the database
		table design in AzureMS is quite verbose

		Args:
			char_stats:
				Dictionary of character stats, formatted in AzureMS style
			database_config:
				Dictionary of protected attributes from a Lazuli object
		"""
		self._stats = char_stats
		self._database_config = database_config

		self._character_id = 0
		self._account_id = 0
		self._name = ""  # varchar 13
		self._level = 0
		self._exp = 0
		self._strength = 0
		self._dex = 0
		self._luk = 0
		self._inte = 0
		self._max_hp = 0
		self._max_mp = 0
		self._meso = 0
		self._job = 0
		self._skin = 0
		self._gender = 0
		self._fame = 0
		self._hair = 0
		self._face = 0
		self._ap = 0
		self._map = 0
		self._bl_slots = 0
		self._rebirths = 0
		self._ambition = 0
		self._insight = 0
		self._willpower = 0
		self._diligence = 0
		self._empathy = 0
		self._charm = 0
		self._honour = 0
		self._mute = ""  # Takes lower case String "true"/"false" but
		# is a varchar (45) and not a Bool

		self.init_stats()  # Assign instance variables

		# Create Account object instance via class constructor,
		# using details from Character object instance
		self._account = self.init_account()

	# fill with attributes from init
	def init_stats(self):
		"""Initialises Character instance attributes' values.

		Runs near the end of Character::__init__(char_stats, database_config).
		Assigns values contained in char_stats (a dictionary of
		character-related attributes from AzureMS's DB) to the Character
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
		self._rebirths = self._stats['reborns']
		self._ambition = self._stats['ambition']
		self._insight = self._stats['insight']
		self._willpower = self._stats['willpower']
		self._diligence = self._stats['diligence']
		self._empathy = self._stats['empathy']
		self._charm = self._stats['charm']
		self._honour = self._stats['innerExp']  # Best guess - might be wrong!
		self._mute = self._stats['chatban']

	def init_account(self):
		"""Instantiate a Account object corresponding to the character

		Runs at the end of Character::__init__(char_stats, database_config).
		Fetch the account ID associated with the character instance; use the
		account ID to fetch the account attributes as a dictionary.
		Then use the Account class constructor to create a new Account object
		instance, with the relevant attributes from the database.

		Returns:
			Account object with attributes identical to its
			corresponding entry in the database
		Raises:
			Generic error on failure - handled by the
			utility.get_db_first_hit() method
		"""
		account_id = utils.get_db_first_hit(
			self._database_config,
			f"SELECT * FROM `characters` WHERE `id` = '{self.character_id}'"
		).get("accountid")
		# get_db() returns a Dictionary, so get() is used
		# to fetch only the account ID
		# The row index will always be 0 because there should be no characters
		# with the same character ID (Primary Key)

		account_info = utils.get_db_first_hit(
			self._database_config,
			f"SELECT * FROM `accounts` WHERE `id` = '{account_id}'"
		)  # The row index will always be 0 because there should be no
		# accounts with the same account ID (Primary Key)

		account = Account(account_info, self._database_config)
		return account

	@property
	def character_id(self):
		return self._character_id
		# Only getter, no setter; Primary Key must not be set manually!

	@property
	def account_id(self):
		return self._account_id
		# Only getter, no setter; Primary Key must not be set manually!

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, x):
		if x > 275:
			raise ValueError("Level should not exceed 275!")
		else:
			self.set_stat_by_column("level", x)
			self._level = x

	def add_level(self, amount):
		"""Adds the specified amount to the current level count

		Args:
			amount:
				Int, representing the number of levels to be added
				to the current count
		"""
		new_level = int(self.level) + amount
		self.level = new_level

	@property
	def job(self):
		return self._job

	@job.setter
	def job(self, job_id):
		if str(job_id) not in JOBS:
			raise ValueError("Invalid Job ID!")
		else:
			self.set_stat_by_column("job", job_id)
			self._job = job_id

	def get_job_name(self):
		"""Returns the actual name of the job from job id

		Returns:
			String, representing the job name corresponding to a job ID
		"""
		return JOBS[str(self.job)]

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, new_name):
		"""Set a new name for the character

		Args:
			new_name:
				String, representing the new character name that
				will be set in the database
		"""
		# Check length against max length in Azure DB
		# Not checking for special symbols etc, since this is an admin command
		if len(str(new_name)) > 13:
			raise ValueError("Character names can only be 13 characters long!")
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
	def meso(self):
		return self._meso

	@meso.setter
	def meso(self, amount):
		if amount > 10000000000:
			raise ValueError("You should not try to set meso to more than 10b!")
		else:
			self.set_stat_by_column("meso", amount)
			self._meso = amount

	def add_mesos(self, amount):
		"""Adds the specified amount to the current meso count

		Args:
			amount:
				Int, representing the amount of mesos to be added
				to the current count
		"""
		new_amount = int(self.meso) + amount
		self.meso = new_amount

	@property
	def fame(self):
		return self._fame

	@fame.setter
	def fame(self, amount):
		if amount > 32767:
			raise ValueError("You should not try to set fame to more than 30k!")
		else:
			self.set_stat_by_column("fame", amount)
			self._fame = amount

	def add_fame(self, amount):
		"""Adds the specified amount to the current fame count

		Args:
			amount:
				Int, representing the number of fames to be added
				to the current count
		"""
		new_fame = int(self.fame) + amount
		self.fame = new_fame

	@property
	def map(self):
		return self._map

	@map.setter
	def map(self, map_id):
		# Best guess for map ID limits - might be wrong!
		if map_id < 100000000 or map_id > 999999999:
			raise ValueError("Wrong map ID!")
		else:
			self.set_stat_by_column("map", map_id)
			self._map = map_id

	@property
	def face(self):
		return self._face

	@face.setter
	def face(self, face_id):
		# Best guess for face ID limits - might be wrong!
		if face_id < 20000 or face_id > 29999:
			raise ValueError("Wrong face ID!")
		else:
			self.set_stat_by_column("face", face_id)
			self._face = face_id

	@property
	def hair(self):
		return self._hair

	@hair.setter
	def hair(self, hair_id):
		# Best guess for hair ID limits - might be wrong!
		if hair_id < 30000 or hair_id > 49999:
			raise ValueError("Wrong hair ID!")
		else:
			self.set_stat_by_column("hair", hair_id)
			self._hair = hair_id

	@property
	def skin(self):
		return self._skin

	@skin.setter
	def skin(self, skin_id):
		# Best guess for skin ID limits - might be wrong!
		if skin_id < 0 or skin_id > 16:
			raise ValueError("Wrong skin colour ID!")
		else:
			self.set_stat_by_column("skincolor", skin_id)
			self._skin = skin_id

	@property
	def gender(self):
		return self._gender

	@gender.setter
	def gender(self, gender_id):
		# Best guess for gender ID limits - might be wrong!
		if gender_id < -1 or gender_id > 1:
			raise ValueError("Wrong gender ID!")
		else:
			self.set_stat_by_column("gender", gender_id)
			self._gender = gender_id

	@property
	def exp(self):
		return self._exp

	@exp.setter
	def exp(self, exp_amount):
		if exp_amount > 9223372036854775807:  # Azure DB uses Bigint for EXP
			raise ValueError(
				"You should not try to set EXP above 9.2 Quintillion!"
			)
		else:
			self.set_stat_by_column("exp", exp_amount)
			self._exp = exp_amount

	def add_exp(self, amount):
		"""Add the specified amount to the current existing EXP pool

		Args:
			amount:
				Int, representing the amount of EXP to be added to
				the current pool
		"""
		new_exp = int(self.exp) + amount
		self.exp = new_exp

	@property
	def strength(self):
		return self._strength

	@strength.setter
	def strength(self, amount):
		# Azure DB uses Int (max 2.1b) for stats, but it may cause problems
		# with the client if one exceeds signed shorts (max 32k)
		if amount > 32767:
			raise ValueError("You should not try to set STR above 30k!")
		else:
			self.set_stat_by_column("str", amount)
			self._strength = amount

	def add_str(self, amount):
		"""Add the specified amount to the current existing STR pool

		Args:
			amount:
				Int, representing the amount of STR to be added to
				the current pool
		"""
		new_str = int(self.strength) + amount
		self.strength = new_str

	@property
	def dex(self):
		return self._dex

	@dex.setter
	def dex(self, amount):
		if amount > 32767:
			raise ValueError("You should not try to set DEX above 30k!")
		else:
			self.set_stat_by_column("dex", amount)
			self._dex = amount

	def add_dex(self, amount):
		"""Add the specified amount to the current existing DEX pool

		Args:
			amount:
				Int, representing the amount of DEX to be added to
				the current pool
		"""
		new_dex = int(self.dex) + amount
		self.dex = new_dex

	@property
	def inte(self):
		return self._inte

	@inte.setter
	def inte(self, amount):
		if amount > 32767:
			raise ValueError("You should not try to set INT above 30k!")
		else:
			self.set_stat_by_column("int", amount)
			self._inte = amount

	def add_inte(self, amount):
		"""Add the specified amount to the current existing INT pool

		Args:
			amount:
				Int, representing the amount of INT to be added to
				the current pool
		"""
		new_inte = int(self.inte) + amount
		self.inte = new_inte

	@property
	def luk(self):
		return self._luk

	@luk.setter
	def luk(self, amount):
		if amount > 32767:
			raise ValueError("You should not try to set LUK above 30k!")
		else:
			self.set_stat_by_column("luk", amount)
			self._luk = amount

	def add_luk(self, amount):
		"""Add the specified amount to the current existing LUK pool

		Args:
			amount:
				Int, representing the amount of LUK to be added to
				the current pool
		"""
		new_luk = int(self.luk) + amount
		self.luk = new_luk

	def get_primary_stats(self):
		"""Returns str, int, dex, luk values in a dictionary

		Returns:
			A Dictionary of the 4 primary stats
		"""
		primary_stats = {
			"str": self.strength,
			"dex": self.dex,
			"int": self.inte,
			"luk": self.luk
		}
		return primary_stats

	@property
	def max_hp(self):
		return self._max_hp

	@max_hp.setter
	def max_hp(self, amount):
		# Client-sided cap of 500k
		if amount > 500000:
			raise ValueError("You should not try to set HP above 500k!")
		else:
			self.set_stat_by_column("maxhp", amount)
			self._max_hp = amount

	def add_max_hp(self, amount):
		"""Add the specified amount to the current existing Max HP pool

		Args:
			amount:
				Int, representing the amount of Max HP to be added to
				the current pool
		"""
		new_hp = int(self.max_hp) + amount
		self.max_hp = new_hp

	@property
	def max_mp(self):
		return self._max_mp

	@max_mp.setter
	def max_mp(self, amount):
		# Client-sided cap of 500k
		if amount > 500000:
			raise ValueError("You should not try to set MP above 500k!")
		else:
			self.set_stat_by_column("maxmp", amount)
			self._max_mp = amount

	def add_max_mp(self, amount):
		"""Add the specified amount to the current existing Max MP pool

		Args:
			amount:
				Int, representing the amount of max MP to be added to
				the current pool
		"""
		new_mp = int(self.max_mp) + amount
		self.max_mp = new_mp

	@property
	def ap(self):
		return self._ap

	@ap.setter
	def ap(self, amount):
		# Azure DB uses Int (max 2.1b) for stats, but it may cause problems
		# with the client if one exceeds signed shorts (max 32k)
		if amount > 32767:
			raise ValueError("You should not try to set AP above 30k!")
		else:
			self.set_stat_by_column("ap", amount)
			self._ap = amount

	def add_ap(self, amount):
		"""Add the specified amount to the current existing free AP pool

		Args:
			amount:
				Int, representing the amount of free AP to be added to
				the current pool
		"""
		new_ap = int(self.ap) + amount
		self.ap = new_ap

	@property
	def bl_slots(self):
		return self._bl_slots

	@bl_slots.setter
	def bl_slots(self, amount):
		# Client-sided cap of 100
		if amount > 100:
			raise ValueError("You should not try to set BL slots above 100!")
		else:
			self.set_stat_by_column("buddyCapacity", amount)
			self._bl_slots = amount

	def add_bl_slots(self, amount):
		new_amount = int(self.bl_slots) + amount
		self.bl_slots = new_amount

	@property
	def rebirths(self):
		return self._rebirths

	@rebirths.setter
	def rebirths(self, amount):
		if amount > 2147483647:
			raise ValueError("You should not try to set rebirths above 2.1b!")
		else:
			self.set_stat_by_column("reborns", amount)
			self._rebirths = amount

	def add_rebirths(self, amount):
		new_amount = int(self.rebirths) + amount
		self.rebirths = new_amount

	@property
	def ambition(self):
		return self._ambition

	@ambition.setter
	def ambition(self, amount):
		# TODO: Add checks; DB allows 2.1b,
		#  but not sure what the actual cap in source is
		self.set_stat_by_column("ambition", amount)
		self._ambition = amount

	def add_ambition(self, amount):
		new_amount = int(self.ambition) + amount
		self.ambition = new_amount

	@property
	def insight(self):
		return self._insight

	@insight.setter
	def insight(self, amount):
		# TODO: Add checks
		self.set_stat_by_column("insight", amount)
		self._insight = amount

	def add_insight(self, amount):
		new_amount = int(self.insight) + amount
		self.insight = new_amount

	@property
	def willpower(self):
		return self._willpower

	@willpower.setter
	def willpower(self, amount):
		# TODO: Add checks
		self.set_stat_by_column("willpower", amount)
		self._willpower = amount

	def add_willpower(self, amount):
		new_amount = int(self.willpower) + amount
		self.willpower = new_amount

	@property
	def diligence(self):
		return self._diligence

	@diligence.setter
	def diligence(self, amount):
		# TODO: Add checks
		self.set_stat_by_column("diligence", amount)
		self._diligence = amount

	def add_diligence(self, amount):
		new_amount = int(self.diligence) + amount
		self.diligence = new_amount

	@property
	def empathy(self):
		return self._empathy

	@empathy.setter
	def empathy(self, amount):
		# TODO: Add checks
		self.set_stat_by_column("empathy", amount)
		self._empathy = amount

	def add_empathy(self, amount):
		new_amount = int(self.empathy) + amount
		self.empathy = new_amount

	@property
	def charm(self):
		return self._charm

	@charm.setter
	def charm(self, amount):
		# TODO: Add checks
		self.set_stat_by_column("charm", amount)
		self._charm = amount

	def add_charm(self, amount):
		new_amount = int(self.charm) + amount
		self.charm = new_amount

	def get_personality_traits(self):
		"""Returns the 6 personality traits' values in a dictionary

		Returns:
			dictionary of personality traits
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
	def honour(self):
		return self._honour

	@honour.setter
	def honour(self, amount):
		# TODO: Add checks
		self.set_stat_by_column("innerExp", amount)
		self._honour = amount

	def add_honour(self, amount):
		new_amount = int(self.honour) + amount
		self.honour = new_amount

	@property
	def mute(self):
		return self._mute

	@mute.setter
	def mute(self, status):
		if status in ("false", "true"):
			self.set_stat_by_column("chatban", status)
			self._mute = status
		else:
			raise ValueError("Invalid input! Stick to `true` or `false`!")

	@property
	def account(self):
		return self._account

	def get_deep_copy(self):
		"""Returns all known info about the character as a Dictionary"""
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

	def get_inv(self):
		"""Create an Inventory instance from the Character ID attribute

		Uses the Character ID associated with the character, and the
		Inventory class constructor to create a new Inventory object instance,
		with the relevant inventory attributes from the database.

		Returns:
			Inventory object instantiated with corresponding data from the
			connected database.
			Defaults to None if the operation fails.

		Raises:
			Generic error on failure - handled by the get_db_first_hit() method
		"""
		inventory = Inventory(self.character_id, self._database_config)
		return inventory

	def get_char_img(self):
		"""Generates character avatar using MapleStory.io; PLEASE USE SPARINGLY!

		Returns:
			url: String, a link to the generated avatar
		"""
		equipped_items = [self.face, self.hair]
		equipped_inv = self.get_inv().equipped_inv

		for item in equipped_inv:
			item_id = equipped_inv[item]["itemid"]
			equipped_items.append(item_id)

		url = f"https://maplestory.io/api/GMS/216/Character/200{self.skin}/{str(equipped_items)[1:-1]}/stand1/1".replace(" ", "")

		return url

	def set_stat_by_column(self, column, value):
		"""Update a character's stats from column name in database

		Grabs the database attributes provided through the class constructor.
		Uses these attributes to attempt a database connection through
		utility.write_to_db. Attempts to update the field represented by the
		provided column in the characters table, with the provided value.
		Not recommended to use this alone, as it won't update the
		character instance variables (in memory) post-change.

		Args:
			value:
				Int or String, representing the value to be set in the database
			column:
				String, representing the column in the database
				that is to be updated

		Returns:
			A Boolean representing whether the operation was successful

		Raises:
			Generic error, handled in utility.write_to_db
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

	def get_stat_by_column(self, column):
		"""Fetches account attribute by column name

		Args:
			column: String, representing column name in DB

		Returns:
			Int or String, representing user attribute queried

		Raises:
			Generic error on failure, handled by utils.get_stat_by_column
		"""
		return utils.get_stat_by_column(self._stats, column)
