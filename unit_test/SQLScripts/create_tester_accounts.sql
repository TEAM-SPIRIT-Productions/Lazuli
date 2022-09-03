-- Create admin tester account with Account ID of 90,001
INSERT INTO `accounts` (`id`, `name`, `password`, `2ndpassword`, `using2ndpassword`, 
`loggedin`, `banned`,`banreason`, `gm`, `nxCash`, `mPoints`, `vpoints`, `realcash`, `chrslot`)
VALUES (90001, 'tester0x00', 'test', '1111', 1, 0, 0, 'Lorem Ipsum', 0, 0, 0, 0, 0, 3)
ON DUPLICATE KEY UPDATE `name`='tester0x00', `password`='test', `2ndpassword`='1111', 
`using2ndpassword`=1, `loggedin`=0, `banned`=0,`banreason`='Lorem Ipsum', `gm`=0, `nxCash`=0, `mPoints`=0,
`vpoints`=0, `realcash`=0, `chrslot`=3;

-- Create admin tester account with Account ID of 90,002
INSERT INTO `accounts` (`id`, `name`, `password`, `2ndpassword`, `using2ndpassword`, 
`loggedin`, `banned`, `gm`, `nxCash`, `mPoints`, `vpoints`, `realcash`, `chrslot`)
VALUES (90002, 'tester0x01', 'test', '1111', 1, 0, 0, 0, 0, 0, 0, 0, 3)
ON DUPLICATE KEY UPDATE `name`='tester0x01', `password`='test', `2ndpassword`='1111', 
`using2ndpassword`=1, `loggedin`=1, `banned`=0, `gm`=0, `nxCash`=0, `mPoints`=0, 
`vpoints`=0, `realcash`=0, `chrslot`=3;

-- Create admin tester character with Character ID of 900,001
INSERT INTO `characters` (`id`, `accountid`, `name`, `level`, `str`, `dex`, `luk`, 
`int`, `hp`, `mp`, `maxhp`, `maxmp`, `hair`, `face`, `map`, `rankpoint`, `gp`, `soul`, `chatban`)
VALUES (900001, 90001, 'tester0x00', 249, 40, 4, 4, 
4, 500, 500, 500, 500, 36786, 23300, 253000000, 0, 0, 0, 'false')
ON DUPLICATE KEY UPDATE `accountid`=90001, `name`='tester0x00', `level`=10, `str`=40, `dex`=4, `luk`=4, 
`int`=4, `hp`=500, `mp`=500, `maxhp`=500, `maxmp`=500, `hair`=36786, `face`=23300, `map`=253000000, `rankpoint`=0, `gp`=0, `soul`=0, `chatban`='false';

-- Create admin tester character with Character ID of 900,002
INSERT INTO `characters` (`id`, `accountid`, `name`, `level`, `str`, `dex`, `luk`, 
`int`, `hp`, `mp`, `maxhp`, `maxmp`, `hair`, `face`, `map`, `rankpoint`, `gp`, `soul`, `chatban`)
VALUES (900002, 90002, 'tester0x01', 250, 40, 4, 4, 
4, 500, 500, 500, 500, 36786, 23300, 253000000, 0, 0, 0, 'false')
ON DUPLICATE KEY UPDATE `accountid`=90002, `name`='tester0x01', `level`=10, `str`=40, `dex`=4, `luk`=4, 
`int`=4, `hp`=500, `mp`=500, `maxhp`=500, `maxmp`=500, `hair`=36786, `face`=23300, `map`=253000000, `rankpoint`=0, `gp`=0, `soul`=0, `chatban`='false';

-- Allocate Inventory slots for character with Character ID of 900,001
INSERT INTO `inventoryslot` (`id`, `characterid`, `equip`, `use`, `setup`, `etc`, `cash`)
VALUES (900001, 900001, 96, 96, 96, 96, 60)
ON DUPLICATE KEY UPDATE `characterid`=900001, `equip`=96, `use`=96, `setup`=96, `etc`=96, `cash`=60;

-- Create equipped, cash equipped, equip, cash equip, use, cash use, etc, setup, cash
-- bagindex:  -1 Cap; -5 Overalls; -7 Boots; -8 Gloves; -9 Cape; -10 Shield; -11 Weapon
-- Equipped - WZ Hat
INSERT INTO `inventoryitems` (`inventoryitemid`, `type`, `characterid`, `itemid`, `inventorytype`, `position`, `quantity`, `GM_Log`, `uniqueid`)
VALUES (90000001, 1, 900001, 1002140, -1, -5, 1, 'KOOKIIE Tester', 90000001)
ON DUPLICATE KEY UPDATE  `type`=1, `characterid`=900001, `itemid`=1002140, `inventorytype`=-1, `position`=-1, `quantity`=1, `GM_Log`='KOOKIIE Tester', `uniqueid`=90000001;
-- Equip - WZ Hat; slot 1
INSERT INTO `inventoryitems` (`inventoryitemid`, `type`, `characterid`, `itemid`, `inventorytype`, `position`, `quantity`, `GM_Log`, `uniqueid`)
VALUES (90000002, 1, 900001, 1002140, 1, 1, 1, 'KOOKIIE Tester', 90000002)
ON DUPLICATE KEY UPDATE  `type`=1, `characterid`=900001, `itemid`=1002140, `inventorytype`=1, `position`=1, `quantity`=1, `GM_Log`='KOOKIIE Tester', `uniqueid`=90000002;

-- Equip stats for above 2 items
INSERT INTO `inventoryequipment` (`inventoryequipmentid`, `inventoryitemid`, `hpR`, `mpR`)
VALUES (90000001, 90000001, 0, 0)
ON DUPLICATE KEY UPDATE `inventoryitemid`=90000001, `hpR`=0, `mpR`=0;
INSERT INTO `inventoryequipment` (`inventoryequipmentid`, `inventoryitemid`, `hpR`, `mpR`)
VALUES (90000002, 90000002, 0, 0)
ON DUPLICATE KEY UPDATE `inventoryitemid`=90000002, `hpR`=0, `mpR`=0;
