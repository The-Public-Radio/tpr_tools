import os
import sys
sys.path.append('../config')
import constants

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

CREDS = open(os.path.join('..', constants.GOOGLE_CREDENTIALS), 'r')

# Authenticate and grab reference to Google Spreadsheet
json_key = json.load(CREDS)
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

print 'STATUS: authenticated with Google!'

sheet = gc.open_by_key(constants.SPREADSHEET_KEY).worksheet('data')
