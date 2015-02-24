# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

mylcd = RPi_I2C_driver.lcd()
# test 2
mylcd.lcd_clear()
mylcd.print_on_center("SHUTTING DOWN", 1)
sleep(2)
mylcd.lcd_clear()
mylcd.backlight(0)
