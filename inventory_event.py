#!/usr/bin/env python

# This script records inventory events (creation of mechanically assembled radios,
# removal of mechanical components from inventory stores) in The Public Radio's
# inventory management spreadsheet on Google Sheets.
#
# It takes in:
#	* Operation (mechanical assembly created OR order fulfilled)
#	* Username (just a string)

import gspread
import datetime
from os import uname
import sys
import csv
from oauth2client.service_account import ServiceAccountCredentials

# Set username. Ideally the username is always set to be a person's name (or similar),
# but in the cases where it's not set then the Raspberry Pi's $HOSTNAME will suffice.
if (len(sys.argv) == 3):
	username = sys.argv[2]
elif (len(sys.argv) == 2):
	username = uname()[1]
else:
	print 'ERROR - wrong number of arguments.'
	print 'Usage: $ inventory_event.py <event> <username>'
	sys.exit(1)

events = ['assemble', 'fulfill']
event = sys.argv[1]

# Confirm that the user wants to do a valid operation.
if event not in events:
	print 'ERROR - invalid event:', event
	print 'Use `assemble` or `fulfill`.'
	sys.exit(1)

timestamp = datetime.datetime.now().isoformat()
print 'time is', timestamp

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/tpr-inv.json', scope)
c = gspread.authorize(credentials)
spreadsheet = c.open('PR9450 Part Usage')


# NOTE: This function takes a long time (~20s) to run. This is not practical for on-the-fly use,
# so this function is NOT currently being used.
def record_assemble(user):
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

# NOTE: This function takes a long time (~20s) to run. This is not practical for on-the-fly use,
# so this function is NOT currently being used.
def record_fulfill(user):
	antenna = spreadsheet.worksheet("PR2034")
	antenna.append_row(["radio_fulfill", timestamp, "-1", user])
	box = spreadsheet.worksheet("PR2500")
	box.append_row(["radio_fulfill", timestamp, "-1", user])
	jar = spreadsheet.worksheet("PR1016")
	jar.append_row(["radio_fulfill", timestamp, "-1", user])
	mech_assy = spreadsheet.worksheet("PR2040")
	mech_assy.append_row(["radio_assemble", timestamp, "-1", user])


def store_event(user):
	f = open('/home/pi/ops_tools/data/stored_inventory_events.csv','a')
	f.write('%s,%s,%s\n' % (event, timestamp, user))
	f.close()

store_event(username)

#if (event == 'assemble'):
#	store_assemble(username)
#elif (event == 'fulfill'):
#	store_fulfill(username)




#worksheet = spreadsheet.worksheet("PR9027") 
#print worksheet
#
#print worksheet.acell('A2').value
#worksheet.append_row(["A", "B", "C"])