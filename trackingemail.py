#This script is meant to send a notification email to customers 
#It should be triggered as close to the actual shipping pickup as possible,
#likely this means triggering once a an order is marked as boxed.   


from getopt import getopt, GetoptError
import requests
import sys, os

subdomain = 'tracking.thepublicrad.io'

if (len(sys.argv) != 4):
	print 'ERROR - wrong number of arguments.'
	print 'Usage: `$ trackingemail.py <email addressr> <tracking number> <mailgun api key>`'
	sys.exit(1)

# set input variables
recipient = sys.argv[1]
tracking = sys.argv[2]
key = sys.argv[3]


# email variables 
request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(subdomain)
request = requests.post(request_url, auth=('api', key), data={
    'from': 'PublicRadioShipments@thepublicrad.io',
    'to': recipient,
    'subject': "Your Public Radio is on its way!",
    'text': "Hi there,\n\n" +
    "We're delighted to let you know that your Public Radio has been programmed & boxed and is waiting to be picked up!" + 
    "You can follow along with your USPS tracking number (which may take a day or so to update) here:\n\n" + 
    "https://tools.usps.com/go/TrackConfirmAction.action?tLabels="+tracking+
    "\n\nCheers,\nZach & Spencer\n" +
    "The Public Radio"
})


# exit codes 
print 'Status: {0}'.format(request.status_code)
print 'Body:   {0}'.format(request.text)
