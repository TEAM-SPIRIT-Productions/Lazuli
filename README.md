# Lazuli
Lazuli is a pip-compatible, Python-based package for interacting with [AzureMSv316](https://github.com/SoulGirlJP/AzureV316)-based databases.  
Lazuli is inspired by and based on the [SwordieDB](https://github.com/Bratah123/SwordieDB) project.  

Lazuli allows access to character and inventory attributes in [AzureMSv316](https://github.com/SoulGirlJP/AzureV316)-based databases.  

#### Current Status: Now Available on PyPi (See [changelog](https://github.com/TEAM-SPIRIT-Productions/Lazuli/blob/main/CHANGELOG.md))

### Quick Start
Installation via PyPi/Pip:
  1. Run `pip install lazuli` inside of your venv (or global, if desired)
      - see [wiki](https://github.com/TEAM-SPIRIT-Productions/Lazuli/wiki/Technical-Details) for how to generate venv
  2. Import the module in your project
      - `from lazuli.database import Lazuli`
  3. Create an Azure database object using the Lazuli class constructor
      - `azure = Lazuli()`
      - See the [Wiki](https://github.com/TEAM-SPIRIT-Productions/Lazuli/wiki/Sample-Code-Fragments#loading-a-database) for full examples
      - See the [API Docs](https://team-spirit-productions.github.io/Lazuli/reference/lazuli/) for more in-depth technical documentation
  4. Query
      - E.g. `number_of_players_online = azure.get_online_count()` gives number (int) of accounts currently connected to the server

## Documentation:
Kindly refer to the [Project Wiki](https://github.com/TEAM-SPIRIT-Productions/Lazuli/wiki) for detailed documentation.  
The [Discussions Page](https://github.com/TEAM-SPIRIT-Productions/Lazuli/discussions) is currently open for any questions!  
Please report any [issues](https://github.com/TEAM-SPIRIT-Productions/Lazuli/issues)!  
