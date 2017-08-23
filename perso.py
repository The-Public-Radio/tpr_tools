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

#import country_code_presets
from getopt import getopt, GetoptError
import sys, os
import time
import subprocess

# Check to see that we have the right number of arguments 
if (len(sys.argv) != 4):
	print 'ERROR - wrong number of arguments.'
	print 'Usage: `$ perso.py <serial number> <frequency> <country code>`'
	sys.exit(1)

# set output filename
eeprom_filename = '/home/pi/ops_tools/temp/eeprom'

# set regions
EU = ['AE','BE','BG','CZ','DE','EE','IE','EL','ES','FR','FO','HR','IT','CY','LV','LT','LU','HU','MT','NL','NZ','AT','PL','PT','RO','SI','SK','FI','SE','UK','GB','DK','CH','ZA']
Americas = ['US','CA','AI','AG','AW','BS','BB','BZ','BM','VG','CA','KY','CR','CU','CW','DM','DO','SV','GL','GD','GP','GT','HT','HN','JM','MQ','MX','PM','MS','CW','KN','NI','PA','PR','KN','LC','PM','VC','TT','TC','VI','SX','BQ','SA','SE','AR','BO','BR','CL','CO','EC','FK','GF','GY','PY','PE','SR','UY','VE']
Asia = ['AF','AM','AZ','BH','BD','BT','BN','KH','CN','CX','CC','IO','GE','HK','IN','ID','IR','IQ','IL','JO','KZ','KP','KR','KW','KG','LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK','SY','TW','TJ','TH','TR','TM','AE','UZ','VN','YE','PS']

# set up get_preset function
#def get_preset(country):
#        if country in EU:
#                band = 0
#                deemphasis = 1
#                spacing = 1
#        elif country in Asia:
#                band = 0
#		print 'band is', band
#                deemphasis = 1
#                spacing = 1
#        elif country in Americas:
#                band = str(0)
#                deemphasis = 0
#                spacing = 0
#		print 'country is in americas'
#        elif country == 'AU':
#                band = 0
#                deemphasis = 1
#                spacing = 0
#        elif country == 'JP':
#                band = 1
#                deemphasis = 1
#                spacing = 1
#	else:
#		print 'Error: country not found'
#		sys.exit(1)

# set input variables
serial = sys.argv[1]
freq = sys.argv[2]
country = sys.argv[3]

# check the country code and define band, channel spacing, deemphasis, region
if country in EU:
	band = str(0)
        deemphasis = str(1)
        spacing = str(1)
elif country in Asia:
        band = str(0)
        deemphasis = str(1)
        spacing = str(1)
elif country in Americas:
        band = str(0)
        deemphasis = str(0)
        spacing = str(0)
elif country == 'AU':
        band = str(0)
        deemphasis = str(1)
        spacing = str(0)
elif country == 'JP':
        band = str(2)
        deemphasis = str(1)
        spacing = str(1)
else:
        print 'Error: country not found'
        sys.exit(1)

# open up the eeprom file
f = open(eeprom_filename, 'w')

# open a subprocess and pipe stdout to the eeprom file
print 'Writing to eeprom_filename via eeprom.py...'
exit = subprocess.call(['/home/pi/ops_tools/eeprom.py', '-f', freq, '-b', band, '-d', deemphasis, '-s', spacing, '-S', serial], stdout=f)
f.close()
print 'eeprom_filename closed'
print exit

if (exit != 0):
	print 'ERROR: failed at eeprom/py. Log below.'
	subprocess.call(['cat', eeprom_filename])
	sys.exit(1)
else:
	print 'SUCCESS! Contents of', eeprom_filename, 'below.'
	subprocess.call(['cat', eeprom_filename])

# close the eeprom file
#f.close()

# display the results
#print 'the contents of', eeprom_filename, 'are below'
#subprocess.call(['cat', eeprom_filename])




