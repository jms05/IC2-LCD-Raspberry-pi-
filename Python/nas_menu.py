# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import psutil
import os 
import socket
import fcntl
import struct
from datetime import timedelta
mylcd = RPi_I2C_driver.lcd()

# test 2
mylcd.lcd_display_string("  JMS.SLYIP.COM ", 1)
mylcd.lcd_display_string("      DONE      ", 2)
#sleep(1.5)
#mylcd.lcd_display_string("Starting RaspPI", 1)
#mylcd.lcd_display_string("   LCD by JMS", 2)

sleep(2) # 2 sec delay

mylcd.lcd_clear()

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("TEMP=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
#def getRAMinfo():
#    p = os.popen('free')
#    i = 0
#    while 1:
#        i = i + 1
#        line = p.readline()
#        if i==2:
#            return(line.split()[1:4])
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
                line = (line.split()[1:4])
                ramtot = line[0]
                ramused = line[1]
                ramfree = line [2]
                ramtot = str(float(ramtot) / 1024)[0:3]      
                ramused = str(float(ramused) / 1024)[0:3]      
                ramfree = str(float(ramfree) / 1024)[0:3]  
                return (ramtot + " " + ramused + " " + ramfree)

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_cpu_speed():
    f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
    cpu = f.read()
    return cpu

mylcd.lcd_clear()


def uptime():
	try:
		f = open( "/proc/uptime" )
		contents = f.read().split()
		f.close()
	except:
		return "ERROR"
	
	total_seconds = float(contents[0])

	MINUTE	= 60
	HOUR	= MINUTE * 60
	DAY	= HOUR * 24

	days	= int( total_seconds / DAY)
	hours	= int( ( total_seconds % DAY ) / HOUR )
	minutes	= int( ( total_seconds % HOUR ) / MINUTE )
	seconds	= int( total_seconds % MINUTE )	
	fim = ""
	
	if days > 0:
		fim += str(days) + "D" + " "
	if len(fim) > 0 or hours > 0:
		fim += str(hours) + "H" + " " 
	if len(fim) > 0 or minutes > 0:
		fim += str(minutes) + "M" + " "
     	fim += str(seconds) + "S"

	return fim;

def getUSBinfo():
        p = os.popen("df")
        i = 0
        while 1:
                i = i + 1
                line = p.readline()
                if i==12:
                        line = line.split()[1:5]
                        size = float(line[0])
                        used = float(line[1])
                        ava = float(line[2])
###Total Size
                        if size  >= 1073741824:
                                                        size = size / 1073741824
                                                        size = str(size)[:4] + "TB"
                        else:
                                size = size / (1024 * 1024)
                                size = str(size)[0] + str(size)[1] + str(size)[2] + "GB"
###Total Used
                        if used  >= 1073741824:
                                                        used = used / 1073741824
                                                        used = str(used)[:4] + "TB"
                        else:
                                used = used / (1024 * 1024)
                                used = str(used)[0] + str(used)[1] + str(used)[2] + "GB"
###Total Ava
                        if ava  >= 1073741824:
                                                        ava = ava / 1073741824
                                                        ava = str(ava)[:4] + "TB"
                        else:
                                ava = ava / (1024 * 1024)
                                ava = str(ava)[0] + str(ava)[1] + str(ava)[2] + "GB"

                        per = line[3]
                        return (size + " " + used + " "  + ava + " "  + per).split()

def getTorrentsinfo():
        p = os.popen("df")
        i = 0
        while 1:
                i = i + 1
                line = p.readline()
                if i==9:
                        line = line.split()[1:5]
                        size = float(line[0])
                        used = float(line[1])
                        ava = float(line[2])
###Total Size
                        if size  >= 1073741824:
                                                        size = size / 1073741824
                                                        size = str(size)[:4] + "TB"
                        else:
                                size = size / (1024 * 1024)
                                size = str(size)[0] + str(size)[1] + str(size)[2] + "GB"
###Total Used
                        if used  >= 1073741824:
                                                        used = used / 1073741824
                                                        used = str(used)[:4] + "TB"
                        else:
                                used = used / (1024 * 1024)
                                used = str(used)[0] + str(used)[1] + str(used)[2] + "GB"
###Total Ava 
                        if ava  >= 1073741824:
                                                        ava = ava / 1073741824
                                                        ava = str(ava)[:4] + "TB"
                        else:
                                ava = ava / (1024 * 1024)
                                ava = str(ava)[0] + str(ava)[1] + str(ava)[2] + "GB"

                        per = line[3]
                        return (size + " " + used + " "  + ava + " "  + per).split()


def getMultimediainfo():
        p = os.popen("df")
        i = 0
        while 1:
                i = i + 1
                line = p.readline()
                if i==10:
                        line = line.split()[1:5]
                        size = float(line[0])
                        used = float(line[1])
                        ava = float(line[2])
###Total Size
                        if size  >= 1073741824:
                                                        size = size / 1073741824
                                                        size = str(size)[:4] + "TB"
                        else:
                                size = size / (1024 * 1024)
                                size = str(size)[0] + str(size)[1] + str(size)[2] + "GB"
###Total Used
                        if used  >= 1073741824:
                                                        used = used / 1073741824
                                                        used = str(used)[:4] + "TB"
                        else:
                                used = used / (1024 * 1024)
                                used = str(used)[0] + str(used)[1] + str(used)[2] + "GB"
###Total Ava 
                        if ava  >= 1073741824:
                                                        ava = ava / 1073741824
                                                        ava = str(ava)[:4] + "TB"
                        else:
                                ava = ava / (1024 * 1024)
                                ava = str(ava)[0] + str(ava)[1] + str(ava)[2] + "GB"


                        per = line[3]
                        return (size + " " + used + " "  + ava + " "  + per).split()

while 1:
#obter Dados
##Informacao relativa ao CPU
        cpuTaux = getCPUtemperature()
	cpuUsa = getCPUuse()
	cpuFreq = get_cpu_speed()
##Informaao relativa a ram
	ram = getRAMinfo()
	ram = ram.split()
	ramtot = ram[0]
	ramUsed = ram[1]
	ramFree = ram[2]
##info relativa ao disco
	disco= getDiskSpace()
	diskTot = disco[0]
	diskUsed = disco[1]
        diskFree = disco[2]
        diskPerUse = disco[3]	
##info relativa ao IP
	etho = get_ip_address('eth0')
##info relativa ao disco externo
	hddsize = getUSBinfo()[0]
        hdduse = getUSBinfo()[1]
        hddava = getUSBinfo()[2]
        hddpused = getUSBinfo()[3]

##info relativa Torrents
        torsize = getTorrentsinfo()[0]
        toruse = getTorrentsinfo()[1]
        torava = getTorrentsinfo()[2]
        torpused = getTorrentsinfo()[3]
##info relativa Multimedia
        multsize = getMultimediainfo()[0]
        multuse = getMultimediainfo()[1]
        multava = getMultimediainfo()[2]
        multpused = getMultimediainfo()[3]

#Imprimir dados
##CPU
	cpuTemp = " CPU TEMP:" + cpuTaux[-4:]
        mylcd.lcd_display_string(cpuTemp, 2)
        mylcd.lcd_display_string(" CPU USE:" + cpuUsa + "%", 1)
        sleep(3)
        mylcd.lcd_clear()
	
	cpuTemp = " CPU TEMP:" + cpuTaux[-4:]
        mylcd.lcd_display_string(cpuTemp, 1)
        mylcd.lcd_display_string( "CPU FREQ Mz:" + cpuFreq[-5:], 2)
        sleep(3)
        mylcd.lcd_clear()

##RAM
	mylcd.lcd_display_string(" Tot RAM:" + ramtot + "MB", 1)
	mylcd.lcd_display_string("Used RAM:" + ramUsed + "MB", 2)
	sleep(3)
	mylcd.lcd_clear()
	
	mylcd.lcd_display_string("Used RAM:" + ramUsed + "MB", 1)
        mylcd.lcd_display_string("Free RAM:" + ramFree + "MB", 2)
        sleep(3)
        mylcd.lcd_clear()
##Disco
	mylcd.lcd_display_string(" Used HDD:" + diskUsed + "B", 1)
        mylcd.lcd_display_string(" Free HDD:" + diskFree + "B", 2)
        sleep(3)
        mylcd.lcd_clear()

	mylcd.lcd_display_string(" Free HDD:" + diskFree + "B", 1)
        mylcd.lcd_display_string("  HDD Used:" + diskPerUse, 2)
        sleep(3)
        mylcd.lcd_clear()
##USBHDD
        mylcd.lcd_display_string(" Used USB:" + hdduse, 1)
        mylcd.lcd_display_string(" Free USB:" + hddava, 2)
        sleep(3)
        mylcd.lcd_clear()

        mylcd.lcd_display_string(" Free USB:" + hddava, 1)
        mylcd.lcd_display_string("  HDD Used:" + hddpused, 2)
        sleep(3)
        mylcd.lcd_clear()
##Torrents
        mylcd.lcd_display_string("Used TOR.:" + toruse, 1)
        mylcd.lcd_display_string("Free TOR.:" + torava, 2)
        sleep(3)
        mylcd.lcd_clear()

        mylcd.lcd_display_string("Free TOR.:" + torava, 1)
        mylcd.lcd_display_string(" TOR. Used:" + torpused, 2)
        sleep(3)
        mylcd.lcd_clear()
##Multimedia
        mylcd.lcd_display_string(" Used MUL:" + multuse, 1)
        mylcd.lcd_display_string(" Free MUL:" + multava, 2)
        sleep(3)
        mylcd.lcd_clear()

        mylcd.lcd_display_string(" Free MUL:" + multava, 1)
        mylcd.lcd_display_string("  MUL Used:" + multpused, 2)
        sleep(3)
        mylcd.lcd_clear()




##NET
	mylcd.lcd_display_string("IP:" + etho, 1)
        mylcd.lcd_display_string("WAKE:" + uptime(), 2)
        sleep(3)
        mylcd.lcd_clear()
##UPTIME
