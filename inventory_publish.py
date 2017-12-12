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

def record_assemble(timestamp, user):
	PCB = spreadsheet.worksheet("PR9027")
	PCB.append_row(["radio_assemble", timestamp, "-1", user])
	lid = spreadsheet.worksheet("PR1014")
	lid.append_row(["radio_assemble", timestamp, "-1", user])
	screw = spreadsheet.worksheet("PR2039")
	screw.append_row(["radio_assemble", timestamp, "-4", user])	
	knob = spreadsheet.worksheet("PR2036")
	knob.append_row(["radio_assemble", timestamp, "-1", user])
	mech_assy = spreadsheet.worksheet("PR2040")
	mech_assy.append_row(["radio_assemble", timestamp, "+1", user])

def record_fulfill(timestamp, user):
	antenna = spreadsheet.worksheet("PR2034")
	antenna.append_row(["radio_fulfill", timestamp, "-1", user])
	box = spreadsheet.worksheet("PR2500")
	box.append_row(["radio_fulfill", timestamp, "-1", user])
	jar = spreadsheet.worksheet("PR1016")
	jar.append_row(["radio_fulfill", timestamp, "-1", user])
	mech_assy = spreadsheet.worksheet("PR2040")
	mech_assy.append_row(["radio_assemble", timestamp, "-1", user])

with open(stored_events_file, 'rwb') as f:
	csvreader = csv.reader(f, delimiter = ',')
	next(csvreader, None)
	for row in csvreader:
		if (row[0] == 'assemble'):
			print 'Looks like', row[2], 'assembled a radio at' row[1]
			record_assemble(row[1], row[2])
		elif (row[0] == 'fulfill'):
			print 'Looks like', row[2], 'fulfilled a radio at' row[1]
			record_fulfill(row[1], row[2])
		else:
			print 'ERROR - CSV file is not properly formatted.'
			print 'Exiting.'
			sys.exit(1)

print 'Done!'
sys.exit(0)
