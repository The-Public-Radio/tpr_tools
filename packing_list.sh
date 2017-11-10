#!/bin/bash



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

# get the shipment, shipment_id and order_id
shipment=$(curl -s -H "$headers" $url/shipments?tracking_number=$tracking_number \
	| jq -c '[.data | {id: .id, order_id: .order_id}][]')
shipment_id=$(echo -n $shipment | jq '.id')
order_id=$(echo -n $shipment | jq '.order_id');

# get all of the order info. strip the quotes off.
order=$(curl -s -H "$headers" $url/orders/$order_id)
name=$(echo -n $order | jq '.name')
name=$(eval echo $name)
street_address_1=$(echo -n $order | jq '.street_address_1')
street_address_1=$(eval echo $street_address_1)
street_address_2=$(echo -n $order | jq '.street_address_2')
street_address_2=$(eval echo $street_address_2)
city=$(echo -n $order | jq '.city')
city=$(eval echo $city)
state=$(echo -n $order | jq '.state')
state=$(eval echo $state)
postal_code=$(echo -n $order | jq '.postal_code')
postal_code=$(eval echo $postal_code)
order_source=$(echo -n $order | jq '.order_source')
order_source=$(eval echo $order_source)
message=$""

echo "street_address_2 is" $street_address_2

# get the radios in the shipment, put the frequencies in an array
radios=($(curl -s -H "$headers" $url/shipments/$shipment_id/radios | jq -c '[.data[] | .frequency][]' | sed 's/"//g'))
# get the number of radios in the shipment, for good measure
radio_count=${#radios[@]}
echo "radio_count is" $radio_count


# create order info image
if [ "$message" == "" ]; then
   convert -pointsize 32 -font /usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 601.5x864 caption:'To:\n'"$name"'\n'"$street_address_1"'\n'"$street_address_2"'\n'"$city"', '"$state"'\n'"$postal_code"'\n\nOrder no:\n'"$order_no" \
	/home/pi/ops_tools/temp/order_info.png
else
	convert -pointsize 32 -font /usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 601.5x864 caption:'To:\n'"$name"'\n'"$street_address_1"'\n'"$street_address_2"'\n'"$city"', '"$state"'\n'"$postal_code"'\n\nOrder no:\n'"$order_no"'\n\nMessage:\n'"$message" \
	/home/pi/ops_tools/temp/order_info.png
fi

# debug - print just the order info
#lpr -P DYMO_LabelWriter_450_Turbo /home/pi/ops_tools/temp/order_info.png

# merge order_info into background
convert /home/pi/ops_tools/data/uncommongoods_background.png /home/pi/ops_tools/temp/order_info.png \
-gravity center -geometry +0-113 -composite /home/pi/ops_tools/temp/packing_list.png

# create part list, and make it the right number of rows
if [[ radio_count -eq 1 ]]; then
	convert -pointsize 32 -font /usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 601.5x192 caption:'Qty Item               Freq\n\n1   The Public Radio   '"${radios[0]}" \
	/home/pi/ops_tools/temp/part_list.png
elif [[ radio_count -eq 2 ]]; then
	convert -pointsize 32 -font /usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 601.5x192 caption:'Qty Item               Freq\n\n1   The Public Radio   '"${radios[0]}"'\n1   The Public Radio   '"${radios[1]}" \
	/home/pi/ops_tools/temp/part_list.png
elif [[ radio_count -eq 3 ]]; then
	convert -pointsize 32 -font /usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 601.5x192 caption:'Qty Item               Freq\n\n1   The Public Radio   '"${radios[0]}"'\n1   The Public Radio   '"${radios[1]}"'\n1   The Public Radio   '"${radios[2]}" \
	/home/pi/ops_tools/temp/part_list.png
else
	echo "no radios!"
	exit 1
fi

#merge part_list into packing_list
convert /home/pi/ops_tools/temp/packing_list.png /home/pi/ops_tools/temp/part_list.png \
-gravity center -geometry +0+356 -composite /home/pi/ops_tools/temp/packing_list.png

# print the result
lpr -P DYMO_LabelWriter_450_Turbo_Paper /home/pi/ops_tools/temp/packing_list.png


# delete all the temp files
#srm -rf /home/pi/ops_tools/temp/*



