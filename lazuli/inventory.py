"""This module holds the Inventory class for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con
import lazuli.utility as utils


class Inventory:
	"""Inventory object; quasi-models AzureMS inventories.

	The instance method Lazuli::get_char_by_name(name) creates a Character object; as part of
	lazuli Character object instantiation, an Inventory object instance containing inventory attributes of
	the character with IGN "name" in the connected AzureMS-based database is created.
	This class contains the appropriate getter methods for said attributes.
	As a consequence of the inherent complexity of MapleStory's item system, for safety reasons,
	this module offers NO inventory-write operations (aka setters).

	Attributes:
		equip_inv: list of dictionaries, representing in-game items contained by the EQUIP tab
		consume_inv: list of dictionaries, representing in-game items contained by the USE tab
		etc_inv: list of dictionaries, representing in-game items contained by the ETC tab
		install_inv: list of dictionaries, representing in-game items contained by the SETUP tab
		cash_inv: list of dictionaries, representing in-game items contained by the CASH tab
		equipped_inv: list of dictionaries, representing in-game items currently equipped by the character
	"""

	def __init__(self, character_id, db_config):
		"""Inventory object; quasi-models AzureMS inventories.

		Modelled after SwordieDB project's Inventory class init method.
		Due to the inherent complexity of MapleStory's inventory system, this Inventory object will
		attempt to contain attributes of all 6 of AzureMS's inventory types, using a custom object.
		Every inventory attribute is a dictionary of dictionaries, the latter of which models the contents of
		the `inventoryitems` table in a AzureMS-based database.
	"""
		self._character_id = character_id
		self._database_config = db_config

		self._equip_inv = self.init_equip_items()
		self._use_inv = self.init_use_inv()
		self._etc_inv = self.init_etc_inv()
		self._cash_inv = self.init_cash_inv()
		self._install_inv = self.init_install_inv()

		self._equipped_inv = self.init_equipped_inv()

	@property
	def database_config(self):
		return self._database_config

	@property
	def character_id(self):
		return self._character_id

	@property
	def equip_inv(self):
		return self._equip_inv

	@property
	def consume_inv(self):
		return self._use_inv

	@property
	def etc_inv(self):
		return self._etc_inv

	@property
	def cash_inv(self):
		return self._cash_inv

	@property
	def install_inv(self):
		return self._install_inv

	@property
	def equipped_inv(self):
		return self._equipped_inv

	@staticmethod
	def get_inv_type_by_name(inv_string):
		inv_type = utils.map_inv_types.get(inv_string)
		return inv_type

	@staticmethod
	def get_inv_name_by_type(inv_type):
		inv_name = utils.get_key(utils.map_inv_types, inv_type)
		return inv_name

	def load_inv(self, inv_type):
		""" Fetches Inventory data from a given Inventory Type, (I.E. -1, 1, 2, 3, 4, 5)

		Args:
			inv_type: int

		Returns: dictionary, representing the inventory type we loaded

		"""
		try:
			database = con.connect(
				host=self.database_config['host'],
				user=self.database_config['user'],
				password=self.database_config['password'],
				database=self.database_config['schema'],
				port=self.database_config['port']
			)
			cursor = database.cursor(dictionary=True)
			cursor.execute(
				f"SELECT * FROM inventoryitems WHERE characterid = '{self.character_id}' AND inventorytype = '{inv_type}'")
			inventory = cursor.fetchall()

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
				# Key value, we set as the bag_index aka position of the item in the inventory.
			return inv
		except Exception as e:
			print(f"[ERROR] Error trying to load inventory type {inv_type}", e)

	def init_equip_items(self):
		return self.load_inv(self.get_inv_type_by_name("equip"))

	def init_use_inv(self):
		return self.load_inv(self.get_inv_type_by_name("use"))

	def init_etc_inv(self):
		return self.load_inv(self.get_inv_type_by_name("etc'"))

	def init_cash_inv(self):
		return self.load_inv(self.get_inv_type_by_name("cash"))

	def init_equipped_inv(self):
		return self.load_inv(self.get_inv_type_by_name("equipped"))

	def init_install_inv(self):
		return self.load_inv(self.get_inv_type_by_name("setup"))

	@staticmethod
	def has_item_in_inv_type(inv_type, item_id):
		"""Checks whether the particular tab of the inventory has an item
		Generic static method used by the other Inventory::has_item_in_XXX() methods, and the
		Character::is_equipping() method.
		Iterates through the dictionary of items associated with the specified tab, and check if
		the provided item ID can be found as a value.
		Returns:
			Boolean, representing whether the specified item was found
		"""
		for bag_index in inv_type:
			if inv_type[bag_index]['itemid'] == item_id:
				return True
		return False

	def has_item_in_equip(self, item_id):
		"""Checks whether the EQUIP tab of the inventory has an item
		Uses Inventory::has_item_in_inv_type()
		Returns:
			Boolean, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.equip_inv, item_id)

	def has_item_in_consume(self, item_id):
		"""Checks whether the USE tab of the inventory has an item
		Uses Inventory::has_item_in_inv_type()
		Returns:
			Boolean, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.consume_inv, item_id)

	def has_item_in_etc(self, item_id):
		"""Checks whether the ETC tab of the inventory has an item
		Uses Inventory::has_item_in_inv_type()
		Returns:
			Boolean, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.etc_inv, item_id)

	def has_item_in_install(self, item_id):
		"""Checks whether the SETUP tab of the inventory has an item
		Uses Inventory::has_item_in_inv_type()
		Returns:
			Boolean, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.install_inv, item_id)

	def has_item_in_cash(self, item_id):
		"""Checks whether the CASH tab of the inventory has an item
		Uses Inventory::has_item_in_inv_type()
		Returns:
			Boolean, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.cash_inv, item_id)

	def is_equipping(self, item_id):
		"""Checks whether the EQUIP window (i.e. Hotkey "E") has an item (i.e. item is equipped)
		Uses Inventory::has_item_in_inv_type()
		Returns:
			Boolean, representing whether the specified item was found
		"""
		return self.has_item_in_inv_type(self.equipped_inv, item_id)

