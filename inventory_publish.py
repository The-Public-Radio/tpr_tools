#!/usr/bin/env python


import gspread
import sys
from os import uname
import csv
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/tpr-inv.json', scope)
c = gspread.authorize(credentials)

if (uname()[1] == 'TPR-0'):
	print 'this is TPR-0'
	spreadsheet = c.open('PR9450 Part Usage_Brooklyn')
else:
	print 'this is *not* TPR-0'
	spreadsheet = c.open('PR9450 Part Usage_WAi')

stored_events_file = '/home/pi/ops_tools/data/stored_inventory_events.csv'

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
PR1014 = []
PR2039 = []
PR2036 = []
PR2043 = []

# Fulfillment parts
PR2034 = []
PR2500 = []
PR1016 = []
PR2043 = []

worksheets = [['PR9027', PR9027], ['PR1014', PR1014], ['PR2039', PR2039], ['PR2036', PR2036], ['PR2043', PR2043], ['PR2034', PR2034], ['PR2500', PR2500], ['PR1016', PR1016]]

with open(stored_events_file, 'rwb') as f:
	csvreader = csv.reader(f, delimiter = ',')
	next(csvreader, None)
	for row in csvreader:
		if (row[0] == 'assemble'):
			print 'Looks like', row[2], 'assembled a radio at', row[1]
			PR9027.append([row[0], row[1], '-1', row[2]])
			PR1014.append([row[0], row[1], '-1', row[2]])
			PR2039.append([row[0], row[1], '-4', row[2]])
			PR2036.append([row[0], row[1], '-1', row[2]])
			PR2043.append([row[0], row[1], '1', row[2]])
		elif (row[0] == 'fulfill'):
			print 'Looks like', row[2], 'fulfilled a radio at', row[1]
			PR2034.append([row[0], row[1], '-1', row[2]])
			PR2500.append([row[0], row[1], '-1', row[2]])
			PR1016.append([row[0], row[1], '-1', row[2]])
			PR2043.append([row[0], row[1], '-1', row[2]])
		else:
			print 'ERROR - CSV file is not properly formatted.'
			print 'Exiting.'
			sys.exit(1)

if len(PR2043):
	for w in worksheets:
		if len(w[1]):
			print 'Updating usage of', w[0]
			sheet = spreadsheet.worksheet("%s" % w[0])
			append_rows(sheet, w[1])
		else:
			print 'No recorded usage of', w[0],'!'
	f = open(stored_events_file, 'w')
	f.write('event,timestamp,user\n')
	f.close()
	print 'All events recorded!'
	sys.exit(0)
else:
	print 'No events to record!'
	sys.exit(0)
