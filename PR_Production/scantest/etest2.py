#!/usr/bin/python

#
# Prelim Test Fixture program.
# No GUI, simple text output and looping suitable for
# maker boards (eg. assembled SMT PCBA, w/o thru-hole parts,
# and user perso.
#
# TODO - add command line parsing instead of hardcoded variables.

from time import sleep
import RPi.GPIO as GPIO
#import subprocess
import string

#
# Firmware image to use 
#firmware='pr.hex'

#
# Program to invoke to generate config, must return filename containing
# intel hex of eeprom contents, or non-zero exit code on error.
#config_prog='./get_next'

#
# basic avrdude command line
#cmd_basis='avrdude -qq -P usb -c usbtiny -p attiny45  -B 15 -e'

#
# GPIO definitions
DUT_PRESENT = 2		# Input. Low when DUT present
DUT_I_TRIP = 21		# Input. Overcurrent detect, < 40mA=>low, >=40mA=>high
DUT_POWER_EN = 20	# Output. Enable DUT power. High = on.
DUT_SW = 26		# Input. Low when DUT button pressed.

LED_PROCESS = 17	# Output. Process LED, orange. High = on
LED_FAIL = 27		# Output. Fail LED, red. High = on
LED_PASS = 22		# Output. Pass LED, green. High = on

SWITCH_1 = 14		# Input. Test fixture switch #1. Low = pressed.
SWITCH_2 = 15		# Input. Test fixture switch #2. Low = pressed.
SWITCH_3 = 18		# Input. Test fixture switch #3. Low = pressed.
SWITCH_4 = 23		# Input. Test fixture switch #4. Low = pressed.

def setup_gpio():
	GPIO.setmode(GPIO.BCM)

	for i in [DUT_PRESENT, DUT_I_TRIP, DUT_SW, SWITCH_1,
					SWITCH_2, SWITCH_3, SWITCH_4]:
		GPIO.setup(i, GPIO.IN)

	for i in [DUT_POWER_EN, LED_PROCESS, LED_FAIL, LED_PASS]:
		GPIO.setup(i, GPIO.OUT)
		GPIO.output(i, False)

#
# invoke config_prog to generate the eeprom contents, and then
# program the firmware and the eeprom contents. Return True if everyhing
# goes accrding to plan, False otherwise.
#def program():
#	try:
#		config_file = subprocess.check_output([config_prog]).strip()
#	except:
#		print "config prog fail"
#		return False
#
#	flash = "-U flash:w:%s" % firmware
#	eeprom = "-U eeprom:w:%s" % config_file
#
#	command = string.join((cmd_basis, flash, eeprom)).split()
#
#	try:
#		subprocess.check_call(command)
#	except:
#		print "avrdude command fail"
#		return False
#
#	print "Programmed with %s & %s OK" % (firmware, config_file)
#	return True

#def test():
#	print "Press button 1 if Audio & LED are OK, button 3 otherwise"
#	while True:
#		if not GPIO.input(SWITCH_1):
#			return True
#		if not GPIO.input(SWITCH_3):
#			return False
#		sleep(0.1)

setup_gpio()




def etest():
	power = False
	present = False
	while True:
		present = not GPIO.input(DUT_PRESENT)
	
		if present and not power:
			sleep(0.5)
			if not GPIO.input(DUT_PRESENT):
				GPIO.output(LED_FAIL, False)
				GPIO.output(LED_PASS, False)
				power = True
				print "Power on"
				GPIO.output(DUT_POWER_EN, True)
				GPIO.output(LED_PROCESS, True)
				sleep(0.1)
				if (GPIO.input(DUT_I_TRIP)):
					print "Fault: overcurrent"
					power = False
					GPIO.output(DUT_POWER_EN, False)
					GPIO.output(LED_PROCESS, True)
					GPIO.output(LED_FAIL, True)
					return(1)
					break
				else:
					
					GPIO.output(LED_PROCESS, True)
					GPIO.output(LED_PASS, True)
					print "Passed"
					return(0)
					break
#				else:
#					GPIO.output(LED_FAIL, True)
#					print "******* Failed ******"
#					return(1)
#					break 
	
#	elif not present and power: 
#		power = False
#		print "Power off"
#		GPIO.output(DUT_POWER_EN, power)
#		GPIO.output(LED_PROCESS, power)

	sleep(0.1)

