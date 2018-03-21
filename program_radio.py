import sys, os
#import RPi.GPIO as GPIO
import time


default_firmware = '/home/pi/ops_tools/data/3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex'
default_eeprom = '/home/pi/ops_tools/temp/eeprom'


#get arguments
# if --f is specified, set firmware to be the firmware argument
# 	if the firmware that was specified doesn't exist, exit 1
# else set firmware to default_firmware
# if --e is specified, set eeprom to be the eeprom argument
# 	if the eeprom that was specified doesn't exist, exit 1
# else set eeprom to default_eeprom


if len(sys.argv) == 3:
	#this means that three arguments were given: the command, the firmware, and the eeprom
	eeprom = sys.argv[1]
	firmware = sys.argv[2]
elif len(sys.argv) == 1:
	# this means that just one argument was given: the command
	# so set firmware and eeprom to defaults
	eeprom = default_eeprom
	firmware = default_firmware
else:
	print('Wrong number of arguments. Exiting. \n')
	exit(1)

# now check to see that they're valid files
if not os.path.exists(eeprom):
	print('Specified eeprom file does not exist. You specified:')
	print(eeprom)
	print('Exiting. \n')
	exit(1)
elif not os.path.exists(firmware):
	print('Specified firmware file does not exist. You specified:')
	print(firmware)
	print('Exiting. \n')
	exit(1)



GPIO.setmode(GPIO.BCM)
# Pin that our button is connected to. I think that GPIO 2 is open currently. Note, this is broadcom numbering.
# See https://pinout.xyz/ for pinout 
# Set this pin as input and enable internal pull up resistor. Our button is active low.  
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    input_state = GPIO.input(2)
    if input_state == False:
    	print('Programming...')
    	avrdude_exit = os.system('sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U \
    		flash:w:'+firmware+ ' -U eeprom:w:'+eeprom)
        if avrdude_exit == 0:
        	print('Programming successful!')
        else:
        	print('Programming FAILED with exit code:')
        	print(avrdude_exit)
        	exit(3)
