# PiAudit
A simple project to audit my collection of Raspberry Pis.

## Overview
Using a network based MySQL database for storage and some Python triggered on the Raspberry Pi at boot to capture: 
* Serial Number (serial)
* System on Chip (hardware) 
* Hardware Revision (revision)
* Version (model)
* Available Ram (ram)
* WiFi mac address (wifi_mac)(if applicable)
* Ethernet mac address (eth_mac)(if applicable)

Automated shutdown can also be enabled after Python completes so SD card can easily be moved to next device.

## Prerequisites
* MySQL server on the same network as the Raspberry Pis being audited.
* [Raspberry Pi OS (32-bit)](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit) SD card (I used the Lite install and copied in a [empty ssh file](https://www.raspberrypi.org/documentation/computers/remote-access.html#enabling-the-server) and preconfigured [wpa_supplicant.conf](https://www.raspberrypi-spy.co.uk/2017/04/manually-setting-up-pi-wifi-using-wpa_supplicant-conf/) to avoid plugging in a keyboard and monitor).
### Required libraries and tools
```bash
sudo apt install python3-pip
sudo pip3 install psutil
sudo pip3 install mysql-connector-python
```

Config



## Code
### SQL
Used to prep the MySQL Database.
#### devices.sql
Script to generate table.
#### insert_device.sql
Script to generate stored procedure called from the Raspberry Pi to insert device detail rows.

### Python
Copy both files to the Raspberry Pi in the same folder. 
#### config.py
Stores username, password, MySQL database name and MySQL server name (will need modifying to work with your database configuration).

#### auditPi.py
Main methods and functions to gather data and write it to the MySQL database.

### Bash Script
start.sh is used to run the Python file from the Cron Job<br />
Make sure to mark it as executable and that the path in the file matches where you've stored the python files.
```bash
chmod +x start.sh
```
### Cron Job
Can be run from either the normal Pi users or root.<br />
(Using the root user allows the possibility of shutdown the Pi after the script has run)<br />
Make sure the path in the cronjob matches where you've put your start.sh file on the Pi.

```bash
crontab -e
```
```bash
@reboot sh /home/pi/start.sh
```

# Output

```sql
SELECT * FROM sandbox.devices;
```

|serial|hardware|revision|model|ram|wifi_mac|eth_mac|blu_mac|notes|detect_count|datetime_last_seen_utc
|--|--|--|--|--|--|--|--|--|--|--
|000000004975fd0e|BCM2835|9000c1|Raspberry Pi Zero W Rev 1.1|430|b8:27:eb:20:b8:54||||4|2021-09-02 18:05:01											


```sql
SELECT model AS Version, COUNT(*) AS Count
FROM sandbox.devices
GROUP BY model
ORDER BY Count DESC;
```
|Version|Count
|-|-
|Raspberry Pi Model B Rev 2|10
|Raspberry Pi Zero W Rev 1.1|7
|Raspberry Pi 4 Model B Rev 1.4|2
|Raspberry Pi 3 Model B Plus Rev 1.3|2
|Raspberry Pi 3 Model A Plus Rev 1.0|1
|Raspberry Pi Model B Rev 1|1
|Raspberry Pi Zero Rev 1.2|1
|Raspberry Pi Model A Rev 2|1
||25

# Still To Do:
- [x] Extra columns to detect duplications
- [ ] Python function to capture Bluetooth mac address
- [ ] Clean up Lazy hack to make sure network stack is up before writing to database
