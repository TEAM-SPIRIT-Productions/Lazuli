## CHANGELOG:  

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
