import sys, os
import RPi.GPIO as GPIO
import time
from getopt import getopt, GetoptError


firmware = '3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex'
eeprom = 'eeprom'

option_list='f:e:'


def usage():
	print r'''Usage: program_radioTEST [-f <firmware>] [-e <n>] [-d <n>] [-s <n>] [-v <n>]
		[-m [-S <sn>] [-T <ts>] [-C <campaign>]]
		-f <s>	Specify the string in MHz (default = 3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex)
		-e <s>	Specify the eeprom (default = eeprom)'''
	sys.exit(1)

try:
	opts, args = getopt(sys.argv[1:], option_list)
except GetoptError as err:
	print str(err)
	usage()

for o, a in opts:
	if o == '-f':
		firmware = str(a)
	elif o == '-e':
		eeprom = str(a)
	else:
		usage()

GPIO.setmode(GPIO.BCM)

# Pin that our button is connected to. I think that GPIO 2 is open currently. Note, this is broadcom numbering.
# See https://pinout.xyz/ for pinout 
# Set this pin as input and enable internal pull up resistor. Our button is active low.  
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(2)
    if input_state == False:
    	#print "programming"
    	exit = os.system('sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U flash:w:/home/pi/ops_tools/data/'+firmware+ ' -U eeprom:w:/home/pi/ops_tools/temp/'+eeprom)
        time.sleep(0.5) 
        exit()