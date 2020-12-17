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
# get api keys
api_keys = {}
api_keys['tpr'] = os.getenv('SHIPPO_TOKEN_TPR')
api_keys['theprepared'] = os.getenv('SHIPPO_TOKEN_THEPREPARED')

companies = [
#	'tpr', 
	'theprepared',
]


for company in companies:
	print("Working on {}...".format(company))
	shippo.config.api_key = api_keys[company]
	try:
		manifest = shippo.Manifest.create(
			carrier_account = carrier_account[company],
			shipment_date = timestamp,
			address_from = from_address[company],
			async = False,
		)
		# with async unspecified the manifest will be QUEUED. if you use async manifest creation
		# sleep for a minute, then retrieve the manifest and grab the documents from it
		#manifest_object_id = manifest["object_id"]
		#print("waiting a minute...")
		#time.sleep(60)
		#manifest_object = shippo.Manifest.retrieve(manifest_object_id)
		#documents = manifest_object["documents"]
		documents = manifest["documents"]
		print("\tWe have documents!")
	except Exception as e:
		documents = ""
		print("\tAn error occurred creating a manifest via Shippo :(")
		print("\t", e)
if documents != "":
	print("\tLet's print them.")
	for url in documents:
		document = requests.get(url, allow_redirects=True)
		open('/home/pi/ops_tools/temp/manifest.pdf', 'wb').write(document.content)
		subprocess.run(['lp', '/home/pi/ops_tools/temp/manifest.pdf', '-o', 'fit-to-page'])
		os.remove('/home/pi/ops_tools/temp/manifest.pdf')
else:
	print("No documents to print!")