## CHANGELOG:  

### v3.0.0
- Remove distribution- and documentation-related dependencies from requirements
- Change documentation library from `Portray` to `pdoc`
- Create GitHub Actions workflow for automatic generation of API documentation 
- Reformat docstrings to follow Google style
- Replace `JOBS` dictionary in `__init__` module with the SpiritSuite YAML document
- PEP 484 Compliance: add type hints
- PEP 621 Compliance: Use `pyproject.toml`, `setuptools`, and `build` for distribution
- Update setup and build scripts

### v2.2.3
- Update dependencies following vulnerability notices from GitHub Advisory Database
  - PyYaml
    - [CVE-2020-1747](https://github.com/advisories/GHSA-6757-jp84-gxfx)
  - mkdocs
    - [CVE-2021-40978](https://github.com/advisories/GHSA-qh9q-34h6-hcv9)
  - jinja2
    - [CVE-2020-28493](https://github.com/advisories/GHSA-g3rq-g295-4j3m)
  - urllib3
    - [CVE-2021-28363](https://github.com/advisories/GHSA-5phf-pp7p-vc2r)
    - [CVE-2021-33503](https://github.com/advisories/GHSA-q2q7-5pp4-w6pg)
  - Pygments
    - [CVE-2021-20270](https://github.com/advisories/GHSA-9w8r-397f-prfh)
    - [CVE-2021-27291](https://github.com/advisories/GHSA-pq64-v7f5-gqh8)
  - nltk
    - [CVE-2021-3828](https://github.com/advisories/GHSA-2ww3-fxvq-293j)
    - [CVE-2021-3842](https://github.com/advisories/GHSA-rqjh-jp2r-59cj)
    - [CVE-2021-43854](https://github.com/advisories/GHSA-f8m6-h2c7-8h9x)

### v2.2.2
- Update dependencies following vulnerability notices from GitHub Advisory Database
  - Update MySQL Connector and protobuf, in view of CVE-2021-22570
- Change dummy name for unit tests
  - Use `tester0xFF` instead of the arbitrary `KOOKIE` for account and character name-change unit tests

### v2.2.1
- Add setup and build scripts
  - `setup.bat` automatically generates the venv folder with all dependencies
  - `build.bat` re-generates API Docs, build distribution archives, and uploads them to PyPi

### v2.2.0
- Add `currency` property to Character  
  - The `currency` property is a dictionary of all the currencies (e.g. NX) associated with the account that contains the character.
  - Dictionary keys: `mesos`, `nx`, `maplepoints`, `vp`, `dp`
- Add `characters` & `free_char_slots` properties to Account
  - `characters` is a list of the IGNs of all the characters in the account
  - `free_char_slots` is an integer representing the number of free character slots in the account

### v2.1.0
- Make the use of pre-underscores in variables consistent
  - Remove accessor for variables like _database_config 
  - These are now always be used with the pre-underscore internally
    - Reason: These variables should NOT be accessed manually when using Lazuli's API
  - These changes are not considered breaking, since the removed properties weren't intended to be manually accessed in the first place

### v2.0.1
- Fixed char image method in Character
  - Previously broken due to faulty refactor of Inventory instantiation

### v2.0.0
- Made Inventory lazy-instantiation by:
  - refactoring to a method in Lazuli, instead of Character
- Update unit test WRT breaking API changes

### v1.1.0
- Add getter methods that return all attributes together
- Made Inventory instantiation more efficient by reducing SQL calls

### v1.0.1
- Perform general linting

### v1.0.0
- Remove unnecessary checks
- Added checks to more setters
- Ready for release!

### v0.1.1
- Remove unused import statements (faulty refactor)
- Remove unnecessary casts causing Character.Meso and Character.EXP to fail
- Fix wrong column names in prepared statements causing setters to fail
- Add unit tests
- Fix unit test bugs

### v0.1.0
- Experimental fix for encoding issues
    - Tested working in CLI
    - To be tested for discord.py integration
- Refactor DB read-write functions for more *DRY*

### v0.0.9
- Fix type errors in meso and EXP setters
- Fix docstring (faulty refactor) in database module
- Add toggle option for GMs in ranking methods 

### v0.0.8
- Fix faulty refactor causing `get_char_by_name` and `get_account_by_username` to fail.
- Make `get_db_first_hit` more DRY

### v0.0.7
- Add utility function `extract_name_and_value`
- Add arg to ranking methods, for variable no. of players
- Add default value (5) for ranking methods' player count
- Make ranking methods extract values like level (not just name), using `extract_name_and_value`

### v0.0.6
- Migrate all **static** functions to utility module (breaking API change!)
- Migrate name extraction (from list of player data) to utility module
- Add ranking methods to Lazuli class
- Add `get_db_all_hits` utility function, for getting all DB matches
- Add `get_db_all_hits`` wrapper function in `database.Lazuli`
- Made `Lazuli::get_online_list` use `Lazuli::get_db_all_hits`

### v0.0.5
- Minor fix: type error for account instantiation
- Generate API Docs
- Feature: Fetch usernames of all players online

### v0.0.4
- Open up Discussions page
- Add docstrings

### v0.0.3
- Add inventory model

### v0.0.2  
- Add character model
- Add account model
  
### v0.0.1  
- Initialise project  
- Add database model (with placeholder for Account and Character objects)  
