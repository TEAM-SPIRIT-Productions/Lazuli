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

        Due to the inherent complexity of MapleStory's inventory system, this Inventory object will
        attempt to contain attributes of all 6 of AzureMS's inventory types, using a custom object.
        Every inventory attribute is a list of dictionaries, the latter of which models the contents of
        the `inventoryitems` table in a AzureMS-based database.
    """
        # Pseudocode:
        # Create generic SQL method that fetches all entries from a given query - Handled by Brandon
        # Create children methods for each inventory type
        # Initialise attributes with contents of each inventory type (init methods)
        # Create getters for each attribute
        # Create has_item_in_XXX and is_equiping methods
        self._character_id = character_id
        self._database_config = db_config

    @property
    def database_config(self):
        return self._database_config

    @property
    def character_id(self):
        return self._character_id

    @staticmethod
    def get_inv_type_by_name(inv_string):
        inv_type = utils.inv_types.get(inv_string)
        return inv_type

    @staticmethod
    def get_inv_name_by_type(inv_type):
        inv_name = utils.get_key(utils.inv_types, inv_type)
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
                isCash = items["isCash"]
                inventory_type = items["inventorytype"]
                item_stats = {
                    "itemid": item_id,
                    "quantity": quantity,
                    "inventorytype": inventory_type,
                    "isCash": isCash
                }
                inv[bag_index] = item_stats
                # Key value, we set as the bag_index aka position of the item in the inventory.
            return inv
        except Exception as e:
            print(f"[ERROR] Error trying to load inventory type {inv_type}", e)
