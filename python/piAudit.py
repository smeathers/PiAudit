import psutil # Memory
import fcntl, socket, struct # Network
import mysql, config # Database
from subprocess import call # Shutdown
import time

class getData():
    def getHwAddr(self, ifname):
        # Extract mac address from known interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mac = ""
        try:
            info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
            mac = ':'.join('%02x' % b for b in info[18:24])
        except:
            return None
        return mac.strip()

    def getSerial(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open("/proc/cpuinfo",'r')
            for line in f:
                if line.startswith("Serial"):
                    cpuserial = line.rsplit(": ")[1]
            f.close()
        except:
            cpuserial = "ERROR00000000"

        return cpuserial.strip()


    def getModel(self):
        # Extract model from cpuinfo file
        model = "Unknown Model"
        try:
            f = open("/proc/cpuinfo",'r')
            for line in f:
                if line.startswith("Model"):
                    model = line.rsplit(": ")[1]
            f.close()
        except:
            model = "Model Error"

        return model.strip()


    def getHardware(self):
        # Extract model from cpuinfo file
        hardware = "Unknown Hardware"
        try:
            f = open("/proc/cpuinfo",'r')
            for line in f:
                if line.startswith("Hardware"):
                    hardware = line.rsplit(": ")[1]
            f.close()
        except:
            hardware = "Hardware Error"

        return hardware.strip()

    def getRevision(self):
        # Extract model from cpuinfo file
        revision = "Unknown Revision"
        try:
            f = open("/proc/cpuinfo",'r')
            for line in f:
                if line.startswith("Revision"):
                    revision = line.rsplit(": ")[1]
            f.close()
        except:
            revision = "Revision Error"

        return revision.strip()


    def getMemory(self):
        totalmemory = psutil.virtual_memory().total >> 20 #(30=gb 20=mb)
        return totalmemory

def dbInsert (serial, hardware, revision, model, ram, wifi_mac, eth_mac):
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
        mySQL_conn = mysql.connector.connect(host=config.server, database=config.database, user=config.username, password=config.password)
        cursor = mySQL_conn.cursor()

        cursor.callproc('insert_device', [serial, hardware, revision, model, ram, wifi_mac, eth_mac])
        mySQL_conn.commit()
        # print out User details
        for result in cursor.stored_results():
            print(result.fetchall())
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        # closing database connection.
        if (mySQL_conn.is_connected()):
            cursor.close()
            mySQL_conn.close()

def main():
    gd = getData()

    serial = gd.getSerial()
    print("serial:\t  " + serial)
    model = gd.getModel()
    print("model:\t  " + model)
    hardware = gd.getHardware()
    print("hardware: " + hardware)
    revision = gd.getRevision()
    print("revision: " + revision)
    memory = gd.getMemory()
    print("memory:\t  " + str(memory) + "Mb")
    eth0 = gd.getHwAddr("eth0")
    if eth0 is not None:
        print("eth0:\t  " + eth0)
    wlan0 = gd.getHwAddr("wlan0")
    print("wlan0:\t  " + wlan0)
    time.sleep(4) # Lazy hack to make sure network stack is up before trying to access database server
    dbInsert(serial, hardware, revision, model, memory, eth0, wlan0)

main()
