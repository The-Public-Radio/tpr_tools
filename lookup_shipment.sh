#!/bin/bash

# This script looks up a shipment and returns relevant info

# Info to get:
#	* name
#	* street_address_1
#	* street_address_2
#	* city
#	* state
#	* postal_code
#	* order_source
#	* uncommon goods order number
#	* radio 1 frequency
#	* radio 2 frequency
#	* radio 3 frequency

if [ "$#" -ne 3 ]; then
  echo "Wrong number of arguments!"
  echo "Usage: $ lookup_shipment.sh <tracking_number> <env> <auth_token>" >&2
  exit 1
fi

tracking_number=$1
auth_token=$3

# Helper functions
script_help() {
  cat <<- EOM
Usage:
./lookup_shipment.sh <tracking_number> <env> <auth_token>

Options:
----------------
<tracking_number>
<environment>	"production" or "staging"			
<auth_token>  	API key
----------------
EOM
exit
}

# Check env
if [[ $2 == 'production' ]]; then
  url='api.thepublicrad.io';
  headers="Authorization: Bearer $auth_token";
elif [[ $2 == 'staging' ]]; then
  url='api-staging.thepublicrad.io';
  headers="Authorization: Bearer $auth_token";
else
  script_help
fi

shipment=$(curl -s -H "$headers" $url/shipments?tracking_number=$tracking_number \
	| jq -c '[.data | {id: .id, order_id: .order_id}][]')
shipment_id=$(echo -n $shipment | jq '.id')
order_id=$(echo -n $shipment | jq '.order_id');

#echo "shipment_id is" $shipment_id
#echo "order_id is" $order_id

order=$(curl -s -H "$headers" $url/orders/$order_id)
name=$(echo -n $order | jq '.name')
street_address_1=$(echo -n $order | jq '.street_address_1')
street_address_2=$(echo -n $order | jq '.street_address_2')
city=$(echo -n $order | jq '.city')
state=$(echo -n $order | jq '.state')
postal_code=$(echo -n $order | jq '.postal_code')
order_source=$(echo -n $order | jq '.order_source')

#echo "order is" $order
#echo "name is" $name
#echo "street_address_1 is" $street_address_1
#echo "street_address_2 is" $street_address_2
#echo "city is" $city
#echo "state is" $state
#echo "postal_code is" $postal_code
#echo "order_source is" $order_source


radios=($(curl -s -H "$headers" $url/shipments/$shipment_id/radios | jq -c '[.data[] | .frequency][]' | sed 's/"//g'))

radio_count=${#radios[@]}
#echo "radio_count is" $radio_count

output="$order_source order_number $name $street_address_1 $street_address_2 $city $state $postal_code 'a very very very very very long message' ${radios[0]} ${radios[1]} ${radios[2]}"
echo $output







