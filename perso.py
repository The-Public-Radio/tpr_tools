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

# print 'length of sys.argv is ', len(sys.argv)

# Check to see that we have the right number of arguments 
if (len(sys.argv) != 4):
	print 'ERROR - wrong number of arguments.'
	print 'Usage: `$ perso.py <serial number> <frequency> <country code>`'
	sys.exit(1)

# set output filename
eeprom_filename = '/Users/snwright/TPR_ops/temp/eeprom'

# set input variables
serialNumber = sys.argv[1]
frequency = sys.argv[2]
countryCode = sys.argv[3]
# print 'serialNumber is', serialNumber
# print 'frequency is', frequency
# print 'countryCode is', countryCode

# check the country code and define band, channel spacing, deemphasis, region
presets = country_code_presets.get_preset(countryCode)
print presets
if (presets == -1):
	print 'Error: country not found'
	sys.exit(1)
# else: print 'countryCode is', countryCode

# run eeprom.py
hexfile = os.system("./eeprom.py -f %s -b %s -d %s -s %s -S %s" % frequency, presets['band'], presets['deemphasis'], presets['channel_spacing'], serialNumber)


# Open the eeprom file
eeprom_file = open(eeprom_filename, 'w')
eeprom_file.write(hexfile)

# Close the eeprom file
eeprom_file.close()





