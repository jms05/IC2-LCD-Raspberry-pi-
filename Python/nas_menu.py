# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import psutil
import os 
import socket
import fcntl
import struct
import string
from datetime import timedelta
mylcd = RPi_I2C_driver.lcd()

# test 2
mylcd.lcd_put_new_line_center("JMS.SLYIP.COM\nDONE")

sleep(2) # 2 sec delay

mylcd.lcd_clear()

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("TEMP=","").replace("'C\n",""))

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

    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY = HOUR * 24

    days    = int( total_seconds / DAY)
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE ) 
    fim = ""
    
    if days > 0:
        fim += str(days) + "D" + " "
    if len(fim) > 0 or hours > 0:
        fim += str(hours) + "H" + " " 
    if len(fim) > 0 or minutes > 0:
        fim += str(minutes) + "M" + " "
        fim += str(seconds) + "S"

    return fim;


def getDeviceinfo(deviceL):
        p = os.popen("df")
        i = 0
        while 1:
                i = i + 1
                line = p.readline()
                if i==deviceL:
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





def dotstonewLine(old):
    ret = string.replace(old,':',' ')
    return ret

def getTime():
    p=os.popen("date")
    date = p.readline() 
    elem = date.split()
    return (dotstonewLine(elem[3])) 


def wakeTime(stH,stM,endH,endM):
    on = 1
    stime = (stH * 60) + stM
    entime = (endH * 60) + endM
    while 1:
        i=0
        acTime = getTime().split()
        hora = int(acTime[0])
        minu = int(acTime[1])
    sec = int(acTime[2])
    horatest = (hora * 60) +  minu
        if horatest >= stime and horatest <= entime: ## Lcd ligado esre tempo
            on = 1
        mylcd.backlight(1)
            loop()
        else: 
        if (on == 1):
        on = 0
                mylcd.lcd_clear()
                mylcd.backlight(0)        


def loop():
    i=0
    while i<1:
        i = i+1
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
        hddsize = getDeviceinfo(12)[0]
        hdduse = getDeviceinfo(12)[1]
        hddava = getDeviceinfo(12)[2]
        hddpused = getDeviceinfo(12)[3]
        ##info relativa Torrents
        torsize = getDeviceinfo(9)[0]
        toruse = getDeviceinfo(9)[1]
        torava = getDeviceinfo(9)[2]
        torpused = getDeviceinfo(9)[3]
        ##info relativa Multimedia
        multsize = getDeviceinfo(10)[0]
        multuse = getDeviceinfo(10)[1]
        multava = getDeviceinfo(10)[2]
        multpused = getDeviceinfo(10)[3]        
    #Imprimir dados
        ##CPU
        cpuTemp = "CPU TEMP:" + cpuTaux[-4:] + "'C"
        cpuUsage = "CPU USE:" + cpuUsa + "%"
        mylcd.lcd_put_new_line_center(cpuTemp + "\n" + cpuUsage)
        sleep(3)
        mylcd.lcd_clear()
        cpufreq = "CPU FREQ Mz:" + cpuFreq[-5:]
        mylcd.lcd_put_new_line_center(cpuTemp + "\n" + cpufreq)
        sleep(3)
        mylcd.lcd_clear()
        ##RAM
        totRam = "Tot RAM:" + ramtot + "MB"
        useRam = "Used RAM:" + ramUsed + "MB"
        freeRam = "Free RAM:" + ramFree + "MB"
        mylcd.lcd_put_new_line_center(totRam + "\n" + useRam)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(useRam + "\n" + freeRam)
        sleep(3)
        mylcd.lcd_clear()
        ##Disco
        usedHDD = "Used HDD:" + diskUsed + "B"
        freeHDD = "Free HDD:" + diskFree + "B"
        precHDD = "HDD Used:" + diskPerUse
        mylcd.lcd_put_new_line_center(usedHDD + "\n" + freeHDD)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeHDD + "\n" + precHDD)
        sleep(3)
        mylcd.lcd_clear()
        ##USBHDD
        usedUSB = "Used USB:" + hdduse
        freeUSB = "Free USB:" + hddava
        precUSB = "HDD Used:" + hddpused
        mylcd.lcd_put_new_line_center(usedUSB + "\n" + freeUSB)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeUSB + "\n" + precUSB)
        sleep(3)
        mylcd.lcd_clear()
        ##Torrents
        usedTOR = "Used TOR.:" + toruse
        freeTOR = "Free TOR.:" + torava
        precTOR = "TOR. Used:" + torpused
        mylcd.lcd_put_new_line_center(usedTOR + "\n" + freeTOR)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeTOR + "\n" + precTOR)
        sleep(3)
        mylcd.lcd_clear()
        ##Multimedia
        usedMUL = "Used MUL:" + multuse
        freeMUL = "Free MUL:" + multava
        precMUL = "MUL Used:" + multpused
        mylcd.lcd_put_new_line_center(usedMUL + "\n" + freeMUL)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeMUL + "\n" + precMUL)
        sleep(3)
        mylcd.lcd_clear()
        ##NET && ##UPTIME
        ip = "IP:" + etho
        wake = "WAKE:" + uptime()
        mylcd.lcd_put_new_line_center(ip + "\n" + wake)
        sleep(3)
        mylcd.lcd_clear()


wakeTime(8,30,17,18) 
