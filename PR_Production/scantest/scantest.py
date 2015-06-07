import sys, os, re
sys.path.append('../config')
import constants
import google
import urllib2
import ujson
import tempfile
import country_code_presets

from subprocess import call
from subprocess import Popen
import etest2

TEST = False
# if len(sys.argv) > 1:
#   TEST = True

if len(sys.argv) > 1:
  PROGRAM = sys.argv[1]
else:
  PROGRAM = 'usbtiny'

PICs = []
SERIALs = []
FREQs = []
COUNTRYs = []

if not TEST:
  # data = google.sheet.get_all_values()

  url = 'https://spreadsheets.google.com/feeds/list/' + constants.SPREADSHEET_KEY + '/od6/public/values?alt=json'
  raw = urllib2.urlopen(url).read()
  print 'STATUS: done downloading!'
  data = ujson.loads(raw)['feed']['entry']

  for row in data:
    PICs.append(row['gsx$pic']['$t'])
    SERIALs.append(row['gsx$serial']['$t'])
    FREQs.append(row['gsx$freq']['$t'])
    COUNTRYs.append(row['gsx$shippingcountrycode']['$t'])

else:
  PICs = ['Tracking Number', '42011222','42011216', '1Z0363374446316122', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '9405510200829591004800', None, None, None, None, None, '9405510200828591075179', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '9405510200829591004770', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '9405510200881590971187', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '9405510200882591104192']
  SERIALs = ['Serial Number']
  FREQs = ['Frequencies', '98.0', '93.9']
  COUNTRYs = ['Country Code', 'BE', 'AF']

  # Make sure all SERIALs and FREQs have the same length as PICs (gspread returns
  # columns as arrays of data only and ignores rows that are blank, even if there
  # are values in the same row, but in other colums).
  SERIALs.extend([None] * (len(PICs) - len(SERIALs)))
  FREQs.extend([None] * (len(PICs) - len(FREQs)))
  COUNTRYs.extend([None] * (len(PICs) - len(COUNTRYs)))

print 'STATUS: data cached!'

# The infinite loop
while True:

  # Get shipping number
  PIC = raw_input('Please scan shipping number: ')
  PIC = PIC if PIC[0] == 'L' else PIC[9:]
  print 'STATUS: PIC received ' + PIC

  # Check length of shipping number
  # if len(PIC) != 22:
  #   print 'ERROR: shipping number not 22 characters'
  #   continue

  if PIC not in PICs:
    print 'ERROR: shipping number not found'
    continue

  # Get row # of shipping label
  INDEX = PICs.index(PIC)

  # Check if there's already a serial number for this shipping number
  if SERIALs[INDEX].strip() != '':
    print 'ERROR: shipping number already has an associated serial number ' + SERIALs[INDEX].strip()
    continue
    
  print 'SUCCESS: shipping number valid and exists in database', PIC

  # Get country presets
  presets = country_code_presets.get_preset(COUNTRYs[INDEX])
  print 'STATUS: got presets'
    
  # Get serial number
  SERIAL = raw_input('Please scan serial number: ')
  if len(SERIAL) != 3 and len(SERIAL) != 4:
    print 'ERROR: serial number not 3 or 4 characters'
    continue
  if SERIAL in SERIALs:
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
  google.sheet.update_cell(INDEX + 2, constants.COL['SERIAL'], SERIAL)
  google.sheet.update_cell(INDEX + 2, constants.COL['STATUS'], constants.STATUS['serial_number_assigned'])
  SERIALs[INDEX] = SERIAL

  print 'STATUS: success! now do the next one...'


