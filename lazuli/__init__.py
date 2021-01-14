"""This is the init file for the package - Compiled by KOOKIIE

Copyright 2020 TEAM SPIRIT. All rights reserved.
Use of this source code is governed by a AGPL-style license that can be found
in the LICENSE file. This module provides a dictionary mapping all Job IDs
to their respective Job names.

All efforts have been made to trace Job IDs in both GMS and KMS accurately.
Notable ommissions (Plase contribute if you have their Job IDs):
 - SAO Classes: Kirito, Asuna, Leafa
 - Sengoku Class (Special): Ayame
 - Explorer Class (Special): Zen
"""
JOBS = {
	# Explorer Classes (Aventurer in MSEA)
	'0': 'Beginner',

	# Explorer Warrior
	'100': 'Warrior',  # Explorer Warrior 1 (Common)
	'110': 'Fighter',
	'111': 'Crusader',
	'112': 'Hero',

	'120': 'Page',
	'121': 'White Knight',
	'122': 'Paladin',

	'130': 'Spearman',
	'131': 'Dragon Knight',
	'132': 'Dark Knight',

	# Explorer Mage
	'200': 'Magician',  # Explorer Mage 1 (Common)
	'210': 'Fire Poison Wizard',
	'211': 'Fire Poison Mage',
	'212': 'Fire Poison Archmage',

	'220': 'Ice Lightning Wizard',
	'221': 'Ice Lightning Mage',
	'222': 'Ice Lightning Archmage',

	'230': 'Cleric',
	'231': 'Priest',
	'232': 'Bishop',

	# Explorer Bowmen
	'300': 'Archer',  # Explorer Bowman 1 (Common)
	'310': 'Hunter',
	'311': 'Ranger',
	'312': 'Bowmaster',

	'320': 'Cross Bowman',
	'321': 'Sniper',
	'322': 'Marksman',

	# Special Explorer: Pathfinder
	'301': 'Pathfinder',  # PF 1 - Not sure why they broke their own conventions
	'330': 'Pathfinder',  # PF 2
	'331': 'Pathfinder',  # PF 3
	'332': 'Pathfinder',  # PF 4

	# Explorer Thieves
	'400': 'Rogue',  # Explorer Thieves 1 (Common)
	'410': 'Assassin',
	'411': 'Hermit',
	'412': 'Night Lord',

	'420': 'Bandit',
	'421': 'Chief Bandit',
	'422': 'Shadower',

	# Special Explorer: Dual Blades
	'430': 'Blade Recruit',
	'431': 'Blade Acolyte',
	'432': 'Blade Specialist',
	'433': 'Blade Lord',
	'434': 'Blade Master',

	# Explorer Pirates
	'500': 'Pirate',  # Explorer Pirates 1 (Common)
	'510': 'Brawler',
	'511': 'Marauder',
	'512': 'Buccaneer',  # (aka Viper in MSEA/KMS)

	'520': 'Gunslinger',
	'521': 'Outlaw',
	'522': 'Corsair',

	# Special Explorer: Canonneer
	'501': 'Cannon Shooter',
	'530': 'Cannoneer',
	'531': 'Cannon Trooper',
	'532': 'Cannon Master',

	# Special Explorer: Jett
	'508': 'Jett',  # Jett 1 - Not sure why they broke their own conventions
	'570': 'Jett',  # Jett 2
	'571': 'Jett',  # Jett 3
	'572': 'Jett',  # Jett 4

	# KoC Classes
	'1000': 'Noblesse',  # KoC Beginner

	# Soul Master in MSEA/KMS
	'1100': 'Dawn Warrior',  # DW 1
	'1110': 'Dawn Warrior',  # DW 2
	'1111': 'Dawn Warrior',  # DW 3
	'1112': 'Dawn Warrior',  # DW 4

	# Flame Wizard in MSEA/KMS
	'1200': 'Blaze Wizard',  # BW 1
	'1210': 'Blaze Wizard',  # BW 2
	'1211': 'Blaze Wizard',  # BW 3
	'1212': 'Blaze Wizard',  # BW 4

	# Wind Breaker in MSEA/KMS
	'1300': 'Wind Archer',  # WA 1
	'1310': 'Wind Archer',  # WA 2
	'1311': 'Wind Archer',  # WA 3
	'1312': 'Wind Archer',  # WA 4

	'1400': 'Night Walker',  # NW 1
	'1410': 'Night Walker',  # NW 2
	'1411': 'Night Walker',  # NW 3
	'1412': 'Night Walker',  # NW 4

	# Striker in MSEA/KMS
	'1500': 'Thunder Breaker',  # TB 1
	'1510': 'Thunder Breaker',  # TB 2
	'1511': 'Thunder Breaker',  # TB 3
	'1512': 'Thunder Breaker',  # TB 4

	# Heroes of Maple/Legends Classes
	# The 6 Hero classes (M, A, P, L, E, S) have 200X beginner job IDs
	'2000': 'Aran',  # Aran Beginner (aka Legend)
	'2100': 'Aran',  # Aran 1
	'2110': 'Aran',  # Aran 2
	'2111': 'Aran',  # Aran 3
	'2112': 'Aran',  # Aran 4

	'2001': 'Evan',  # Evan Beginner
	'2200': 'Evan',  # Evan 1
	'2210': 'Evan',  # Evan 2
	'2211': 'Evan',  # Evan 3
	'2212': 'Evan',  # Evan 4
	'2213': 'Evan',  # Evan 5
	'2214': 'Evan',  # Evan 6
	'2215': 'Evan',  # Evan 7
	'2216': 'Evan',  # Evan 8
	'2217': 'Evan',  # Evan 9
	'2218': 'Evan',  # Evan 10

	'2002': 'Mercedes',  # Mercedes Beginner
	'2300': 'Mercedes',  # Mercedes 1
	'2310': 'Mercedes',  # Mercedes 2
	'2311': 'Mercedes',  # Mercedes 3
	'2312': 'Mercedes',  # Mercedes 4

	'2003': 'Phantom',  # Phantom Beginner
	'2400': 'Phantom',  # Phantom 1
	'2410': 'Phantom',  # Phantom 2
	'2411': 'Phantom',  # Phantom 3
	'2412': 'Phantom',  # Phantom 4

	# Eunwol in MSEA/KMS
	'2005': 'Shade',  # Shade Beginner
	'2500': 'Shade',  # Shade 1
	'2510': 'Shade',  # Shade 2
	'2511': 'Shade',  # Shade 3
	'2512': 'Shade',  # Shade 4

	'2004': 'Luminous',  # Luminous Beginner
	'2700': 'Luminous',  # Luminous 1
	'2710': 'Luminous',  # Luminous 2
	'2711': 'Luminous',  # Luminous 3
	'2712': 'Luminous',  # Luminous 4

	# Resistance Classes
	'3000': 'Citizen',  # Non-Demon/Xenon Resistance

	# Resistance classes have 300X beginner job IDs
	# Demon classes Beginner (Demons have their own beginner classes)
	'3001': 'Demon',
	'3100': 'Demon Slayer',  # DS 1
	'3110': 'Demon Slayer',  # DS 2
	'3111': 'Demon Slayer',  # DS 3
	'3112': 'Demon Slayer',  # DS 4

	'3101': 'Demon Avenger',  # DA 1
	'3120': 'Demon Avenger',  # DA 2
	'3121': 'Demon Avenger',  # DA 3
	'3122': 'Demon Avenger',  # DA 4

	'3200': 'Battle Mage',  # BaM 1
	'3210': 'Battle Mage',  # BaM 2
	'3211': 'Battle Mage',  # BaM 3
	'3212': 'Battle Mage',  # BaM 4

	'3300': 'Wild Hunter',  # WH 1
	'3310': 'Wild Hunter',  # WH 2
	'3311': 'Wild Hunter',  # WH 3
	'3312': 'Wild Hunter',  # WH 4

	'3500': 'Mechanic',  # Mech 1
	'3510': 'Mechanic',  # Mech 2
	'3511': 'Mechanic',  # Mech 3
	'3512': 'Mechanic',  # Mech 4

	'3002': 'Xenon',  # Xenon Beginner (Xenons have their own beginner class)
	'3600': 'Xenon',  # Xenon 1
	'3610': 'Xenon',  # Xenon 2
	'3611': 'Xenon',  # Xenon 3
	'3612': 'Xenon',  # Xenon 4

	'3700': 'Blaster',  # Blaster 1
	'3710': 'Blaster',  # Blaster 1
	'3711': 'Blaster',  # Blaster 1
	'3712': 'Blaster',  # Blaster 1

	# Sengoku Classes
	# Sengoku classes have 400X beginner job IDs
	'4001': 'Hayato',  # Hayato Beginner
	'4100': 'Hayato',  # Hayato 1
	'4110': 'Hayato',  # Hayato 2
	'4111': 'Hayato',  # Hayato 3
	'4112': 'Hayato',  # Hayato 4

	'4002': 'Kanna',  # Kanna Beginner
	'4200': 'Kanna',  # Kanna 1
	'4210': 'Kanna',  # Kanna 2
	'4211': 'Kanna',  # Kanna 3
	'4212': 'Kanna',  # Kanna 4

	# Special KoC
	'5000': 'Mihile',  # Mihile Beginner (aka Nameless Warden)
	'5100': 'Mihile',  # Mihile 1
	'5110': 'Mihile',  # Mihile 2
	'5111': 'Mihile',  # Mihile 3
	'5112': 'Mihile',  # Mihile 4

	# Nova Classes
	'6000': 'Kaiser',  # Kaiser Beginner
	'6100': 'Kaiser',  # Kaiser 1
	'6110': 'Kaiser',  # Kaiser 2
	'6111': 'Kaiser',  # Kaiser 3
	'6112': 'Kaiser',  # Kaiser 4

	'6001': 'Angelic Buster',  # AB Beginner
	'6500': 'Angelic Buster',  # AB 1
	'6510': 'Angelic Buster',  # AB 2
	'6511': 'Angelic Buster',  # AB 3
	'6512': 'Angelic Buster',  # AB 4

	'6002': 'Cadena',  # Cadena Beginner
	'6400': 'Cadena',  # Cadena 1
	'6410': 'Cadena',  # Cadena 2
	'6411': 'Cadena',  # Cadena 3
	'6412': 'Cadena',  # Cadena 4

	# Child of God Classes
	'10000': 'Zero',  # Zero Beginner
	'10100': 'Zero',  # Zero 1
	'10110': 'Zero',  # Zero 2
	'10111': 'Zero',  # Zero 3
	'10112': 'Zero',  # Zero 4

	# Child of Furry Classes
	'11000': 'Beast Tamer',  # Beast Tamer Beginner
	'11200': 'Beast Tamer',  # Beast Tamer 1
	'11210': 'Beast Tamer',  # Beast Tamer 2
	'11211': 'Beast Tamer',  # Beast Tamer 3
	'11212': 'Beast Tamer',  # Beast Tamer 4

	# Special: Kinesis
	'14000': 'Kinesis',  # Kinesis Beginner
	'14200': 'Kinesis',  # Kinesis 1
	'14210': 'Kinesis',  # Kinesis 2
	'14211': 'Kinesis',  # Kinesis 3
	'14212': 'Kinesis',  # Kinesis 4

	# Flora Classes
	'15000': 'Illium',  # Illium Beginner
	'15200': 'Illium',  # Illium 1
	'15210': 'Illium',  # Illium 2
	'15211': 'Illium',  # Illium 3
	'15212': 'Illium',  # Illium 4

	'15001': 'Ark',  # Ark Beginner
	'15500': 'Ark',  # Ark 1
	'15510': 'Ark',  # Ark 2
	'15511': 'Ark',  # Ark 3
	'15512': 'Ark',  # Ark 4

	'15002': 'Adele',  # Adele Beginner
	'15100': 'Adele',  # Adele 1
	'15110': 'Adele',  # Adele 2
	'15112': 'Adele',  # Adele 3
	'15111': 'Adele',  # Adele 4

	# Anima Classes
	'16000': 'Hoyoung',  # Hoyoung Beginner
	'16400': 'Hoyoung',  # Hoyoung 1
	'16410': 'Hoyoung',  # Hoyoung 2
	'16411': 'Hoyoung',  # Hoyoung 3
	'16412': 'Hoyoung',  # Hoyoung 4

	# Special jobs
	'800': 'Manager',
	'900': 'GM',
	'910': 'Super GM',
	'9000': 'Additional Skills',
	'40000': 'V-Skills',

	# Special: Pink Bean
	'13000': 'Pink Bean',  # Pink Bean Beginner
	'13100': 'Pink Bean',  # Pink Bean 1
}
