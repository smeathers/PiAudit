DELIMITER //
CREATE PROCEDURE `insert_device`(
IN pSerial char(16),
IN pHardware varchar(10),
IN pRevision varchar(10),
IN pModel varchar(45),
IN pRam int,
IN pEth_mac char(17),
IN pWifi_mac char(17)
)
BEGIN
	INSERT INTO devices	(serial, hardware, revision, model, ram, wifi_mac, eth_mac)
	VALUES (pSerial,
            pHardware,
            pRevision,
            pModel,
            pRam,
            pWifi_mac,
            pEth_mac)
    ON DUPLICATE KEY UPDATE
		Wifi_mac = pWifi_mac,
        Eth_mac = pEth_mac,
		detect_count = detect_count + 1,
		datetime_last_seen_utc = CURRENT_TIMESTAMP;
            
END//
DELIMITER ;
