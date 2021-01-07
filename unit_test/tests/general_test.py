"""This is a unit test for checking basic general handling functionality

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
def azure():
	"""Returns a database instance"""
	# Import DB
	try:
		database_object = Lazuli()  # Use defaults - these should be the same as Azure v316 repository defaults
	except Exception as e:
		raise SystemExit(f"Error has occurred whist attempting to load DB: \n{e}")
	return database_object


# General functional testing -------------------------------------------------------------------------------
@pytest.mark.parametrize("expected", [1])
def test_fetch_online_count(azure, expected):
	assert azure.get_online_count() == expected, \
		f"Online count test failed! Count: {azure.get_online_count()}; Type: {type(azure.get_online_count())}"


@pytest.mark.parametrize("expected", [["tester0x01"]])
def test_fetch_online_players(azure, expected):
	assert azure.get_online_players() == expected, \
		f"Online count test failed! Players: {azure.get_online_players()}; Type: {type(azure.get_online_players())}"


@pytest.mark.parametrize("expected_1st, expected_2nd", [("tester0x01", "tester0x00")])
def test_level_ranking(azure, expected_1st, expected_2nd):
	assert azure.get_level_ranking()[0][0] == expected_1st, \
		f"Level Ranking test failed! Player: {azure.get_level_ranking()[0]}; Type: {type(azure.get_level_ranking()[0][0])}"
	assert azure.get_level_ranking()[1][0] == expected_2nd, \
		f"Level Ranking test failed! Player: {azure.get_level_ranking()[1]}; Type: {type(azure.get_level_ranking()[1][0])}"

# Other general methods omitted for being the exact same logic in the engine
