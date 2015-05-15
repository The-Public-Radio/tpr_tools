import os
import sys
sys.path.append('../config')
import constants
import google

import xml

ENDICIA_XML = 'endicia_export_log.xml'

# Cache data locally to speed up; WARNING: dangerous if people editing while
# running script. This is also really slow.
data = google.sheet.col_values(constants.COL['EMAIL'])
print 'Data cached!'

# Read Endicia output
root = xml.etree.ElementTree.parse(ENDICIA_XML).getroot()

# Loop through all of the labels (i.e., each backer)
for label in root:

  # Grab the email address and PIC (i.e., tracking number)
  email = pic = None
  for key in label:
    if key.tag == 'ToEmail':
      email = key.text
    elif key.tag == 'PIC':
      pic = key.text

  if email != None and pic != None:
    try:
      index = data.index(email)
      google.sheet.update_cell(index + 1, constants.COL['PIC'], pic)
      google.sheet.update_cell(index + 1, constants.COL['STATUS'], constants.STATUS['shipping_label_created'])
      print 'Updated!', email, pic, index
    except ValueError:
      print email, 'not found!'