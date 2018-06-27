#!/bin/bash
#
# Print return labels for a warranty shipment
# Usage:
# ./print_return_label.sh <env> <tracking_number> <auth_token>
#
# <env>                 environment to download label for [staging, production]
# <tracking_number>		Tracking number of primary shipment
# <auth_token>          tpr-coordinator auth token


# Helper functions
script_help() {
	cat <<- EOM
Usage:
./print_return_label.sh <env> <tracking_number> <auth_token>

Options:
----------------
<env>                   environment to download labels for [staging, production]
<tracking_number>		Tracking number of primary shipment
<auth_token>            tpr-coordinator auth token
----------------
EOM
exit
}
clean_up() {
	rm -rf $tmp_dir/*
}

# Set some base variables

# Check ARGV and send HELP!
if [[ $1 == "--help" || "$#" -lt 1 ]];
  then script_help;
fi

# Set auth tokencn
auth_token="$3";

# Set tracking number 
tracking_number=$2

# Check env
if [[ $1 == 'production' ]]; then
	url='api.thepublicrad.io';
	headers="Authorization: Bearer $auth_token";
elif [[ $1 == 'staging' ]]; then
	url='api-staging.thepublicrad.io';
	headers="Authorization: Bearer $auth_token";
else
	script_help
fi

# set temp directory variable. temp directory should be inside the directory that the script is located in.
basename="$(dirname $0)"
tmp_dir="$basename/temp"

# make the temp directory. -p forces no error if temp directory already exists.
mkdir -p $tmp_dir

# move to the temp directory
cd $tmp_dir

# Pull down the shipment by tracking number
# Save the ID and return_label_url into an array
shipment=$(curl -s -H "$headers" $url/shipments?tracking_number=$tracking_number | jq -c '[.data | {id: .id, return_label_url: .return_label_url}][]')
echo "shipment is" $shipment

return_label_url=$(echo -n $shipment | jq -r '.return_label_url' | tr -d '\n')

echo "return_label_url is" $return_label_url

id=$(echo -n $shipment | jq '.id')

echo '----------------'
echo "id is" $id

# if $id isn't null, download it and then confirm.
if [ "$id" != "null" ];	then 
	# Download label from label_url
	curl "$return_label_url" > ./$id.pdf;
	echo "Downloaded return label for shipment $id!";
else 
	echo "No return label in the database!"
	clean_up
	exit 3
fi


# add the label to the print queue. if lpr exit code != 0, clean up and exit.
echo '----------------'
echo "Printing $id.pdf"
lpr -P DYMO_LabelWriter_4XL ./$id.pdf
if [[ $? -ne 0 ]]; then
	echo "ERROR: $file could not be put in print queue. Removing file. Fix errors and re-run script."
	clean_up
	exit 1
fi

# do NOT update shipment status in the database!
# doing so might cause things to get out of sync, depending on when this happens relative to marking the shipment BOXED
#echo "Updating shipment_id $id in the order database"
#curl -X PUT $url/shipments/$id -H "$headers" -H 'Content-Type: application/json' -d '{"shipment": {"shipment_status": "label_printed"}}' > /dev/null 2>&1

clean_up
echo "Return label for shipment $id sent to print ✅"
exit 0
