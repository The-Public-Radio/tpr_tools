#!/bin/bash
# 
# Print labels for shipments
# Usage:
# ./print_labels.sh <dir>
# 
# <dir>       tmp dir for label pdfs, defaults: ./
# <env>				environment to download labels for [staging, production]


# Helper functions
script_help() {
	cat <<- EOM
Usage:
./print_labels.sh <env> <dir> 

Options:
----------------
<dir>       tmp dir for label pdfs, defaults: ./
<env>       environment to download labels for [staging, production]
----------------
EOM
exit
}

# Set some base variables

# Check ARGV and send HELP!
if [[ $1 == "--help" || "$#" -lt 1 ]];
  then script_help;
fi

# Check dir
if [[ -z $2 ]]; then 
	dir='./tmp';
else
	dir=$2
fi

# Check env
if [[ $1 == 'production' ]]; then 
	url='api.thepublicrad.io/shipments';
elif [[ $1 == 'staging' ]]; then
	url='api-staging.thepublicrad.io/shipments?shipment_status=label_created';
else
	script_help
fi

# Make temp dir
mkdir ./tmp


# Pull down all label_created shipments
curl $url | jq -c '[.data[] | {id: .id, label_data: .label_data}][]' | while read i; do
	label_data=$(echo -n $i | jq -ja '.label_data')
	id=$(echo -n $i | jq '.id')

	echo -n $label_data | base64 -d > ./tmp/$id.pdf
done

# Print each label
for file in $dir/*.pdf; do
	echo "Printing $file"
	lpr -P DYMO_LabelWriter_4XL $file
done 

# Sleep before starting print loop check
echo 'Sleeping before updating status'
sleep 10

# Check print queue in loop, deleting images that are not present in queue 
# (already printed) and updating coordinator with status label_printed

# While there are files in the directory....
while [ $(ls $dir | wc -l) -gt 0 ]; do
	echo "Starting check for files in $dir"
	for file in $dir/*.pdf; do
		echo "Checking print queue for $file"
		# check to see if the file is in the queue
		in_queue=$(lpq -P DYMO_LabelWriter_4XL | grep $file | wc -l)
		if [[ in_queue -gt 0 ]]; then
			echo "$file is still in print queue. Moving on."
		else
			echo "$file no longer in print queue."
			# if not in queue, assume it printed and update coordinator
			shipment_id=$(echo $file | cut -d'.' -f1)
			echo "Updating shipment_id $shipment_id"
			echo 'curl -X PUT api-staging.thepublicrad.io/shipments/$shipment_id -d '{"shipment": {"shipment_status": "label_printed"}}''
		fi
	done
	echo 'Sleeping before checking queue again'
	sleep 5
done

echo 'Labels printed ✅'
