## CHANGELOG:  

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
