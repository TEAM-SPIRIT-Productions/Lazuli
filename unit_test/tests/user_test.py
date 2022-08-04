"""This is a unit test for checking basic User handling functionality

NOTE: PLACE THE UNIT TEST FILES IN THE ROOT OF THE REPOSITORY!
Kindly set up the DB for use; refer to the AzureMS repository on how to set up
an Azure-based DB. Then, use the script in the unit_test/SQLScripts folder of this
project to create a tester account. Once it's been successfully run, you can
use this script to test the functionality of Lazuli's APIs.
Note that you may re-run the SQL script to reset all tester accounts
and characters to their baseline values, if desired.
Copyright KOOKIIE Studios 2022. All rights reserved.
"""
import pytest
from lazuli.database import Lazuli


#  Test one method of fetching user, and use the other as fixture
def test_direct_user_fetch():
	"""Returns a tester Account instance"""
	# Import DB
	try:
		azure = Lazuli()  # Use defaults - these should be the same as Azure v316 repository defaults
	except Exception as e:
		raise SystemExit(f"Error has occurred whist attempting to load DB: \n{e}")
	user = azure.get_account_by_username("tester0x00")
	# Account ID test is here:
	assert user.account_id == 90001,\
		f"Error encountered whilst fetching Account by Username:\n" \
		f"Expected: 90001 (Int); Encountered: {user.user_id}, Type: {type(user.user_id)}"


@pytest.fixture
def user():
	"""Returns a tester Account instance"""
	# Import DB
	try:
		azure = Lazuli()  # Use defaults - these should be the same as Azure v316 repository defaults
	except Exception as e:
		raise SystemExit(f"Error has occurred whist attempting to load DB: \n{e}")

	char_obj = azure.get_char_by_name("tester0x00")
	if char_obj is None:
		raise SystemExit("CRITICAL ERROR: UNABLE TO FETCH CHARACTER BY NAME! TERMINATING...")

	user_obj = char_obj.account  # Get user from Char object
	if user_obj is None:
		raise SystemExit("CRITICAL ERROR: UNABLE TO FETCH ACCOUNT FROM CHARACTER! TERMINATING...")
	return user_obj


# User info fetching tests -------------------------------------------------------------------------------
@pytest.mark.parametrize("expected", ["tester0x00"])
def test_fetch_acc_name(user, expected):
	assert user.username == expected, \
		f"Critical Error: Name test failed! Name: {user.username}; Type: {type(user.username)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_login_status(user, expected):
	assert user.logged_in == expected, \
		f"Login Status test failed! Status: {user.logged_in}; Type: {type(user.logged_in)}"
	assert user.is_online() is False, \
		f"Login Status (is_online() method) test failed! Status: {user.is_online()}; Type: {type(user.is_online())}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_ban_status(user, expected):
	assert user.banned == expected, \
		f"Ban Status test failed! Status: {user.banned}; Type: {type(user.banned)}"


@pytest.mark.parametrize("expected", ["Lorem Ipsum"])
def test_fetch_ban_reason(user, expected):
	assert user.ban_reason == expected, \
		f"Ban Reason test failed!: Expected: {expected} ({type(expected)});\n" \
		f"Encountered: {user.ban_reason}, Type: {type(user.ban_reason)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_donor_points(user, expected):
	assert user.dp == expected, \
		f"DP test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.dp}, Type: {type(user.dp)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_maple_points(user, expected):
	assert user.maple_points == expected, \
		f"Maple Points test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.maple_points}, Type: {type(user.maple_points)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_vote_points(user, expected):
	assert user.vp == expected, \
		f"Vote Points test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.vp}, Type: {type(user.vp)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_nx(user, expected):
	assert user.nx == expected, \
		f"NX test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.nx}, Type: {type(user.nx)}"


@pytest.mark.parametrize("expected", [3])
def test_fetch_char_slots(user, expected):
	assert user.char_slots == expected, \
		f"Character Slot test failed!\nExpected: {expected} ({type(expected)});\n" \
		f"Encountered: {user.char_slots}, Type: {type(user.char_slots)}"


# User info setting tests -------------------------------------------------------------------------------
@pytest.mark.parametrize("before, expected", [
	("tester0x00", "tester0xFF"),
])
def test_name_changes(user, before, expected):
	user.username = expected
	assert user.username == expected, \
		f"Name setting test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.username}, Type: {type(user.username)}"
	user.username = before  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	(0, 1),
])
def test_unstuck(user, before, expected):
	user.logged_in = expected
	assert user.logged_in == expected, \
		f"Login status setting test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.logged_in}, Type: {type(user.logged_in)}"
	user.unstuck()
	assert user.logged_in == before, \
		f"Unstuck test failed!\n" \
		f"Expected: {before} ({type(before)}); Encountered: {user.logged_in}, Type: {type(user.logged_in)}"
	user.logged_in = before  # reset to baseline, just in case


@pytest.mark.parametrize("before, expected", [
	(0, 1),
])
def test_ban_changes(user, before, expected):
	user.banned = expected
	assert user.banned == expected, \
		f"Ban status setting test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.banned}, Type: {type(user.banned)}"
	user.banned = before  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	("Lorem Ipsum", "dolor sit amet"),
])
def test_ban_reason_changes(user, before, expected):
	user.ban_reason = expected
	assert user.ban_reason == expected, \
		f"Ban Reason setting test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.ban_reason}, Type: {type(user.ban_reason)}"
	user.ban_reason = before  # reset to baseline


# Password change function omitted from checks - insecure function! Deprecated!


@pytest.mark.parametrize("before, delta, expected", [
	(314159, 2827433, 3141592),
])
def test_dp_changes(user, before, delta, expected):
	user.dp = before
	assert user.dp == before, \
		f"DP setting test failed!\n" \
		f"Expected: {before} ({type(before)}); Encountered: {user.dp}, Type: {type(user.dp)}"
	user.add_dp(delta)
	assert user.dp == expected, \
		f"DP count adding test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.dp}, Type: {type(user.dp)}"
	user.dp = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(314159, 2827433, 3141592),
])
def test_maple_points_changes(user, before, delta, expected):
	user.maple_points = before
	assert user.maple_points == before, \
		f"Maple Points setting test failed!\n" \
		f"Expected: {before} ({type(before)}); Encountered: {user.maple_points}, Type: {type(user.maple_points)}"
	user.add_maple_points(delta)
	assert user.maple_points == expected, \
		f"Maple Points adding test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.maple_points}, Type: {type(user.maple_points)}"
	user.maple_points = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(314159, 2827433, 3141592),
])
def test_vp_changes(user, before, delta, expected):
	user.vp = before
	assert user.vp == before, \
		f"VP setting test failed!\n" \
		f"Expected: {before} ({type(before)}); Encountered: {user.vp}, Type: {type(user.vp)}"
	user.add_vp(delta)
	assert user.vp == expected, \
		f"VP adding test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.vp}, Type: {type(user.vp)}"
	user.vp = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(314159, 2827433, 3141592),
])
def test_nx_changes(user, before, delta, expected):
	user.nx = before
	assert user.nx == before, \
		f"VP setting test failed!\n" \
		f"Expected: {before} ({type(before)}); Encountered: {user.nx}, Type: {type(user.nx)}"
	user.add_nx(delta)
	assert user.nx == expected, \
		f"VP adding test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.nx}, Type: {type(user.nx)}"
	user.nx = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(10, 21, 31),
])
def test_char_slot_changes(user, before, delta, expected):
	user.char_slots = before
	assert user.char_slots == before, \
		f"Character Slot setting test failed!\n" \
		f"Expected: {before} ({type(before)}); Encountered: {user.char_slots}, Type: {type(user.char_slots)}"
	user.add_char_slots(delta)
	assert user.char_slots == expected, \
		f"Character Slot adding test failed!\n" \
		f"Expected: {expected} ({type(expected)}); Encountered: {user.char_slots}, Type: {type(user.char_slots)}"
	user.char_slots = 3  # reset to baseline
