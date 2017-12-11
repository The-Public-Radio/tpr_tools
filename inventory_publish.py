#!/usr/bin/env python


import gspread
import sys
import csv
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/tpr-inv.json', scope)
c = gspread.authorize(credentials)
spreadsheet = c.open('PR9450 Part Usage')

stored_events_file = '/home/pi/ops_tools/data/stored_inventory_events.csv'

with open(stored_events_file, 'rwb') as f:
	csvreader = csv.reader(f, delimiter = ',')
	for row in csvreader:
		if (row[1] == assemble):
			print 'We\'ve got an assemble row!'
			print 'Looks like', row[2], ' assembled a radio.'
			# do some stuff
		elif (row[1] == fulfill):
			# do other stuff
			print 'We\'ve got a fulfill row!'
			print 'Looks like', row[2], ' fulfilled a radio.'
		else:
			print 'ERROR - CSV file is not properly formatted.'
			print 'Exiting.'
			sys.exit(1)

print 'Done!'
sys.exit(0)
