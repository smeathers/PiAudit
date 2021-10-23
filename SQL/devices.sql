CREATE TABLE `devices` (
  `serial` char(16) NOT NULL,
  `hardware` varchar(10) DEFAULT NULL,
  `revision` varchar(10) DEFAULT NULL,
  `model` varchar(45) DEFAULT NULL,
  `ram` int(11) DEFAULT NULL,
  `wifi_mac` char(17) DEFAULT NULL,
  `eth_mac` char(17) DEFAULT NULL,
  `blu_mac` char(17) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `detect_count` int(11) NOT NULL DEFAULT '1',
  `datetime_last_seen_utc` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Used to record info on Raspberry Pi devices'
