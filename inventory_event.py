#!/usr/bin/env python

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/tpr-inv.json', scope)


c = gspread.authorize(credentials)
spreadsheet = c.open('PR9450 Part Usage')
print(spreadsheet)
worksheet = spreadsheet.worksheet("PR9027") 
print(worksheet)

print(worksheet.acell('A2').value)
row_to_add = ['foo', 'foo', 'three']
worksheet.append_row(["A", "B", "C"])