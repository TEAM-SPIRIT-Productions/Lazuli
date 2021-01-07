## CHANGELOG:  

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
