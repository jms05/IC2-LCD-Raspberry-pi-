# -*- coding: utf-8 -*-

#Compiled, mashed and generally mutilated 2014-2015 by Joao Silva
#Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources, 
# original souce downloaded from Denis Pleic on 2015-02-2015
# By JMS (Joao Silva)
# added function to print on lcd to diferent ways
# 08-03-2015

import smbus
from time import *
 
class i2c_device:
   def __init__(self, addr, port=1):
      self.addr = addr
      self.bus = smbus.SMBus(port)
 
# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)
 
# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)
 
# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)
 
# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)
 
# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)
 
# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)
 
 
 
# LCD Address
ADDRESS = 0x27
 
# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
 
# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00
 
# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00
 
# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00
 
# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00
 
# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
 
En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit
 
class lcd:
   #initializes objects and lcd
   def __init__(self):
      self.lcd_device = i2c_device(ADDRESS)
 
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)
 
      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)
 
 
   # clocks EN to latch command
   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)
 
   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)
 
   # write a command to lcd
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))
 
   # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
   # works!
   def lcd_write_char(self, charvalue, mode=1):
      self.lcd_write_four_bits(mode | (charvalue & 0xF0))
      self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
  
 
   # put string function
   def lcd_display_string(self, string, line):
      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)
 
      for char in string:
         self.lcd_write(ord(char), Rs)
   #just works for 1 "\n" to work with more uncomment the following lines
   def lcd_put_new_line(self,string):
      string = string.split('\n')
      self.lcd_display_string(string[0],1)
      self.lcd_display_string(string[1],2)
      #self.lcd_display_string(string[2],3)
      #self.lcd_display_string(string[3],4)

   def anime_left_right(self,string,linha,delay,rept):
      aux = "                "
      oriSize = len(string) + 17
      j = 0
      while j < rept:
         i = 0
         string_aux = aux + string
         while i < oriSize:
            self.lcd_display_string(string_aux,linha)
            string_aux  = string_aux[1:]
            string_aux = string_aux + " "
            i = i + 1
            if i < (oriSize - 1):
               sleep(delay)
         j = j + 1


   def lcd_str_dance(self,string,wline,delay,rept):
      strSize = len(string)
      if strSize <= 16: # strings greater than 16 chars not allowed (lcd line size)
         aux = ""

         while (len(aux) + strSize) < 16:
            aux = aux + " "
         j = 0 #contol the number of loops 
         auxSize = len(aux)

         while j < rept:
            i = 0
            string_aux = aux + string
            while i < auxSize :
               self.lcd_display_string(string_aux,wline)
               string_aux  = string_aux[1:]
               string_aux = string_aux + " "
               i = i + 1
               sleep(delay)
            i = 0
            while i < auxSize :
               self.lcd_display_string(string_aux,wline)
               string_aux  = string_aux[:-1]
               string_aux = " " + string_aux
               i = i + 1
               sleep(delay)
            j = j + 1
         # this final loop makes string go way progressively
         while (i<16):
            string_aux = " " + string_aux
            self.lcd_display_string(string_aux,wline)
            i = i + 1
            sleep(delay)

   # pint a string on the center of the LCD
   def print_on_center(self,string,line):     
      n = 0 #indicates where inserte the next ' '
      while (len(string) < 16):
         if n == 0:
            n = 1
            string = " " + string
         else:
            n = 0
            string = string + " "

      self.lcd_display_string(string,line)

   #just works for 1 "\n" to work with more uncomment the following lines
   def lcd_put_new_line_center(self,string):
      string = string.split('\n')
      self.print_on_center(string[0],1)
      self.print_on_center(string[1],2)
      #self.print_on_center(string[2],3)
      #self.print_on_center(string[3],4)

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)
 
   # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
   def backlight(self, state): # for state, 1 = on, 0 = off
      if state == 1:
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)
 
   # add custom characters (0 - 7)
   def lcd_load_custom_chars(self, fontdata):
      self.lcd_write(0x40);
      for char in fontdata:
         for line in char:
            self.lcd_write_char(line)         
         
   # define precise positioning (addition from the forum)
   def lcd_display_string_pos(self, string, line, pos):
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    elif line == 3:
      pos_new = 0x14 + pos
    elif line == 4:
      pos_new = 0x54 + pos
 
    self.lcd_write(0x80 + pos_new)
 
    for char in string:
      self.lcd_write(ord(char), Rs)
