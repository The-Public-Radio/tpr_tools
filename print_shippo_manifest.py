import shippo
import datetime
import time

timestamp = datetime.datetime.now().isoformat()[:-3] + 'Z'

manifest = shippo.Manifest.create(
    carrier_account = carrier_account,
    shipment_date = timestamp,
    address_from = "c6036179a6f1412abf083cfe3fbd1867",
)
manifest_object = manifest["object_id"]

# the manifest will probably be queued (not completed) at this point
# wait a minute so that the object gets through Shippo's queue
print("waiting a minute...")
time.sleep(60)

shippo.Manifest.retrieve(manifest_object)

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