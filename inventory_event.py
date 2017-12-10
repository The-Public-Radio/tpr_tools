#!/usr/bin/env python

# This script records inventory events (creation of mechanically assembled radios,
# removal of mechanical components from inventory stores) in The Public Radio's
# inventory management spreadsheet on Google Sheets.
#
# It takes in:
#	* Operation (mechanical assembly created OR order fulfilled)
#	* Username (just a string)


import gspread
import time
import os
import sys
from oauth2client.service_account import ServiceAccountCredentials

# Set username. Ideally the username is always set to be a person's name (or similar),
# but in the cases where it's not set then the Raspberry Pi's $HOSTNAME will suffice.
if (len(sys.argv) == 3):
	print 'three'
	username = sys.argv[2]
	print username
elif (len(sys.argv) == 2):
	print 'two'
	username = os.uname()[1]
	print username
else:
	print 'ERROR - wrong number of arguments.'
	print 'Usage: $ inventory_event.py <event> <username>'
	sys.exit(1)

events = ['assemble', 'fulfill']
event = sys.argv[1]

if event not in events:
	print 'ERROR - invalid event.'
	print 'Use `assemble` or `fulfill`.'
	sys.exit(1)
	

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/tpr-inv.json', scope)


c = gspread.authorize(credentials)
spreadsheet = c.open('PR9450 Part Usage')

worksheet = spreadsheet.worksheet("PR9027") 
print worksheet

print worksheet.acell('A2').value
row_to_add = ['foo', 'foo', 'three']
worksheet.append_row(["A", "B", "C"])