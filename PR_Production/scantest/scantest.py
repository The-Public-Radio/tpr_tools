import sys, os, re
sys.path.append('../config')
import constants
import google
import urllib2
import ujson
import tempfile
from getopt import getopt, GetoptError
import country_code_presets

from subprocess import call
from subprocess import Popen
import etest2

def usage():
  print r'''Usage: python scantest.py -n <num radios> -p <programmer>'''
  sys.exit(1)

option_list = 'n:p:'

try:
  opts, args = getopt(sys.argv[1:], option_list)
except GetoptError as err:
  print str(err)
  usage()

# Defaults
PROGRAM = 'usbtiny'
NUM_RADIOS = 1

# User-defined
for opt, val in opts:
  if opt == '-p':
    PROGRAM = val
  elif opt == '-n':
    NUM_RADIOS = int(val)

PICs = []
SERIALs = []
FREQs = []
COUNTRYs = []
NUM_RADIOs = []

url = 'https://spreadsheets.google.com/feeds/list/' + constants.SPREADSHEET_KEY + '/od6/public/values?alt=json'
raw = urllib2.urlopen(url).read()
print 'STATUS: done downloading!'
data = ujson.loads(raw)['feed']['entry']

for row in data:
  PICs.append(row['gsx$pic']['$t'])
  SERIALs.append(row['gsx$serial']['$t'])
  FREQs.append(row['gsx$freq']['$t'])
  COUNTRYs.append(row['gsx$shippingcountrycode']['$t'])
  NUM_RADIOs.append(int(row['gsx$numradios']['$t']))

print 'STATUS: data cached!'

# The infinite loop
while True:

  print '---------------------------------------'
  print 'STARTING NEW SHIPPING NUMBER'
  print '---------------------------------------'

  # Get shipping number
  PIC = raw_input('Please scan shipping number: ')
  PIC = PIC if PIC[0] == 'L' else PIC[9:]
  print 'STATUS: PIC received ' + PIC

  if PIC not in PICs:
    print 'ERROR: shipping number not found'
    continue

  # Get row # of shipping label
  INDEX = PICs.index(PIC)

  # Get country presets
  presets = country_code_presets.get_preset(COUNTRYs[INDEX])
  if presets == -1:
    print "ERROR: country not found. Please set aside!!!"
    continue

  print 'STATUS: got presets'
    
  # Loop through number of radios / shipping label
  for r_index in range(NUM_RADIOs[INDEX]):
    print '-----> RADIO', str(r_index + 1), 'OF', str(NUM_RADIOs[INDEX])

    # Check if there's already a serial number for this shipping number
    if len(SERIALs[INDEX].strip().split('|')) >= NUM_RADIOs[INDEX] and not SERIALs[INDEX].strip() == '':
      print 'ERROR: shipping number already has ' + str(NUM_RADIOs[INDEX]) + ' radios associated with serial(s) ' + SERIALs[INDEX].strip()
      continue
      
    print 'SUCCESS: shipping number valid and exists in database', PIC

    # Get serial number
    SERIAL = raw_input('Please scan serial number: ')
    if len(SERIAL) != 3 and len(SERIAL) != 4:
      print 'ERROR: serial number not 3 or 4 characters'
      continue

    for LIST in SERIALs:
      if SERIAL in LIST.split('|'):
        print 'ERROR: serial number already used'
        continue
    print 'SUCCESS: serial number valid', SERIAL

    # Get frequency
    FREQ = FREQs[INDEX]
    print 'STATUS: using frequency', FREQ

    # Create temporary file
    TMP_FILE_PATH = tempfile.mkstemp()[1]
    TMP_FILE = open(TMP_FILE_PATH, 'w')

    # Get hex file to write to radio
    print 'STATUS: writing hex file'
    exit = call(['python', 'eeprom.py', '-f', FREQ, '-b', presets['band'], '-d', presets['deemphasis'], '-s', presets['channel_spacing']], stdout=TMP_FILE)
    if exit != 0:
      print 'ERROR: failed to write hex file. Log below'
      call(['cat', TMP_FILE_PATH])
      continue
    print 'SUCCESS: hex file written with contents below'
    call(['cat', TMP_FILE_PATH])
  	
    # Make sure radio is on jig
    raw_input('Press enter when radio is on jig')

    # Run electrical test
    print 'STATUS: running electrical test'
    if etest2.etest() != 0:
      print 'ERROR: failed electrical test'
      continue
    print 'SUCCESS: passed electrical test'

    # Start wav file
    Popen(['sudo', './pifm', '1ktest.wav', FREQ, '44100'])

    # Program radio
    print 'STATUS: programming radio with frequency', FREQ
    print 'STATUS: using program', PROGRAM
    print TMP_FILE_PATH
    exit = os.system('sudo avrdude -P usb -c ' + PROGRAM +' -p attiny45 -e -U flash:w:pr.hex -U eeprom:w:' + TMP_FILE_PATH)
    if exit != 0:
      print 'ERROR: failed to program radio'
      continue
    print 'SUCCESS: programmed radio'

    # Updating main database and local cache
    print 'STATUS: updating database'
    SERIALs[INDEX] = SERIAL if r_index == 0 else SERIALs[INDEX] + '|' + SERIAL
    google.sheet.update_cell(INDEX + 2, constants.COL['SERIAL'], SERIALs[INDEX])
    google.sheet.update_cell(INDEX + 2, constants.COL['STATUS'], constants.STATUS['serial_number_assigned'])

    print 'STATUS: success! now do the next one...'


