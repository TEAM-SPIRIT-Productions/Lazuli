"""This is a unit test for checking basic Inventory handling functionality

NOTE: PLACE THE UNIT TEST FILES IN THE ROOT OF THE REPOSITORY!
Kindly set up the DB for use; refer to the AzureMS repository on how to set up
an Azure-based DB. Then, use the script in the unit_test/SQLScripts folder of this
project to create a tester account. Once it's been successfully run, you can
use this script to test the functionality of Lazuli's APIs.
Note that you may re-run the SQL script to reset all tester accounts
and characters to their baseline values, if desired.
Copyright KOOKIIE Studios 2020. All rights reserved.
"""
import pytest
from lazuli.database import Lazuli


@pytest.fixture
def inventory():
	"""Returns a tester Inventory instance"""
	# Import DB
	try:
		azure = Lazuli()  # Use defaults - these should be the same as Azure v316 repository defaults
	except Exception as e:
		raise SystemExit(f"Error has occurred whist attempting to load DB: \n{e}")
	character = azure.get_char_by_name("tester0x00")
	if character is None:
		raise SystemExit("CRITICAL ERROR: UNABLE TO FETCH CHARACTER BY NAME! TERMINATING...")

	inventory = character.inventory
	return inventory


# Inventory info fetching tests -------------------------------------------------------------------------------
# Test non-cash equipped
@pytest.mark.parametrize("slot, item_id, qty", [(-1, 1002140, 1)])
def test_fetch_equipped_item(inventory, slot, item_id, qty):
	assert inventory.equipped_inv[slot]['itemid'] == item_id,  \
		f"Error encountered whilst directly fetching item ID from bagindex: \n" \
		f"Expected: {item_id} ({type(item_id)}); Encountered: {inventory.equipped_inv[slot]['itemid']}, " \
		f"Type: {type(inventory.equipped_inv[slot]['itemid'])}"

	assert inventory.equipped_inv[slot]['quantity'] == qty,  \
		f"Error encountered whilst directly fetching item qty from bagindex: \n" \
		f"Expected: {qty} ({type(qty)}); Encountered: {inventory.equipped_inv[slot]['quantity']}, " \
		f"Type: {type(inventory.equipped_inv[slot]['quantity'])}"


@pytest.mark.parametrize("item_id, wrong_id , status", [(1002140, 1002141, True)])
def test_is_equipped(inventory, item_id, wrong_id, status):
	assert inventory.is_equipping(item_id), \
		f"Error encountered whilst checking if non-cash equip is worn: \n" \
		f"Expected: {status} ({type(status)}); Encountered: {inventory.is_equipping(item_id)}, " \
		f"Type: {type(inventory.is_equipping(item_id))}"
	assert not inventory.is_equipping(wrong_id), \
		f"Error encountered whilst checking for false positives, for whether non-cash equip is worn: \n" \
		f"Expected: {not status} ({type(not status)}); Encountered: {inventory.is_equipping(wrong_id)}, " \
		f"Type: {type(inventory.is_equipping(wrong_id))}"


# Test non-cash equip
@pytest.mark.parametrize("slot, item_id, qty", [(1, 1002140, 1)])
def test_fetch_equip_item(inventory, slot, item_id, qty):
	assert inventory.equip_inv[slot]['itemid'] == item_id,  \
		f"Error encountered whilst directly fetching item ID from bagindex: \n" \
		f"Expected: {item_id} ({type(item_id)}); Encountered: {inventory.equip_inv[slot]['itemid']}, " \
		f"Type: {type(inventory.equip_inv[slot]['itemid'])}"

	assert inventory.equip_inv[slot]['quantity'] == qty,  \
		f"Error encountered whilst directly fetching item qty from bagindex: \n" \
		f"Expected: {qty} ({type(qty)}); Encountered: {inventory.equip_inv[slot]['quantity']}, " \
		f"Type: {type(inventory.equip_inv[slot]['quantity'])}"


@pytest.mark.parametrize("item_id, wrong_id , status", [(1002140, 1002141, True)])
def test_is_in_equip(inventory, item_id, wrong_id, status):
	assert inventory.has_item_in_equip(item_id), \
		f"Error encountered whilst checking if non-cash equip is in inventory: \n" \
		f"Expected: {status} ({type(status)}); Encountered: {inventory.has_item_in_equip(item_id)}, " \
		f"Type: {type(inventory.has_item_in_equip(item_id))}"
	assert not inventory.has_item_in_equip(wrong_id), \
		f"Error encountered whilst checking for false positives, for whether non-cash equip is in inventory: \n" \
		f"Expected: {not status} ({type(not status)}); Encountered: {inventory.has_item_in_equip(wrong_id)}, " \
		f"Type: {type(inventory.has_item_in_equip(wrong_id))}"

# Other tabs truncated for being the exact same logic as equip tab, in the engine
# No Inventory setting tests - setting inventory is out of scope!
