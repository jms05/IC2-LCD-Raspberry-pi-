# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

mylcd = RPi_I2C_driver.lcd()



mylcd.print_on_center("YOUR MENSAGE",1)
mylcd.anime_left_right("BOOTING UP RASPBERRY PI...",2,0.25,1)
mylcd.print_on_center("DONE",2)
sleep(2.5)
mylcd.anime_left_right("STARTING NAS SERVICES",2,0.25,1)