"""This module holds the Inventory class for the lazuli package.

Copyright 2022 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
from typing import Any, Optional
import mysql.connector as con
import lazuli.utility as utils


class Inventory:
	"""`Inventory` object; quasi-models AzureMS inventories.

	The instance method `Lazuli::get_char_by_name(name)` creates a `Character`
	object; as part of lazuli `Character` object instantiation, an `Inventory`
	object instance containing inventory attributes of the character with
	IGN `name` in the connected AzureMS-based database is created.
	This class contains the appropriate getter methods for said attributes.
	As a consequence of the inherent complexity of MapleStory's item system,
	for safety reasons, this module offers NO inventory-write operations
	(aka setter methods).
	"""

	def __init__(self, character_id, db_config):
		"""`Inventory` object; quasi-models AzureMS inventories.

		Modelled after SwordieDB project's `Inventory` class init method.
		This `Inventory` object attempts to model attributes of all 6 of
		AzureMS's inventory types, using a custom object.
		Every inventory attribute is a `dict` of `dict`,
		the latter of which models the contents of the `inventoryitems` table
		in a AzureMS-based database.

		Args:

			character_id (`int`): Represents the foreign key
			db_config (`dict`): Represents the protected attributes from a `Lazuli` object
	"""
		self._character_id = character_id
		self._database_config = db_config

		# `list[`dict`]`: Represents all inventory/equipped items
		self._all_items = self.fetch_all_inv_items()

		self._equip_inv = self.init_equip_items()
		self._use_inv = self.init_use_inv()
		self._etc_inv = self.init_etc_inv()
		self._cash_inv = self.init_cash_inv()
		self._install_inv = self.init_install_inv()

		self._equipped_inv = self.init_equipped_inv()


	@staticmethod
	def has_item_in_inv_type(
		inv_type: dict[int, dict[str, Optional[int]]],
		item_id: int,
	) -> bool:
		"""Checks whether the particular tab of the inventory has an item

		Generic method used by `Inventory::has_item_in_XXX()` methods,
		and the `Inventory::is_equipping()` method. Iterates through the dictionary
		of items associated with the specified tab, and check if
		the provided item ID can be found as a value.

		Args:

			inv_type (`dict`): Represents the inventory tab to search
			item_id (`int`): Represents the ID of the item to search for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		for bag_index in inv_type:
			if inv_type[bag_index]['itemid'] == item_id:
				return True
		return False

	@property
	def equip_inv(self):
		"""`dict` of `dict`: Represents the in-game items contained within the EQUIP tab

		The key is the position of the item in the inventory tab, and the value
		contains the item attributes.
		"""
		return self._equip_inv

	@property
	def consume_inv(self):
		"""`dict` of `dict`: Represents the in-game items contained within the USE tab

		The key is the position of the item in the inventory tab, and the value
		contains the item attributes.
		"""
		return self._use_inv

	@property
	def etc_inv(self):
		"""`dict` of `dict`: Represents the in-game items contained within the ETC tab

		The key is the position of the item in the inventory tab, and the value
		contains the item attributes.
		"""
		return self._etc_inv

	@property
	def cash_inv(self):
		"""`dict` of `dict`: Represents the in-game items contained within the CASH tab

		The key is the position of the item in the inventory tab, and the value
		contains the item attributes.
		"""
		return self._cash_inv

	@property
	def install_inv(self):
		"""`dict` of `dict`: Represents the in-game items contained within the SETUP tab

		The key is the position of the item in the inventory tab, and the value
		contains the item attributes.
		"""
		return self._install_inv

	@property
	def equipped_inv(self):
		"""`dict` of `dict`: Represents the in-game items currently equipped by the character

		The key is the position of the item in the inventory tab, and the value
		contains the item attributes.
		"""
		return self._equipped_inv

	def fetch_all_inv_items(self):
		"""Fetch all items associated with the character

		Returns:
			A `list` of `dict` representing all inventory/equipped items
		"""
		try:
			database = con.connect(
				host=self._database_config['host'],
				user=self._database_config['user'],
				password=self._database_config['password'],
				database=self._database_config['schema'],
				port=self._database_config['port'],
				charset=self._database_config['charset']
			)
			cursor = database.cursor(dictionary=True)
			cursor.execute(
				f"SELECT * FROM `inventoryitems` WHERE `characterid` = "
				f"'{self._character_id}'"
			)
			inventory = cursor.fetchall()
			return inventory
		except Exception as e:
			print(f"ERROR: Unable to fetch inventory items\n{e}")

	def load_inv(self, inv_type):
		"""Given an inventory type, fetch every item associated with it

		Examples of inventory types: `-1`, `1`, `2`, `3`, `4`, `5`

		Args:

			inv_type (`int`): Representation of the inventory type encoded in the database

		Returns:
			A `dict` of `dict`, representing all the in-game items
			that are in the specified inventory type

		Raises:
			A generic error on failure
		"""
		try:
			all_items = self._all_items
			inventory = []
			# Extract the relevant inventory for the type
			for item in all_items:
				if item.get("inventorytype") == inv_type:
					inventory.append(item)

			inv = {}

			for items in inventory:
				# More to add if needed.
				bag_index = items["position"]
				item_id = items["itemid"]
				quantity = items["quantity"]
				is_cash = items["isCash"]
				inventory_type = items["inventorytype"]
				item_stats = {
					"itemid": item_id,
					"quantity": quantity,  # Never used
					"inventorytype": inventory_type,
					"iscash": is_cash  # Never used
				}
				inv[bag_index] = item_stats
				# Use the bag index (i.e. position of the item in the inventory)
				# as the key for the dictionary
			return inv
		except Exception as e:
			print(f"ERROR: Unable to load inventory type {inv_type}\n{e}")

	def init_equip_items(self):
		"""Extract items belonging to the EQUIP tab from the full list of items"""
		return self.load_inv(utils.get_inv_type_by_name("equip"))

	def init_use_inv(self):
		"""Extract items belonging to the USE tab from the full list of items"""
		return self.load_inv(utils.get_inv_type_by_name("use"))

	def init_etc_inv(self):
		"""Extract items belonging to the ETC tab from the full list of items"""
		return self.load_inv(utils.get_inv_type_by_name("etc'"))

	def init_cash_inv(self):
		"""Extract items belonging to the CASH tab from the full list of items"""
		return self.load_inv(utils.get_inv_type_by_name("cash"))

	def init_equipped_inv(self):
		"""Extract items that are currently equipped from the full list of items"""
		return self.load_inv(utils.get_inv_type_by_name("equipped"))

	def init_install_inv(self):
		"""Extract items belonging to the SETUP tab from the full list of items"""
		return self.load_inv(utils.get_inv_type_by_name("setup"))

	def has_item_in_equip(self, item_id):
		"""Checks whether the EQUIP tab of the inventory has an item

		Uses `Inventory::has_item_in_inv_type()`

		Args:

			item_id (`int`): Item ID of the item to check for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.equip_inv, item_id)

	def has_item_in_consume(self, item_id):
		"""Checks whether the USE tab of the inventory has an item

		Uses `Inventory::has_item_in_inv_type()`

		Args:

			item_id (`int`): Item ID of the item to check for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.consume_inv, item_id)

	def has_item_in_etc(self, item_id):
		"""Checks whether the ETC tab of the inventory has an item

		Uses `Inventory::has_item_in_inv_type()`

		Args:

			item_id (`int`): Item ID of the item to check for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.etc_inv, item_id)

	def has_item_in_install(self, item_id):
		"""Checks whether the SETUP tab of the inventory has an item

		Uses `Inventory::has_item_in_inv_type()`

		Args:

			item_id (`int`): Item ID of the item to check for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.install_inv, item_id)

	def has_item_in_cash(self, item_id):
		"""Checks whether the CASH tab of the inventory has an item

		Uses `Inventory::has_item_in_inv_type()`

		Args:

			item_id (`int`): Item ID of the item to check for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.cash_inv, item_id)

	def is_equipping(self, item_id):
		"""Checks whether an item is currently equipped

		Uses `Inventory::has_item_in_inv_type()` to check whether the
		EQUIP window (i.e. Hotkey "E") has an item (i.e. item is equipped)

		Args:

			item_id (`int`): Item ID of the item to check for

		Returns:
			A `bool`, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.equipped_inv, item_id)
