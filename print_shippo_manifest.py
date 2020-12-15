import shippo
import datetime
import time
import requests
import subprocess
import os

timestamp = datetime.datetime.now().isoformat()[:-3] + 'Z'

# get carrier accounts
carrier_account = {}
carrier_account['tpr'] = os.getenv('CARRIER_ACCOUNT_TPR')
carrier_account['theprepared'] = os.getenv('CARRIER_ACCOUNT_THEPREPARED')
# get from_addresses
from_address = {}
from_address['tpr'] = os.getenv('ADDRESS_FROM_TPR')
from_address['theprepared'] = os.getenv('ADDRESS_FROM_THEPREPARED')

companies = ['tpr']

for company in companies:
	manifest = shippo.Manifest.create(
	    carrier_account = carrier_account[company],
	    shipment_date = timestamp,
	    address_from = from_address[company],
	)
	manifest_object_id = manifest["object_id"]

	# the manifest will probably be queued (not completed) at this point
	# wait a minute so that the object gets through Shippo's queue
	print("waiting a minute...")
	time.sleep(60)

	manifest_object = shippo.Manifest.retrieve(manifest_object_id)
	documents = manifest_object["documents"]

	for url in documents:
		document = requests.get(url, allow_redirects=True)
		open('/home/pi/ops_tools/temp/manifest.pdf', 'wb').write(document.content)
		subprocess.run(['lp', '/home/pi/ops_tools/temp/manifest.pdf', '-o', 'fit-to-page'])
		os.remove('/home/pi/ops_tools/temp/manifest.pdf')




#https://shippo-delivery-east.s3.amazonaws.com/92750901649158000314205469_5630_usps.pdf?Signature=uszFTT4H%2Fj6T3z3saizZZr6G1B0%3D&Expires=1639533640&AWSAccessKeyId=AKIAT3Z7F7EU3MDETVFS
#lpadmin -p M479FDW -v socket://192.168.1.128 -P

#{
#  "address_from": "c6036179a6f1412abf083cfe3fbd1867",
#  "carrier_account": "",
#  "documents": [],
#  "errors": [],
#  "object_created": "2020-12-15T02:00:39.655Z",
#  "object_id": "859ef2898b104efab1530938d4ee92ea",
#  "object_owner": "info@thepublicrad.io",
#  "object_updated": "2020-12-15T02:00:39.655Z",
#  "provider": "usps",
#  "shipment_date": "2020-12-14T20:00:00Z",
#  "status": "QUEUED",
#  "transactions": []
#}