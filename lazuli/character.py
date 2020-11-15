"""This module holds the Character class for the lazuli package.

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
Refer to database.py or the project wiki on GitHub for usage examples.
"""
import mysql.connector as con

from lazuli import JOBS
from lazuli.inventory import Inventory
from lazuli.account import Account


class Character:
    """Character object; models AzureMS characters.

    Using instance method Lazuli::get_char_by_name(name) will create a Character object instance with
    attributes identical to the character with IGN "name" in the connected AzureMS-based database.
    This class contains the appropriate getter and setter methods for said attributes.

    Attributes:
        TO BE ADDED
    """

    def __init__(self, char_stats, database_config):
        """Emulates how character object is handled server-sided

        Not all character attributes are inherited, as the database table design in AzureMS is quite verbose

        Args:
            char_stats: dictionary of character stats, formatted in AzureMS style
            database_config: dictionary of protected attributes from a Lazuli object
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
        self._mute = ""  # Takes lower case true/false but is a varchar (45) and not a Bool

        self.init_stats()  # Assign instance variables

        # Create Inventory object instance via class constructor, using details from Character object instance
        self._inventory = self.init_inventory()

        # Create Account object instance via class constructor, using details from Character object instance
        self._account = self.init_account()

    # fill with attributes from init
    def init_stats(self):
        """Given a dictionary of stats from AzureMS's DB we add them to Character object's attributes

        Runs near the end of Character::__init__(char_stats, database_config).
        It assigns the character attributes in char_stats to their respective protected attributes belonging to
        the Character object instance.
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
        """Fetch a dictionary of account attributes from AzureMS's DB and use it to instantiate a new Account object

        Runs at the end of Character::__init__(char_stats, database_config).
        Checks the account ID associated with the character instance, and uses the Account class constructor to create
        a new Account object instance, with the relevant attributes from the database.

        Returns:
            Account object with attributes identical to its corresponding entry in the database
        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        account_id = self.get_db(
            self._database_config,
            f"SELECT * FROM characters WHERE id = '{self.character_id}'"
        )  # The row will always be 0 because there should be no characters with the same character ID (Primary Key)
        
        account_info = self.get_db(
            self._database_config,
            f"SELECT * FROM accounts WHERE id = '{account_id}'"
        )  # The row will always be 0 because there should be no characters with the same account ID (Primary Key)

        account = Account(account_info, self.database_config)
        return account

    def init_inventory(self):
        """Fetch a dictionary of user attributes from AzureMS's DB and use it to instantiate a new (custom) Inventory object

        Runs near the end of Character::__init__(char_stats, database_config).
        Uses the Character ID associated with the character instance, and the Inventory class constructor to create
        a new Inventory object instance, with the relevant inventory attributes from the database.

        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        inventory = Inventory(self.character_id, self.database_config)
        return inventory

    # Static method for fetching DB
    @staticmethod
    def get_db(config, query):
        """Generic static method for fetching data from DB using the provided DB config and query
        
        This method assumes that only one character is found - it always defaults to the first result.
        An effort has been made to convert this to a decorator so that it may also be applied to
        Character::set_stat_by_column() & Character::get_user_id(), which ultimately ended in failure.
        
        Args:
            config, dictionary, representing database config attributes
            query, String, representing SQL query

        Returns:
            String representing the result of the provided SQL query, using the provided DB connection attributes

        Raises:
            SQL Error 2003: Can't cannect to DB
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
                port=config['port']
            )
            cursor = database.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()[0]
            database.disconnect()

            return data
            
        except Exception as e:
            print("CRITICAL: Error encountered whilst attempting to connect to the database! \n", e)

    @property
    def database_config(self):
        return self._database_config

    @property
    def stats(self):
        return self._stats

    @property
    def character_id(self):
        return self._character_id  # Only getter, no setter; Primary Key must not be set manually!

    @property
    def account_id(self):
        return self._account_id  # Only getter, no setter; Primary Key must not be set manually!

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
            amount: Int, representing the number of levels to be added to the current count
        """
        new_level = int(self.level) + amount
        if new_level > 275:
            raise ValueError("Level should not exceed 275!")
        else:
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
            new_name: string, representing the new character name that will be set in the database
        """
        if len(new_name) > 13:
            raise ValueError("Character names can only be 13 characters long!")
        else:
            self.set_stat_by_column("name", new_name)
            self._name = new_name

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
            amount: Int, representing the amount of mesos to be added to the current count
        """
        new_amount = int(self.meso) + amount
        if new_amount > 10000000000:
            raise ValueError("You should not try to set meso to more than 10b!")
        else:
            self.meso = str(new_amount)  # money is a String; converting back to String for consistency

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
            amount: Int, representing the number of fames to be added to the current count
        """
        new_fame = int(self.fame) + amount
        if new_fame > 32767:
            raise ValueError("You should not try to set fame to more than 30k!")
        else:
            self.fame = new_fame

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, map_id):
        if map_id < 100000000 or map_id > 999999999:  # Best guess - might be wrong!
            raise ValueError("Wrong map ID!")
        else:
            self.set_stat_by_column("map", map_id)
            self._map = map_id

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, face_id):
        self.set_stat_by_column("face", face_id)  # TODO: Add check
        self._face = face_id

    @property
    def hair(self):
        return self._hair

    @hair.setter
    def hair(self, hair_id):
        self.set_stat_by_column("hair", hair_id)  # TODO: Add check
        self._hair = hair_id

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, skin_id):
        self.set_stat_by_column("skin", skin_id)  # TODO: Add check
        self._skin = skin_id

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender_id):
        self.set_stat_by_column("gender", gender_id)  # TODO: Add check
        self._gender = gender_id

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp_amount):
        if exp_amount > 2147483647:
            raise ValueError("You should not try to set EXP above 2bil!")
        else:
            self.set_stat_by_column("exp", exp_amount)
            self._exp = exp_amount

    def add_exp(self, amount):
        """Add the specified amount to the current existing EXP pool

        Args:
            amount: Int, representing the amount of EXP to be added to the current pool
        """
        if amount > 2147483647:
            raise ValueError("You should not try to increment EXP by more than 2bil!")
        else:
            new_exp = int(self.exp) + amount
            self.exp = str(new_exp)  # EXP is a String; converting back to String for consistency

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, amount):
        if amount > 32767:
            raise ValueError("You should not try to set STR above 30k!")
        else:
            self.set_stat_by_column("str", amount)
            self._strength = amount

    def add_str(self, amount):
        """Add the specified amount to the current existing STR pool

        Args:
            amount: Int, representing the amount of STR to be added to the current pool
        """
        new_str = int(self.strength) + amount
        if new_str > 32767:
            raise ValueError("You should not try to set STR above 30k!")
        else:
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
            amount: Int, representing the amount of DEX to be added to the current pool
        """
        new_dex = int(self.dex) + amount
        if new_dex > 32767:
            raise ValueError("You should not try to set DEX above 30k!")
        else:
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
            amount: Int, representing the amount of INT to be added to the current pool
        """
        new_inte = int(self.inte) + amount
        if new_inte > 32767:
            raise ValueError("You should not try to set INT above 30k!")
        else:
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
            amount: Int, representing the amount of LUK to be added to the current pool
        """
        new_luk = int(self.luk) + amount
        if new_luk > 32767:
            raise ValueError("You should not try to set LUK above 30k!")
        else:
            self.luk = new_luk

    def get_primary_stats(self):
        """Returns str, int, dex, luk values in a dictionary

        Returns:
            dictionary of primary stats
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
        self.set_stat_by_column("maxhp", amount)
        self._max_hp = amount

    def add_max_hp(self, amount):
        """Add the specified amount to the current existing Max HP pool

        Args:
            amount: Int, representing the amount of Max HP to be added to the current pool
        """
        new_hp = int(self.max_hp) + amount
        self.max_hp = new_hp

    @property
    def max_mp(self):
        return self._max_mp

    @max_mp.setter
    def max_mp(self, amount):
        self.set_stat_by_column("maxmp", amount)
        self._max_mp = amount

    def add_max_mp(self, amount):
        """Add the specified amount to the current existing Max MP pool

        Args:
            amount: Int, representing the amount of max MP to be added to the current pool
        """
        new_mp = int(self.max_mp) + amount
        self.max_mp = new_mp

    @property
    def ap(self):
        return self._ap

    @ap.setter
    def ap(self, amount):
        if amount > 32767:
            raise ValueError("You should not try to set AP above 30k!")
        else:
            self.set_stat_by_column("ap", amount)
            self._ap = amount

    def add_ap(self, amount):
        """Add the specified amount to the current existing free AP pool

        Args:
            amount: Int, representing the amount of free AP to be added to the current pool
        """
        new_ap = int(self.ap) + amount
        if new_ap > 32767:
            raise ValueError("You should not try to set AP above 30k!")
        else:
            self.ap = new_ap

    @property
    def bl_slots(self):
        return self._bl_slots

    @bl_slots.setter
    def bl_slots(self, amount):
        # TODO: Add checks
        self.set_stat_by_column("buddyCapacity", amount)
        self._bl_slots = amount

    def add_bl_slots(self, amount):
        # TODO: Add checks
        new_amount = int(self.bl_slots) + amount
        self.bl_slots = new_amount

    @property
    def rebirths(self):
        return self._rebirths

    @rebirths.setter
    def rebirths(self, amount):
        # TODO: Add checks
        self.set_stat_by_column("reborns", amount)
        self._rebirths = amount

    def add_rebirths(self, amount):
        # TODO: Add checks
        new_amount = int(self.rebirths) + amount
        self.rebirths = new_amount

    @property
    def ambition(self):
        return self._ambition

    @ambition.setter
    def ambition(self, amount):
        # TODO: Add checks
        self.set_stat_by_column("ambition", amount)
        self._ambition = amount

    def add_ambition(self, amount):
        # TODO: Add checks
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
        # TODO: Add checks
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
        # TODO: Add checks
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
        # TODO: Add checks
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
        # TODO: Add checks
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
        # TODO: Add checks
        new_amount = int(self.charm) + amount
        self.charm = new_amount

    @property
    def honour(self):
        return self._honour

    @honour.setter
    def honour(self, amount):
        # TODO: Add checks
        self.set_stat_by_column("honour", amount)
        self._honour = amount

    def add_honour(self, amount):
        # TODO: Add checks
        new_amount = int(self.honour) + amount
        self.honour = new_amount

    @property
    def mute(self):
        return self._mute

    @mute.setter
    def mute(self, status):
        # TODO: Add checks
        self.set_stat_by_column("mute", status)
        self._mute = status

    @property
    def account(self):
        return self._account

    @property
    def inventory(self):
        return self._inventory

    def get_char_img(self):
        equipped_items = [self.face, self.hair]
        equipped_inv = self.inventory.equipped_inv

        for item in equipped_inv:
            item_id = equipped_inv[item]["itemid"]
            equipped_items.append(item_id)

        url = f"https://maplestory.io/api/GMS/216/Character/200{self.skin}/{str(equipped_items)[1:-1]}/stand1/1".replace(" ", "")

        return url

    def set_stat_by_column(self, column, value):
        """Update a character's stats from column name in database

        Grabs the database attributes provided through the class constructor.
        Uses these attributes to attempt a database connection.
        Attempts to update the field represented by the provided column in characterstats, with the provided value.
        Not recommended to use this alone, as it won't update the character object which this was used from.

        Args:
            value: int or string, representing the value to be set in the database
            column: string, representing the column in the database that is to be updated

        Returns:
            A boolean representing whether the operation was successful

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
            cursor.execute(f"UPDATE characters SET {column} = '{value}' WHERE name = '{self.name}'")
            database.commit()
            print(f"Successfully updated {column} value for character: {self.name}.")
            self._stats[column] = value  # Update the stats in the dictionary
            database.disconnect()
            return True
        except Exception as e:
            print("[ERROR] Error trying to set stats in database.", e)
            return False

    def get_stat_by_column(self, column):
        """Given a column name, return its value in the database

        Args:
            column: string, representing the column in the database from which the value is to be fetched from

        Returns:
            string, representing the value in the database associated with the provided column

        Raises:
            Generic error on failure
        """
        try:
            return self.stats[column]
        except Exception as e:
            print("[ERROR] Error trying to get stats from given column.", e)
            return False