"""This module holds the Inventory class for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con


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

    def __init__(self, inv_ids, db_config):
        """Inventory object; quasi-models AzureMS inventories.

        Due to the inherent complexity of MapleStory's inventory system, this Inventory object will
        attempt to contain attributes of all 6 of AzureMS's inventory types, using a custom object.
        Every inventory attribute is a list of dictionaries, the latter of which models the contents of
        the `inventoryitems` table in a AzureMS-based database.
    """
        # Pseudocode:
        # Create generic SQL method that fetches all entries from a given query
        # Create children methods for each inventory type
        # Initialise attributes with contents of each inventory type (init methods)
        # Create getters for each attribute
        # Create has_item_in_XXX and is_equiping methods
