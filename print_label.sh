#!/bin/bash
#
# Print labels for shipments
# Usage:
# ./print_label.sh <env> <auth_token>
#
# <env>				environment to download labels for [staging, production]
# <auth_token>     tpr-coordinator auth token


# Helper functions
script_help() {
	cat <<- EOM
Usage:
./print_labels.sh <env> <auth_token>

Options:
----------------
<env>            environment to download labels for [staging, production]
<auth_token>     tpr-coordinator auth token
----------------
EOM
exit
}

clean_up() {
	rm -rf $tmp_dir
}

# Set some base variables

# Check ARGV and send HELP!
if [[ $1 == "--help" || "$#" -lt 1 ]];
  then script_help;
fi

auth_token="$2";

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

# Pull down the next label_created shipment
# if the result you get isn't "null," then save the id and label_data parameters and dump the label data into a pdf.
# otherwise, there are no orders to print! so clean up and exit.
curl -s -H "$headers" $url/next_shipment_to_print | jq -c '[.data | {id: .id, label_data: .label_data}][]' | while read i; do
	label_data=$(echo -n $i | jq -r '.label_data' | tr -d '\n')
	id=$(echo -n $i | jq '.id')
	if [ $id != null ]
		echo "Downloaded shipment $id!"
		then echo -n $label_data | base64 --decode > $id.pdf
	else 
		echo "No labels in the database!"
		clean_up
		exit
	fi
done

# add the label to the print queue. if lpr exit code != 0, clean up and exit.
echo '----------------'
echo "Printing $id.pdf"
lpr -P DYMO_LabelWriter_4XL $id.pdf
if [[ $? -ne 0 ]]; then
	echo "ERROR: $file could not be put in print queue. Removing file. Fix errors and re-run script."
	clean_up
	exit
fi

# Sleep before starting print loop check
echo 'Sleeping before updating status'
sleep 1

# Check print queue in loop, deleting images that are not present in queue
# (already printed) and updating coordinator with status label_printed

# While the label's pdf still exists....
while [ -e id.pdf ]; do
	echo "Checking print queue for $id.pdf"
	in_queue=$(lpq -P DYMO_LabelWriter_4XL | grep $id.pdf | wc -l)
	if [[ in_queue -gt 0 ]]; then
		echo "$id.pdf is still in print queue."
	else
		echo "$id.pdf no longer in print queue."
		# if not in queue, assume it printed and update coordinator
		echo "Updating shipment_id $id in the order database"
		curl -X PUT $url/shipments/$shipment_id -H "$headers" -H 'Content-Type: application/json' -d '{"shipment": {"shipment_status": "label_printed"}}' > /dev/null 2>&1
		if [[ $? -ne 0 ]]; then
			echo "Error updating shipment_id $id status!"
		fi
	fi
	echo 'Sleeping before checking queue again'
	sleep 5
done

clean_up
echo 'All new labels printed ✅'
