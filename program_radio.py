import sys, os
import RPi.GPIO as GPIO
import time
import argparse

default_firmware = '/home/pi/ops_tools/data/3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex'
default_eeprom = 'eeprom'


#get arguments
# if --f is specified, set firmware to be the firmware argument
# 	if the firmware that was specified doesn't exist, exit 1
# else set firmware to default_firmware
# if --e is specified, set eeprom to be the eeprom argument
# 	if the eeprom that was specified doesn't exist, exit 1
# else set eeprom to default_eeprom





GPIO.setmode(GPIO.BCM)

# Pin that our button is connected to. I think that GPIO 2 is open currently. Note, this is broadcom numbering.
# See https://pinout.xyz/ for pinout 
# Set this pin as input and enable internal pull up resistor. Our button is active low.  
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(2)
    if input_state == False:
    	#print "programming"
    	avrdude_exit = os.system('sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U flash:w:'+firmware+ ' -U eeprom:w:'+eeprom)
        #if avrdude_exit = 0:
        	# notify the user that the programming succeeded and exit 0
        #else
        	# notify the user that the programming failed and give a semantic exit code
