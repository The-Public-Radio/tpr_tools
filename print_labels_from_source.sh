#!/bin/bash
#
# Print labels for shipments
# Usage:
# ./reprint_labels.sh <env> <auth_token> <order_source>
#
# <env>       environment to download labels for [staging, production]
# <auth_token>     tpr-coordinator auth token
# <order_source>          order source


# Helper functions
script_help() {
  cat <<- EOM
Usage:
./reprint_labels.sh <env> <auth_token>

Options:
----------------
<env>         environment to download labels for [staging, production]
<auth_token>  API key
<order_source>      order source
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

auth_token="$2";
order_source="$3";

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

# Make temp tmp_dir
basename="$(dirname $0)"
tmp_dir="$basename/temp"

# make the temp directory. -p forces no error if temp directory already exists.
mkdir -p $tmp_dir

# move to the temp directory
cd $tmp_dir
# remove any files that may be there already
clean_up

# Pull down all label_printed, but not yet boxed shipments
curl -s -H "$headers" $url/orders?order_source=$order_source | jq -c '[.data[] | {id: .id}][]' | while read i; do
  id=$(echo -n $i | jq '.id')
  # put the label data in a pdf in $tmp_dir
  r=$(curl -s -H "$headers" $url/shipments?order_id=$id | jq -c '[.data[] | {id: .id, label_data: .label_data}][]')
  label_data=$(echo -n $r | jq -r '.label_data')
  shipment_id=$(echo -n $r | jq '.id')
  # Store label in pdf file
  echo -n $label_data | base64 -d > $id.pdf
  # Print label 
  lpr -P DYMO_LabelWriter_4XL $id.pdf
  # Update coordinator
  if [ -z "$shipment_id" ]; then
    echo "Shipment ID empty. Exiting to not set all shipments as printed";
    exit;
  else
    curl -X PUT $url/shipments/$shipment_id -H "$headers" -H 'Content-Type: application/json' -d '{"shipment": {"shipment_status": "label_printed"}}' > /dev/null 2>&1;
  fi
done

# if [[ $(ls $tmp_dir/ | wc -l) == 0  ]]; then
#   echo "No labels to print!"
#   clean_up
#   exit
# fi

# Print each label
# for file in $tmp_dir/*.pdf; do
#   echo '----------------'
#   echo "Printing $file"
  
#   if [[ $? -ne 0 ]]; then
#     echo "ERROR: $file could not be put in print queue. Removing file. Fix errors and re-run script."
#     echo "Cancelling process!"
#     clean_up
#     exit 1
#   fi
#   echo "Updating shipment_id $id in the order database"

# ###############################################################
# #######################  WARNING    ###########################
# # THE COMMENTED-OUT LINE BELOW IS NOT SAFE TO RUN


#  curl -X PUT $url/shipments/$id -H "$headers" -H 'Content-Type: application/json' -d '{"shipment": {"shipment_status": "label_printed"}}' > /dev/null 2>&1
# done

# don't do any queue checking; it's not worth it.
clean_up
echo 'All new labels sent to print ✅'
exit 0
