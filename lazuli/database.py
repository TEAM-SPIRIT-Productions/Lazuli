"""Lazuli is designed for use in development of AzureMSv316-based MapleStory private server tools (e.g. Discord bots).

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found in the LICENSE file.
This module contains the main class that users would instantiate: Lazuli.
Users can use this class to fetch and manipulate information from the database.
Refer to the project wiki on GitHub for more in-depth examples.

    Typical usage example:

    lazuli = Lazuli()  # Instantiate DB object
    char = lazuli.get_char_by_name("KOOKIIE")  # Instantiate Character object
    meso = char.money  # Use of Character methods to fetch data from DB
    char.money = 123456789  # Use of Character methods to write data to DB
"""
import mysql.connector as con
from lazuli.character import Character
from lazuli.account import Account
import lazuli.utility as utils


class Lazuli:
    """Database object; models the AzureMS DB.

    Use this class to create instances of AzureMS characters, or inventories, complete with their respective
    data from the connected AzureMS-based database.
    Using instance method Lazuli::get_char_by_name("name") will create a Character object (see character.py) instance
    that has attributes identical to the character with IGN "name" in the connected AzureMS-based database.

    Attributes:
        host: Optional; IP address of the database. Defaults to "localhost"
        schema: Optional; Name of the schema of the database. Defaults to "kms_316`"
        user: Optional; Username for access to the database. Defaults to "root"
        password: Optional; Password for access to the database. Defaults to ""
        port: Optional; Port with which to access the database. Defaults to 3306
    """

    def __init__(self, host="localhost", schema="kms_316", user="root", password="", port=3306):
        self._host = host
        self._schema = schema
        self._user = user
        self._password = password
        self._port = port

        self._database_config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
            'schema': self.schema,
            'port': self.port
        }

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, x):
        self._host = x

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, x):
        self._schema = x

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, x):
        self._user = x

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, x):
        self._password = x

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port

    def get_char_by_name(self, char_name):
        """Create an instance of a Character object from the given character name

        Uses the class constructor of the Character class to create a new instance, with the corresponding
        character data and database attributes from the connected database.

        Args:
            char_name: string, representing character name (aka IGN)

        Returns:
            Character object instantiated with corresponding data from the connected database.
            Defaults to None if the operation fails.

        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        character_stats = Character.get_db_first_hit(
            self._database_config,
            f"SELECT * FROM characters WHERE `name` = '{char_name}'"
        )  # Fetch first result because there should only be one character with that name

        character = Character(character_stats, self._database_config)
        return character

    def get_account_by_username(self, username):
        """Given a username (NOT IGN), create a new account object instance

        Fetches the user account attributes from the database by querying for username.
        uses the User class constructor to create a new User object instance, with the said attributes.
        Useful for getting account information from accounts with no characters.

        Args:
            username: String, representing the username used for logging the user into game

        Returns:
            Account object with attributes identical to its corresponding entry in the database

        Raises:
            Generic error on failure - handled by the Character::get_db() method
        """
        account_info = Character.get_db_first_hit(
            self._database_config,
            f"SELECT * FROM accounts WHERE `name` = '{username}'"
        )  # Fetch first result because there should only be one character with that name

        account = Account(account_info, self._database_config)
        return account

    def set_char_stat(self, name, column, value):
        """Given a character name and column name, change its value in the database

        Args:
            column: string, representing the column in the database
            name: string, representing the character name in the database
            value: string/int, representing the value that is to be updated in the corresponding field

        Returns:
            boolean, representing whether the operation completed successfully

        Raises:
            SQL Error 2003: Can't cannect to DB
            WinError 10060: No response from DB
            List index out of range: Wrong column or character name
        """
        try:
            database = con.connect(host=self.host, user=self.user, password=self.password, database=self.schema,
                                   port=self.port)
            cursor = database.cursor(dictionary=True)
            cursor.execute(f"UPDATE characters SET {column} = '{value}' WHERE `name` = '{name}'")
            database.commit()
            database.disconnect()
            print(f"Successfully set {name}'s stats in database.")
            return True
        except Exception as e:
            print("[ERROR] Error trying to update character stats in Database.", e)
            return False

    def get_db_all_hits(self, query):
        """Fetch all matching data from DB using the provided query

        Wrapper function. Uses the DB config from Lazuli attributes for DB connection.
        Feeds the config values into utility.get_db_all_hits().

        Args:
            query: String, representing SQL query

        Returns:
            List of objects, representing the result of the provided SQL query, using the provided DB connection attributes

        Raises:
            Generic error on failure - handled by the utility.get_db_all_hits() method

        """
        data = utils.get_db_all_hits(self._database_config, query)
        return data

    def get_online_list(self):
        """Fetch the list of players currently online

        AzureMS stores login state in the DB, in the 'accounts' table, 'loggedin' column.
        Lazuli::get_online_list queries for a list of all accounts that are logged in,
        using the Lazuli::get_db_all_hits method.

        Returns:
            List, representing all players online. Defaults to False in the event of an error during execution

        Raises:
            Generic error on failure
        """
        data = self.get_db_all_hits(f"SELECT * FROM accounts WHERE `loggedin` > 0")
        return data  # List of online players

    def get_online_count(self):
        """Fetch the number of players currently online

        Uses the Lazuli::get_online_list method to fetch the list of all players online.
        Counts the length of said list, to obtain number of players online.

        Returns:
            Int, representing number of players online. Defaults to False in the event of an error during execution

        Raises:
            Generic error on failure, handled by Lazuli::get_online_list()
        """
        players = self.get_online_list()
        return len(players)

    def get_online_players(self):
        """Fetch usernames of all players currently online

        Uses the Lazuli::get_online_list method to fetch the list of all players online.
        Extract the usernames from the said list.

        Returns:
            List, representing all players online. Defaults to False in the event of an error during execution

        Raises:
            Generic error on failure, handled by Lazuli::get_online_list()
        """
        player_data = self.get_online_list()
        return utils.extract_name(player_data)

    def get_level_ranking(self):
        """Fetches the Top 5 players in terms of level

        Uses Lazuli::get_db_all_hits to query, and utility.extract_name to process the data.

        Returns:
            List of Strings, representing player names
        """
        player_data = self.get_db_all_hits("SELECT * FROM `characters` ORDER BY `level` DESC LIMIT 5")
        return utils.extract_name(player_data)

    def get_meso_ranking(self):
        """Fetches the Top 5 players in terms of mesos

        Uses Lazuli::get_db_all_hits to query, and utility.extract_name to process the data.

        Returns:
            List of Strings, representing player names
        """
        player_data = self.get_db_all_hits("SELECT * FROM `characters` ORDER BY `meso` DESC LIMIT 5")
        return utils.extract_name(player_data)

    def get_fame_ranking(self):
        """Fetches the Top 5 players in terms of fame

        Uses Lazuli::get_db_all_hits to query, and utility.extract_name to process the data.

        Returns:
            List of Strings, representing player names
        """
        player_data = self.get_db_all_hits("SELECT * FROM `characters` ORDER BY `fame` DESC LIMIT 5")
        return utils.extract_name(player_data)

    def get_rebirth_ranking(self):
        """Fetches the Top 5 players in terms of rebirths

        Uses Lazuli::get_db_all_hits to query, and utility.extract_name to process the data.

        Returns:
            List of Strings, representing player names
        """
        player_data = self.get_db_all_hits("SELECT * FROM `characters` ORDER BY `reborns` DESC LIMIT 5")
        return utils.extract_name(player_data)

    def get_rebirth_ranking_by_job_id(self, job_id):
        """Fetches the Top 5 players of a particular class (specific Job ID), in terms of rebirths

        Uses Lazuli::get_db_all_hits to query, and utility.extract_name to process the data.

        Returns:
            List of Strings, representing player names
        """
        player_data = self.get_db_all_hits(f"SELECT * FROM `characters` WHERE `job`={job_id} ORDER BY `reborns` DESC LIMIT 5")
        return utils.extract_name(player_data)
