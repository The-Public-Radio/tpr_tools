import urllib2
import ujson
import csv
from collections import OrderedDict
from UnicodeCSV import UnicodeWriter
import os, sys

if len(sys.argv) > 1:
  NUM_BACKERS = int(sys.argv[1])
else:
  NUM_BACKERS = 99999

if len(sys.argv) > 2:
  SPREADSHEET_KEY = sys.argv[2]
else:
  # KUER: 1nIryj50yzO8-TlaOMa2pqKDhSTY6Du2Rr4BFszI4EUU/ooo4zw2
  # Master $48: 1-EGfK3dHh24X8zoXzpqRP0dJvDkVwvDxS42ciiui7k8/od6
  SPREADSHEET_KEY = '1-EGfK3dHh24X8zoXzpqRP0dJvDkVwvDxS42ciiui7k8/od6'

OUTPUT_DIR = 'output'
ENDICIA_US_CSV = OUTPUT_DIR + '/endicia_us.csv'
ENDICIA_INTL_CSV = OUTPUT_DIR + '/endicia_intl.csv'
ENDICIA_UNKNOWN_CSV = OUTPUT_DIR + '/endicia_unknown.csv'

if not os.path.exists(OUTPUT_DIR):
  os.makedirs(OUTPUT_DIR)

# For whatever reason, internet is slow; set to True to use local version of
# data (local data / data in repo is bad. Don't do this. But we did)
TESTING = False

if TESTING:
  raw = open('data.json').read()
  print 'done reading!'
else:
  url = 'https://spreadsheets.google.com/feeds/list/' + SPREADSHEET_KEY + '/public/values?alt=json'
  raw = urllib2.urlopen(url).read()
  print 'STATUS: done downloading!'

db = ujson.loads(raw)['feed']['entry']
print 'Number of backers in db:', len(db)

endicia_column_mapping = OrderedDict([
  ('Shipping Name', 'gsx$shippingname'),
  ('Company', None),
  ('Shipping Address 1', 'gsx$shippingaddress1'),
  ('Shipping Address 2', 'gsx$shippingaddress2'),
  ('Shipping City', 'gsx$shippingcity'),
  ('Shipping State', 'gsx$shippingstate'),
  ('Shipping Postal Code', 'gsx$shippingpostalcodecalc'),
  ('Shipping Country', 'gsx$shippingcountrycode'),
  ('Phone', None),
  ('Email', 'gsx$email'),
  ('Backer number', 'gsx$backernumber'),
  ('Backer uid', 'gsx$backeruid')]
)

# Create files
endicia_us = open(ENDICIA_US_CSV, 'w')
endicia_intl = open(ENDICIA_INTL_CSV, 'w')
endicia_unknown = open(ENDICIA_UNKNOWN_CSV, 'w')

# Create CSV writers
writer_us = UnicodeWriter(endicia_us, quotechar='"', quoting=csv.QUOTE_ALL)
writer_intl = UnicodeWriter(endicia_intl, quotechar='"', quoting=csv.QUOTE_ALL)
writer_unknown = UnicodeWriter(endicia_unknown, quotechar='"', quoting=csv.QUOTE_ALL)

# Create headers
writer_us.writerow(endicia_column_mapping.keys())
writer_intl.writerow(endicia_column_mapping.keys())
writer_unknown.writerow(endicia_column_mapping.keys())

backerCount = 0

# Loop over all the rows
for backer in db:

  # Ignore backers that already have shipping label
  if backer['gsx$pic']['$t'] != '':
    continue

  # Stop loop if we've gotten enough labels
  backerCount += 1
  if backerCount > NUM_BACKERS:
    break

  # Create empty row
  row = []

  # Loop over each field (backer)
  for key in endicia_column_mapping.keys():
  # [backer[endicia_column_mapping[field]]['$t'] for field in endicia_column_mapping.keys()]
    field = endicia_column_mapping[key]
    if field == None:
      row.append('')
    else:
      # NOTE: Replacing new line characters within a cell with space
      row.append(backer[field]['$t'].replace('\n', ' '))

  # Write filled row to cs
  country = backer['gsx$shippingcountrycode']['$t']
  if country == 'US':
    writer_us.writerow(row)
  elif country.strip() != '':
    writer_intl.writerow(row)
  else:
    writer_unknown.writerow(row)

# Close files
endicia_us.close()
endicia_intl.close()
endicia_unknown.close()
