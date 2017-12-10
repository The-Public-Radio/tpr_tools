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

#print username

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/tpr-inv.json', scope)


c = gspread.authorize(credentials)
spreadsheet = c.open('PR9450 Part Usage')
print spreadsheet
worksheet = spreadsheet.worksheet("PR9027") 
print worksheet

print worksheet.acell('A2').value
row_to_add = ['foo', 'foo', 'three']
worksheet.append_row(["A", "B", "C"])