#!/bin/bash
# 
# Print labels for shipments
# Usage:
# ./print_labels.sh <tmp_dir>
# 
# <tmp_dir>       tmp directory for label pdfs, defaults: ./
# <env>				environment to download labels for [staging, production]


# Helper functions
script_help() {
	cat <<- EOM
Usage:
./print_labels.sh <env> <tmp_dir> 

Options:
----------------
<tmp_dir>   temp directory for label pdfs, defaults: ./
<env>       environment to download labels for [staging, production]
----------------
EOM
exit
}

clean_up() {
	rmdir $tmp_dir
}

# Set some base variables

# Check ARGV and send HELP!
if [[ $1 == "--help" || "$#" -lt 1 ]];
  then script_help;
fi

# Check tmp_dir
if [[ -z $2 ]]; then 
	tmp_dir='./tmp';
else
	tmp_dir=$2
fi

# Check env
if [[ $1 == 'production' ]]; then 
	url='api.thepublicrad.io';
elif [[ $1 == 'staging' ]]; then
	url='api-staging.thepublicrad.io';
else
	script_help
fi

# Make temp tmp_dir
mkdir ./tmp

# Pull down all label_created shipments
curl -s $url/shipments?shipment_status=label_created | jq -c '[.data[] | {id: .id, label_data: .label_data}][]' | while read i; do
	label_data=$(echo -n $i | jq -ra '.label_data' | tr -d '\n')
	id=$(echo -n $i | jq '.id')

	echo -n $label_data | base64 -d > ./tmp/$id.pdf
done

if [[ $(ls $tmp_dir/ | wc -l) == 0  ]]; then
	echo "No labels to print!"
	clean_up
	exit
fi

# Print each label
for file in $tmp_dir/*.pdf; do
	echo '----------------'
	echo "Printing $file"
	lpr -P DYMO_LabelWriter_4XL $file
	if [[ $? -ne 0 ]]; then
		echo "ERROR: $file could not be put in print queue. Removing file. Fix errors and re-run script."
		rm $file
	fi
done 

# Sleep before starting print loop check
echo 'Sleeping before updating status'
sleep 1

# Check print queue in loop, deleting images that are not present in queue 
# (already printed) and updating coordinator with status label_printed

# While there are files in the directory....
while [ $(ls $tmp_dir | wc -l) -gt 0 ]; do
	echo "Starting check for files in $tmp_dir"
	for file in $tmp_dir/*.pdf; do
		echo '----------------'
		file_name=$(echo $file | sed 's/.*\///')
		echo "Checking print queue for $file_name"
		# check to see if the file is in the queue
		in_queue=$(lpq -P DYMO_LabelWriter_4XL | grep $file_name | wc -l)
		if [[ in_queue -gt 0 ]]; then
			echo "$file_name is still in print queue. Moving on."
		else
			echo "$file_name no longer in print queue."
			# if not in queue, assume it printed and update coordinator
			shipment_id=$(echo $file_name | cut -d. -f1)
			echo "Updating shipment_id $shipment_id"
			curl -X PUT $url/shipments/$shipment_id -H 'Content-Type: application/json' -d '{"shipment": {"shipment_status": "label_printed"}}' > /dev/null 2>&1
			if [[ $? -ne 0 ]]; then
				echo "Error updating shipment $shipment_id status!"
			fi
			# delete file
			rm $file
		fi
	done
	echo 'Sleeping before checking queue again'
	sleep 5
done

clean_up
echo 'All new labels printed ✅'
