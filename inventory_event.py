#!/usr/bin/env python

# This script records inventory events (creation of mechanically assembled radios,
# removal of mechanical components from inventory stores) in a CSV file on one of TPR's RPis.
#
# It takes in:
#	* Operation (mechanical assembly created OR order fulfilled)
#	* Username (optional, just a string)

import datetime
from os import uname
import sys

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


def store_event(user):
	f = open('/home/pi/ops_tools/data/stored_inventory_events.csv','a')
	f.write('%s,%s,%s\n' % (event, timestamp, user))
	f.close()

store_event(username)
sys.exit(0)
