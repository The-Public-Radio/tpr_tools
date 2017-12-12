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

#def record_assemble(timestamp, user):
#	PCB = spreadsheet.worksheet("PR9027")
#	PCB.append_row(["radio_assemble", timestamp, "-1", user])
#	lid = spreadsheet.worksheet("PR1014")
#	lid.append_row(["radio_assemble", timestamp, "-1", user])
#	screw = spreadsheet.worksheet("PR2039")
#	screw.append_row(["radio_assemble", timestamp, "-4", user])	
#	knob = spreadsheet.worksheet("PR2036")
#	knob.append_row(["radio_assemble", timestamp, "-1", user])
#	mech_assy = spreadsheet.worksheet("PR2040")
#	mech_assy.append_row(["radio_assemble", timestamp, "+1", user])
#
#def record_fulfill(timestamp, user):
#	antenna = spreadsheet.worksheet("PR2034")
#	antenna.append_row(["radio_fulfill", timestamp, "-1", user])
#	box = spreadsheet.worksheet("PR2500")
#	box.append_row(["radio_fulfill", timestamp, "-1", user])
#	jar = spreadsheet.worksheet("PR1016")
#	jar.append_row(["radio_fulfill", timestamp, "-1", user])
#	mech_assy = spreadsheet.worksheet("PR2040")
#	mech_assy.append_row(["radio_assemble", timestamp, "-1", user])

def append_rows(worksheet, list_of_values):
	col_count = len(list_of_values[0])
	row_count = worksheet.row_count
	start_cell = worksheet.get_addr_int(row_count + 1, 1)
	end_cell = worksheet.get_addr_int(row_count + len(list_of_values), col_count)
	worksheet.add_rows(len(list_of_values))
	rng = worksheet.range('%s:%s' % (start_cell, end_cell))
	for cell in rng:
		cell.value = list_of_values[cell._row - row_count - 1][cell._col - 1]
	worksheet.update_cells(rng)

# Assembly parts:
PR9027 = []
PR1024 = []
PR2039 = []
PR2036 = []
PR2040 = []

# Fulfillment parts
PR2034 = []
PR2500 = []
PR1016 = []
PR2040 = []

#worksheets = ['PR9027', 'PR1024', 'PR2039', 'PR2036', 'PR2040', 'PR2034', 'PR2500', 'PR1016', 'PR2040']
worksheets = ['PR9040']

with open(stored_events_file, 'rwb') as f:
	csvreader = csv.reader(f, delimiter = ',')
	next(csvreader, None)
	for row in csvreader:
		if (row[0] == 'assemble'):
			print 'Looks like', row[2], 'assembled a radio at', row[1]
			PR9027.append([row[0], row[1], '-1', row[2]])
			PR1024.append([row[0], row[1], '-1', row[2]])
			PR2039.append([row[0], row[1], '-4', row[2]])
			PR2036.append([row[0], row[1], '-1', row[2]])
			PR2040.append([row[0], row[1], '1', row[2]])
		elif (row[0] == 'fulfill'):
			print 'Looks like', row[2], 'fulfilled a radio at', row[1]
			PR2034.append([row[0], row[1], '-1', row[2]])
			PR2500.append([row[0], row[1], '-1', row[2]])
			PR1016.append([row[0], row[1], '-1', row[2]])
			PR2040.append([row[0], row[1], '-1', row[2]])
		else:
			print 'ERROR - CSV file is not properly formatted.'
			print 'Exiting.'
			sys.exit(1)

print PR9040

#for w in worksheets:
#	sheet = spreadsheet.worksheet(w)
#	append_rows('%s', w[] % w)



print 'Done!'
sys.exit(0)
