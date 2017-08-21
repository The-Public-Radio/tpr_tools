#!/usr/bin/env python

#
# This script takes in all of the personalization data required to program a radio. 
# It validates all of that data and then creates the appropriate EEPROM image.
#
# Programming a radio requires:
#	Manufacturing data
#		* Serial number
#	Personalization data
#		* FM frequency
#		* Country code
#
# Usage: `$ perso.py <serial number> <frequency> <country code>`
# 

import country_code_presets
from getopt import getopt, GetoptError
import sys, os
import time


# Check to see that we have the right number of arguments

if (len(sys.argv) != 4):
	print('ERROR - wrong number of arguments.')
	print('Usage: `$ perso.py <serial number> <frequency> <country code>`')
	sys.exit(1)

eeprom_filename = "/home/pi/TPR_ops/temp/eeprom"

