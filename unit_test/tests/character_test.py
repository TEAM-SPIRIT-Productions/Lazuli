"""This is a unit test for checking basic Character handling functionality

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
def char():
	"""Returns a tester Character instance"""
	# Import DB
	try:
		azure = Lazuli()  # Use defaults - these should be the same as Azure v316 repository defaults
	except Exception as e:
		raise SystemExit(f"Error has occurred whist attempting to load DB: \n{e}")
	character = azure.get_char_by_name("tester0x00")
	if character is None:
		raise SystemExit("CRITICAL ERROR: UNABLE TO FETCH CHARACTER BY NAME! TERMINATING...")
	return character


# Character info fetching tests -------------------------------------------------------------------------------
@pytest.mark.parametrize("expected", ["tester0x00"])
def test_fetch_char_name(char, expected):
	assert char.name == expected, \
		f"Critical Error: Name test failed! Name: {char.name}; Type: {type(char.name)}"


@pytest.mark.parametrize("expected", [900001])
def test_fetch_char_id(char, expected):
	assert char.character_id == expected, \
		f"Critical Error: Character ID test failed! Name: {char.character_id}; Type: {type(char.character_id)}"


@pytest.mark.parametrize("expected", [90001])
def test_fetch_acc_id(char, expected):
	assert char.account_id == expected, \
		f"Critical Error: Account ID test failed! Name: {char.account_id}; Type: {type(char.account_id)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_mesos(char, expected):
	assert char.meso == expected, \
		f"Meso test failed! Meso count: {char.meso}; Type: {type(char.meso)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_fame(char, expected):
	assert char.fame == expected, \
		f"Fame test failed! Fame count: {char.fame}; Type: {type(char.fame)}"


@pytest.mark.parametrize("expected", ["Beginner"])
def test_fetch_char_class_name(char, expected):
	job = char.get_job_name()  # return job name from ID via Hashmap; String
	assert job == expected, \
		f"Job name test failed! Job name: {job}; Type: {type(job)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_class_id(char, expected):
	assert char.job == expected, \
		f"Job ID test failed! Job ID: {char.job}; Type: {type(char.job)}"


@pytest.mark.parametrize("expected", [10])
def test_fetch_char_level(char, expected):
	assert char.level == expected, \
		f"Character level test failed! Level count: {char.level}; Type: {type(char.level)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_honour(char, expected):
	assert char.honour == expected, \
		f"Honour EXP test failed! Honour count: {char.honour}; Type: {type(char.honour)}"


@pytest.mark.parametrize("expected", [253000000])
def test_fetch_char_map(char, expected):
	assert char.map == expected, \
		f"Map ID test failed! Map ID: {char.map}; Type: {type(char.map)}"


@pytest.mark.parametrize("expected", [23300])
def test_fetch_char_face(char, expected):
	assert char.face == expected, \
		f"Face ID test failed! Face ID: {char.face}; Type: {type(char.face)}"


@pytest.mark.parametrize("expected", [36786])
def test_fetch_char_hair(char, expected):
	assert char.hair == expected, \
		f"Hair ID test failed! Hair ID: {char.hair}; Type: {type(char.hair)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_skin(char, expected):
	assert char.skin == expected, \
		f"Skin ID test failed! Skin ID: {char.skin}; Type: {type(char.skin)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_exp(char, expected):
	assert char.exp == expected, \
		f"EXP test failed! EXP amount: {char.exp}; Type: {type(char.exp)}"


@pytest.mark.parametrize("expected", [40])
def test_fetch_char_str(char, expected):
	assert char.strength == expected, \
		f"STR test failed! STR amount: {char.strength}; Type: {type(char.strength)}"


@pytest.mark.parametrize("expected", [4])
def test_fetch_char_dex(char, expected):
	assert char.dex == expected, \
		f"DEX test failed! DEX amount: {char.dex}; Type: {type(char.dex)}"


@pytest.mark.parametrize("expected", [4])
def test_fetch_char_int(char, expected):
	assert char.inte == expected, \
		f"INT test failed! INT amount: {char.inte}; Type: {type(char.inte)}"


@pytest.mark.parametrize("expected", [4])
def test_fetch_char_luk(char, expected):
	assert char.luk == expected, \
		f"LUK test failed! LUK amount: {char.luk}; Type: {type(char.luk)}"


@pytest.mark.parametrize("expected", [{'str': 40, 'dex': 4, 'int': 4, 'luk': 4}])
def test_fetch_char_pri_stats(char, expected):
	primary_stats = char.get_primary_stats()  # returns a dictionary of the 4 main stats; dictionary
	assert primary_stats == expected, \
		f"Primary Stats test failed! \nExpected: expected \nEncountered: {primary_stats}"


@pytest.mark.parametrize("expected", [500])
def test_fetch_char_hp(char, expected):
	assert char.max_hp == expected, \
		f"HP test failed! HP amount: {char.max_hp}; Type: {type(char.max_hp)}"


@pytest.mark.parametrize("expected", [500])
def test_fetch_char_mp(char, expected):
	assert char.max_mp == expected, \
		f"MP test failed! MP amount: {char.max_mp}; Type: {type(char.max_mp)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_char_ap(char, expected):
	assert char.ap == expected, \
		f"AP test failed! AP amount: {char.ap}; Type: {type(char.ap)}"


@pytest.mark.parametrize("expected", [25])
def test_fetch_bl_slots(char, expected):
	assert char.bl_slots == expected, \
		f"Buddy List slots test failed! BL count: {char.bl_slots}; Type: {type(char.bl_slots)}"


@pytest.mark.parametrize("expected", [0])
def test_fetch_rbs(char, expected):
	assert char.rebirths == expected, \
		f"Rebirths test failed! RB count: {char.rebirths}; Type: {type(char.rebirths)}"


@pytest.mark.parametrize("expected", ["false"])
def test_fetch_mute(char, expected):
	assert char.mute == expected, \
		f"Mute test failed! Mute status: {char.mute}; Type: {type(char.mute)}"


@pytest.mark.parametrize("expected", [{
	'ambition': 0,
	'insight': 0,
	'willpower': 0,
	'diligence': 0,
	'empathy': 0,
	'charm': 0,
}])
def test_fetch_personality(char, expected):
	personality = {
		'ambition': char.ambition,
		'insight': char.insight,
		'willpower': char.willpower,
		'diligence': char.diligence,
		'empathy': char.empathy,
		'charm': char.charm,
	}  # There's no getter for the whole set right now; manually fetching
	assert personality == expected, \
		f"Personality trait test failed! Traits: {personality}; Type: {type(personality)}"


# Character info setting tests -------------------------------------------------------------------------------
@pytest.mark.parametrize("before, delta, expected", [
	("314159", 2827433, "3141592"),
])
def test_meso_changes(char, before, delta, expected):
	char.meso = before  # Sets money to 314,159 mesos in the database
	assert char.meso == before, \
		f"Meso setting test failed! Expected: {before}; Meso count: {char.meso}; Type: {type(char.meso)}"
	char.add_mesos(delta)  # Adds 2,827,433 to the current meso count, and saves to DB
	# character now has 3,141,592 mesos
	assert char.meso == expected, \
		f"Meso adding test failed! Expected: {expected}; Meso count: {char.meso}; Type: {type(char.meso)}"
	char.meso = "0"  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(3, 28, 31),
])
def test_fame_changes(char, before, delta, expected):
	char.fame = before  # Sets money to 314,159 mesos in the database
	assert char.fame == before, \
		f"Fame setting test failed! Expected: {before}; Fame count: {char.fame}; Type: {type(char.fame)}"
	char.add_fame(delta)  # Adds 28 fame to the existing count and saves to database
	# character fame is now 31
	assert char.fame == expected, \
		f"Fame adding test failed! Expected: {expected}; Fame count: {char.fame}; Type: {type(char.fame)}"
	char.fame = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(11, 20, 31),
])
def test_level_changes(char, before, delta, expected):
	char.level = before
	assert char.level == before, \
		f"Character level setting test failed! Expected: {before}; Level count: {char.level}; Type: {type(char.level)}"
	char.add_level(delta)  # Adds 21 to the existing count and saves to database
	# character is now level 31
	assert char.level == expected, \
		f"Character level adding test failed! Expected: {expected}; Level count: {char.level}; Type: {type(char.level)}"
	char.level = 10  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	(0, 100),
])
def test_job_changes(char, before, expected):
	char.job = expected  # set job ID to warrior
	assert char.job == expected, \
		f"Job ID setting test failed! Expected: {expected}; Job ID: {char.job}; Type: {type(char.job)}"
	char.job = before  # reset job ID to beginner


@pytest.mark.parametrize("before, expected", [
	("tester0x00", "KOOKIIE"),
])
def test_name_changes(char, before, expected):
	char.name = expected
	assert char.name == expected, \
		f"Name setting test failed! Expected: {expected}; Name: {char.name}; Type: {type(char.name)}"
	char.name = before  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	("253000000", "100000000"),
])
def test_map_changes(char, before, expected):
	char.map = expected
	assert char.map == expected, \
		f"Map ID setting test failed! Expected: {expected},{type(expected)}; Map ID: {char.map}; Type: {type(char.map)}"
	char.map = before  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	(23300, 20010),
])
def test_face_changes(char, before, expected):
	char.face = expected
	assert char.face == expected, \
		f"Face ID setting test failed! Expected: {expected}; Face ID: {char.face}; Type: {type(char.face)}"
	char.face = before  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	(36786, 30027),
])
def test_hair_changes(char, before, expected):
	char.hair = expected
	assert char.hair == expected, \
		f"Hair ID setting test failed! Expected: {expected}; Hair ID: {char.hair}; Type: {type(char.hair)}"
	char.hair = before  # reset to baseline


@pytest.mark.parametrize("before, expected", [
	(0, 2),
])
def test_skin_changes(char, before, expected):
	char.skin = expected
	assert char.skin == expected, \
		f"Skin ID setting test failed! Expected: {expected}; Skin ID: {char.skin}; Type: {type(char.skin)}"
	char.skin = before  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	("314159", 2827433, "3141592"),
])
def test_exp_changes(char, before, delta, expected):
	char.exp = before
	assert char.exp == before, \
		f"EXP test setting failed! Expected: {before}; EXP amount: {char.exp}; Type: {type(char.exp)}"
	char.add_exp(delta)
	assert char.exp == expected, \
		f"EXP test adding failed! Expected: {expected}; EXP amount: {char.exp}; Type: {type(char.exp)}"
	char.exp = "0"  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_str_changes(char, before, delta, expected):
	char.strength = before
	assert char.strength == before, \
		f"STR setting test failed! Expected: {before}; STR amount: {char.strength}; Type: {type(char.strength)}"
	char.add_str(delta)
	assert char.strength == expected, \
		f"STR adding test failed! Expected: {expected}; STR amount: {char.strength}; Type: {type(char.strength)}"
	char.strength = 40  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_dex_changes(char, before, delta, expected):
	char.dex = before
	assert char.dex == before, \
		f"DEX setting test failed! Expected: {before}; DEX amount: {char.dex}; Type: {type(char.dex)}"
	char.add_dex(delta)
	assert char.dex == expected, \
		f"DEX adding test failed! Expected: {expected}; DEX amount: {char.dex}; Type: {type(char.dex)}"
	char.dex = 4  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_int_changes(char, before, delta, expected):
	char.inte = before
	assert char.inte == before, \
		f"INT setting test failed! Expected: {before}; INT amount: {char.inte}; Type: {type(char.inte)}"
	char.add_inte(delta)
	assert char.inte == expected, \
		f"INT adding test failed! Expected: {expected}; INT amount: {char.inte}; Type: {type(char.inte)}"
	char.inte = 4  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_luk_changes(char, before, delta, expected):
	char.luk = before
	assert char.luk == before, \
		f"LUK setting test failed! Expected: {before}; LUK amount: {char.luk}; Type: {type(char.luk)}"
	char.add_luk(delta)
	assert char.luk == expected, \
		f"LUK adding test failed! Expected: {expected}; LUK amount: {char.luk}; Type: {type(char.luk)}"
	char.luk = 4  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_hp_changes(char, before, delta, expected):
	char.max_hp = before
	assert char.max_hp == before, \
		f"HP setting test failed! Expected: {before}; HP amount: {char.max_hp}; Type: {type(char.max_hp)}"
	char.add_max_hp(delta)
	assert char.max_hp == expected, \
		f"HP adding test failed! Expected: {expected}; HP amount: {char.max_hp}; Type: {type(char.max_hp)}"
	char.max_hp = 500  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_mp_changes(char, before, delta, expected):
	char.max_mp = before
	assert char.max_mp == before, \
		f"MP setting test failed! Expected: {before}; MP amount: {char.max_mp}; Type: {type(char.max_mp)}"
	char.add_max_mp(delta)
	assert char.max_mp == expected, \
		f"MP adding test failed! Expected: {expected}; MP amount: {char.max_mp}; Type: {type(char.max_mp)}"
	char.max_mp = 500  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_ap_changes(char, before, delta, expected):
	char.ap = before
	assert char.ap == before, \
		f"AP setting test failed! Expected: {before}; AP amount: {char.ap}; Type: {type(char.ap)}"
	char.add_ap(delta)
	assert char.ap == expected, \
		f"AP adding test failed! Expected: {expected}; AP amount: {char.ap}; Type: {type(char.ap)}"
	char.ap = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_bl_slots_changes(char, before, delta, expected):
	char.bl_slots = before
	assert char.bl_slots == before, \
		f"BL Slots setting test failed! Expected: {before}; BL count: {char.bl_slots}; Type: {type(char.bl_slots)}"
	char.add_bl_slots(delta)
	assert char.bl_slots == expected, \
		f"BL Slots adding test failed! Expected: {expected}; BL count: {char.bl_slots}; Type: {type(char.bl_slots)}"
	char.bl_slots = 25  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	(31, 1, 32),
])
def test_rb_changes(char, before, delta, expected):
	char.rebirths = before
	assert char.rebirths == before, \
		f"Rebirths setting test failed! Expected: {before}; RB count: {char.rebirths}; Type: {type(char.rebirths)}"
	char.add_rebirths(delta)
	assert char.rebirths == expected, \
		f"Rebirths adding test failed! Expected: {expected}; RB count: {char.rebirths}; Type: {type(char.rebirths)}"
	char.rebirths = 0  # reset to baseline


@pytest.mark.parametrize("before, delta, expected", [
	{
		'ambition': 10,
		'insight': 10,
		'willpower': 10,
		'diligence': 10,
		'empathy': 10,
		'charm': 10,
	},
	21,
	{
		'ambition': 31,
		'insight': 31,
		'willpower': 31,
		'diligence': 31,
		'empathy': 31,
		'charm': 31,
	},
])
def test_personality_changes(char, before, delta, expected):
	char.ambition = before['ambition']
	char.insight = before['insight']
	char.willpower = before['willpower']
	char.diligence = before['diligence']
	char.empathy = before['empathy']
	char.charm = before['charm']
	personality = {
		'ambition': char.ambition,
		'insight': char.insight,
		'willpower': char.willpower,
		'diligence': char.diligence,
		'empathy': char.empathy,
		'charm': char.charm,
	}  # There's no getter for the whole set right now; manually fetching
	assert personality == before, \
		f"Personality trait setting test failed!\nExpected: {personality};\n" \
		f"Traits: {personality}; Type: {type(personality)}"
	char.add_ambition(delta)
	char.add_insight(delta)
	char.add_willpower(delta)
	char.add_diligence(delta)
	char.add_empathy(delta)
	char.add_charm(delta)
	personality = {
		'ambition': char.ambition,
		'insight': char.insight,
		'willpower': char.willpower,
		'diligence': char.diligence,
		'empathy': char.empathy,
		'charm': char.charm,
	}  # Because: grabbing by value and not by reference
	assert personality == expected, \
		f"Personality trait adding test failed!\nExpected: {personality};\n" \
		f"Traits: {personality}; Type: {type(personality)}"
	# reset to baseline:
	char.ambition = 0
	char.insight = 0
	char.willpower = 0
	char.diligence = 0
	char.empathy = 0
	char.charm = 0


@pytest.mark.parametrize("before, expected", [
	("false", "true"),
])
def test_mute_changes(char, before, expected):
	char.mute = expected
	assert char.mute == expected, \
		f"Mute setting test failed! Expected: {expected}; Mute status: {char.mute}; Type: {type(char.mute)}"
	char.mute = before  # reset to baseline
