import sys, os
import time
sys.path.append('../config')
from subprocess import Popen
import tempfile
from subprocess import call
import country_code_presets
from getopt import getopt, GetoptError

## ENTER PROGRAMMER HERE ##
# PROGRAM = 'usbtiny'


def usage():
  print r'''Usage: python PRProg1.py -f <frequency> -c <country_code>'''
  sys.exit(1)

option_list = 'f:c:'

try:
  opts, args = getopt(sys.argv[1:], option_list)
except GetoptError as err:
  print str(err)
  usage()

# # Defaults
# country_code = 'US'
# FREQ = 93.9  

# User-defined
for opt, val in opts:
  if opt == '-f':
    FREQ = val
  elif opt == '-c':
    country_code = val


# The infinite loop

# while True:
  
# Generate EEPROM settings based on country location
# country_code = raw_input('Enter the two letter country code, ex: US: ') 
presets = country_code_presets.get_preset(country_code)
if presets == -1:
  sys.exit(1)
  print "Error: country not found"
  # continue  

# Pass in tuning frequency.   
# FREQ = raw_input('Enter the FM Frequency: ') 
print 'STATUS: using frequency', FREQ

# Create temporary file
TMP_FILE_PATH = '/home/pi/TPR_ops/temp/eeprom' #= tempfile.mkdtemp(suffix = 'eemprom', dir = /tmp)[1]
print TMP_FILE_PATH
TMP_FILE = open(TMP_FILE_PATH, 'w')
print TMP_FILE

# Get hex file to write to radio
print 'STATUS: writing hex file'
exit = call(['sudo', 'python', '/home/pi/TPR_ops/tools/programmer/eeprom.py', '-f', FREQ, '-b', presets['band'],'-d', presets['deemphasis'], '-s', presets['channel_spacing']] > TMP_FILE)
if exit != 0:
  sys.exit(1)
  print 'ERROR: failed to write hex file. Log below'
  call(['cat', TMP_FILE_PATH])
  # continue
print 'SUCCESS: hex file written with contents below'

call(['cat', TMP_FILE_PATH])

# #####################END##############################

# # Make sure radio is on jig
# # Using raw input here, this could be triggered by Tulip via the footpedal if we want 
# raw_input('Press enter when radio is on jig')

# # Run electrical test
# # TO DO: ADD ETEST CODE HERE! 

# # Program radio
# print 'STATUS: programming radio with frequency', FREQ
# print 'STATUS: using program', PROGRAM
# print TMP_FILE_PATH 

# exit = os.system('sudo avrdude -P usb -c ' + PROGRAM +' -p attiny45 -B 5 -b 9600 -e -U flash:w:TPR_firmware.hex -U eeprom:w:' + TMP_FILE_PATH)
# if exit != 0:
#   print 'ERROR: failed to program radio'
# # TO DO: Add code here to update the database via Tulip for failed radios   
#   # continue
# print 'SUCCESS: programmed radio'

# # Transmit 1K test tone to programmed radio at desired frequency 
# Popen(['sudo','./pifm', '1KTest.wav', FREQ, '44100'])

#   # TO DO: Add code here to update the database via Tulip for successful radios 



