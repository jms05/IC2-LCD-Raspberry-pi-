# requires RPi_I2C_driver.py on the same folder

# -*- coding: utf-8 -*-

#Compiled, mashed and generally mutilated 2014-2015 by Joao Silva
#Made available under GNU GENERAL PUBLIC LICENSE
#By JMS (Joao Silva)
#08-03-2015

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

mylcd.lcd_put_new_line_center("YOUR BOOT\nMESSAGE")

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
                ramtot = float(line[0])
                ramused = float(line[1])
                ramfree = float(line[2])
                ##GB
                if ramtot >= (1024 * 1024):
                    ramtot = ramtot / (1024*1024)
                    if ramtot < 10:
                        ramtot = str(ramtot)[0:1]
                    else:
                         if ramtot < 100:
                            ramtot = str(ramtot)[0:2]
                         else:
                            ramtot = str(ramtot)[0:3]
                    ramtot = ramtot + "GB"

                if ramused >= (1024 * 1024):
                    ramused = ramused / (1024*1024)
                    if ramused < 10:
                        ramused = str(ramused)[0:1]
                    else:
                         if ramused < 100:
                            ramused = str(ramused)[0:2]
                         else:
                            ramused = str(ramused)[0:3]
                    ramused = ramused + "GB"

                if ramfree >= (1024 * 1024):
                    ramfree = ramfree / (1024*1024)
                    if ramfree < 10:
                        ramfree = str(ramfree)[0:1]
                    else:
                         if ramfree < 100:
                            ramfree = str(ramfree)[0:2]
                         else:
                            ramfree = str(ramfree)[0:3]
                    ramfree = ramfree + "GB"

                ##MB
                if ramtot >= 1024 and ramtot < (1024*1024):
                    ramtot = ramtot / (1024)
                    if ramtot < 10:
                        ramtot = str(ramtot)[0:1]
                    else:
                         if ramtot < 100:
                            ramtot = str(ramtot)[0:2]
                         else:
                            ramtot = str(ramtot)[0:3]
                    ramtot = ramtot + "MB"

                if ramused >= 1024 and ramused < (1024*1024):
                    ramused = ramused / (1024)
                    if ramused < 10:
                        ramused = str(ramused)[0:1]
                    else:
                         if ramused < 100:
                            ramused = str(ramused)[0:2]
                         else:
                            ramused = str(ramused)[0:3]
                    ramused = ramused + "MB"

                if ramfree >= 1024 and ramfree < (1024*1024):
                    ramfree = ramfree / (1024)
                    if ramfree < 10:
                        ramfree = str(ramfree)[0:1]
                    else:
                         if ramfree < 100:
                            ramfree = str(ramfree)[0:2]
                         else:
                            ramfree = str(ramfree)[0:3]
                    ramfree = ramfree + "MB"
                     ##KB
                if ramtot <1024:
                    if ramtot < 10:
                        ramtot = str(ramtot)[0:1]
                    else:
                         if ramtot < 100:
                            ramtot = str(ramtot)[0:2]
                         else:
                            ramtot = str(ramtot)[0:3]
                    ramtot = ramtot + "KB"

                if ramused < 1024:
                    if ramused < 10:
                        ramused = str(ramused)[0:1]
                    else:
                         if ramused < 100:
                            ramused = str(ramused)[0:2]
                         else:
                            ramused = str(ramused)[0:3]
                    ramused = ramused + "KB"

                if ramfree < 1024:
                    if ramfree < 10:
                        ramfree = str(ramfree)[0:1]
                    else:
                         if ramfree < 100:
                            ramfree = str(ramfree)[0:2]
                         else:
                            ramfree = str(ramfree)[0:3]
                    ramfree = ramfree + "KB"

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





def dotstoSpace(old):
    ret = string.replace(old,':',' ')
    return ret

def getTime():
    p=os.popen("date")
    date = p.readline() 
    elem = date.split()
    return (dotstoSpace(elem[3])) 


def wakeTime(stH,stM,endH,endM,minLoop):
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
        sectime = (horatest * 60) + sec  
        if horatest >= stime and horatest <= entime: ## Lcd ligado esre tempo
            on = 1
            mylcd.backlight(1)
            loop()
        else: 
            if ( minLoop > 0 and sectime % (minLoop * 60) == 0):
                if (on == 0):
                    on = 1
                    mylcd.lcd_clear()
                    mylcd.backlight(1)
                loop()
            else (on == 1):
                on = 0
                mylcd.lcd_clear()
                mylcd.backlight(0)        


def loop():
    i=0
    while i<1:
        i = i+1
    #Get data
        ##CPU
        cpuTaux = getCPUtemperature()
        cpuUsa = getCPUuse()
        cpuFreq = get_cpu_speed()
        ##RAM
        ram = getRAMinfo().split()
        ramtot = ram[0]
        ramUsed = ram[1]
        ramFree = ram[2]
        ##LOCAL HDD
        disco= getDiskSpace()
        diskTot = disco[0]
        diskUsed = disco[1]
        diskFree = disco[2]
        diskPerUse = disco[3]   
        ##IP
        etho = get_ip_address('eth0')
        ##EXTERNAL HDD
        hddsize = getDeviceinfo(12)[0]
        hdduse = getDeviceinfo(12)[1]
        hddava = getDeviceinfo(12)[2]
        hddpused = getDeviceinfo(12)[3]
        ##NETWORK DRIVE_TORRENTS
        torsize = getDeviceinfo(9)[0]
        toruse = getDeviceinfo(9)[1]
        torava = getDeviceinfo(9)[2]
        torpused = getDeviceinfo(9)[3]
        ##NETWORK DRIVE_MULTIMEDIA
        multsize = getDeviceinfo(10)[0]
        multuse = getDeviceinfo(10)[1]
        multava = getDeviceinfo(10)[2]
        multpused = getDeviceinfo(10)[3]        
    #PRINT DATA
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
        totRam = "Tot RAM:" + ramtot
        useRam = "Used RAM:" + ramUsed
        freeRam = "Free RAM:" + ramFree
        mylcd.lcd_put_new_line_center(totRam + "\n" + useRam)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(useRam + "\n" + freeRam)
        sleep(3)
        mylcd.lcd_clear()
        ##LOCAL HD
        usedHDD = "Used HDD:" + diskUsed + "B"
        freeHDD = "Free HDD:" + diskFree + "B"
        precHDD = "HDD Used:" + diskPerUse
        mylcd.lcd_put_new_line_center(usedHDD + "\n" + freeHDD)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeHDD + "\n" + precHDD)
        sleep(3)
        mylcd.lcd_clear()
        ##EXTERNAL HDD
        usedUSB = "Used USB:" + hdduse
        freeUSB = "Free USB:" + hddava
        precUSB = "HDD Used:" + hddpused
        mylcd.lcd_put_new_line_center(usedUSB + "\n" + freeUSB)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeUSB + "\n" + precUSB)
        sleep(3)
        mylcd.lcd_clear()
        ##NETWORK DRIVE_TORRENTS
        usedTOR = "Used TOR.:" + toruse
        freeTOR = "Free TOR.:" + torava
        precTOR = "TOR. Used:" + torpused
        mylcd.lcd_put_new_line_center(usedTOR + "\n" + freeTOR)
        sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_put_new_line_center(freeTOR + "\n" + precTOR)
        sleep(3)
        mylcd.lcd_clear()
        ##NETWORK DRIVE_MULTIMEDIA
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


wakeTime(8,30,23,59,10) #start hour, start minute, end hour, end minute, interval to show on sleep mode 0 to not show
