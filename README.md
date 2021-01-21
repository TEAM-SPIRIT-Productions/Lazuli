# Lazuli
![](https://i.imgur.com/o25Tqra.png)  
[![Downloads](https://static.pepy.tech/personalized-badge/lazuli?period=total&units=international_system&left_color=black&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/lazuli) [![Downloads](https://static.pepy.tech/personalized-badge/lazuli?period=month&units=international_system&left_color=black&right_color=blue&left_text=Monthly%20Downloads)](https://pepy.tech/project/lazuli) [![Downloads](https://static.pepy.tech/personalized-badge/lazuli?period=week&units=international_system&left_color=black&right_color=blue&left_text=Weekly%20Downloads)](https://pepy.tech/project/lazuli) [![HitCount](http://hits.dwyl.com/TEAM-SPIRIT-Productions/Lazuli.svg)](http://hits.dwyl.com/TEAM-SPIRIT-Productions/Lazuli)  
*Stats courtesy of PePy and [dwyl](https://github.com/dwyl)*  
Lazuli is a pip-compatible, Python-based package for interacting with [AzureMSv316](https://github.com/SoulGirlJP/AzureV316)-based databases.  
Lazuli is inspired by and based on the [SwordieDB](https://github.com/Bratah123/SwordieDB) project.  

Lazuli allows access to character and inventory attributes in [AzureMSv316](https://github.com/SoulGirlJP/AzureV316)-based databases.  
This makes it possible to produce not only feature-rich Discord bots, but also integrated websites.  

***Perks:***  
  - Easy to set-up - *simply install with pip!*
  - Lovingly commented
  - API docs and example code provided
  - Already used in [Lapis](https://github.com/TEAM-SPIRIT-Productions/Lapis)

#### Current Status: Now Available on [PyPi](https://pypi.org/project/lazuli/) (See [changelog](https://github.com/TEAM-SPIRIT-Productions/Lazuli/blob/main/CHANGELOG.md))
---
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

## Acknowledgements:
1. The [SwordieDB](https://github.com/Bratah123/SwordieDB) project by [Bratah123](https://github.com/Bratah123)  
    - This project is inspired by and based on SwordieDB  
2. [**MapleStory:**IO](https://maplestory.io/) by [Senpai#1337](https://discord.gg/3SyrbAs)  
      - The character sprite generation makes use of MapleStory.IO APIs  

### Disclaimer:
*Lazuli is an open-source third-party implementation of APIs for a particular MapleStory server emulation project ([AzureMSv316](https://github.com/SoulGirlJP/AzureV316)). Lazuli is non-monetised, provided as is, and is unaffiliated with NEXON. Every effort has been taken to ensure correctness and reliability of Lazuli. We will not be liable for any special, direct, indirect, or consequential damages or any damages whatsoever resulting from loss of use, data or profits, whether in an action if contract, negligence or other tortious action, arising out of or in connection with the use of Lazuli (in part or in whole).*
