#!/bin/bash
#
# Print labels for shipments
# Usage:
# ./print_labels_from_source.sh <env> <auth_token> <order_source>
#
# <env>       environment to download labels for [staging, production]
# <auth_token>     tpr-coordinator auth token
# <order_source>          order source


# Helper functions
script_help() {
  cat <<- EOM
Usage:
./reprint_labels.sh <env> <auth_token> <order_source>

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

# Pull down all orders from the source you want
curl -s -H "$headers" $url/orders?order_source=$order_source | jq -c '[.data[] | {id: .id}][]' | while read i; do
  order_id=$(echo -n $i | jq '.id')
  echo "order_id $order_id is from that source"

  # find the shipments that correspond with this order. there may be multiple shipments per order, so read them in one by one
  curl -s -H "$headers" $url/shipments?order_id=$order_id | grep 'label_created' | jq -c '[.data[] | {id: .id, label_data: .label_data}][]' | while read i; do
    echo "Shipments parsed!"
    shipment_id=$(echo -n $i | jq '.id');
    # if there IS a shipment_id that has a label_created status
    if [ ! -z "shipment_id" ]; then
      # set up label_data and shipment variables
      echo "shipment_id $shipment_id needs to be printed";

      label_data=$(echo -n $i | jq -r '.label_data');
      # Store label in pdf file that's named for the shipment_id
      echo -n $label_data | base64 -d > ./$shipment_id.pdf;
      # Print label 
      lpr -P DYMO_LabelWriter_4XL ./$shipment_id.pdf;

      # then update it!
      curl -X PUT $url/shipments/$shipment_id -H "$headers" -H 'Content-Type: application/json' -d '{"shipment": {"shipment_status": "label_printed"}}' > /dev/null 2>&1;
    else
      echo "all shipments in order_id $order_id have been printed";
    fi
  done
done

clean_up
echo 'All new labels sent to print ✅'
exit 0
