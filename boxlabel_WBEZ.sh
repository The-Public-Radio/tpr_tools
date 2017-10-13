#!/bin/bash

# This script creates a label that's used for the outside of TPR's 
# shipping box.
#
# Usage: $ boxlabel_WBEZ.sh <frequency> <serial number>

# check number of arguments and give feedback if it's not 2
if [ "$#" -ne 1 ]; then
  echo "Wrong number of arguments!"
  echo "Usage: $ boxlabel_WBEZ.sh <serial number>" >&2
  exit 1
fi

# create QR code for serial number
qrencode -o /home/pi/ops_tools/temp/sn.png "$1"

# resize QR code
convert -resize 300% /home/pi/ops_tools/temp/sn.png /home/pi/ops_tools/temp/sn.png

# merge two images into one
convert /home/pi/ops_tools/data/WBEZ_label.png /home/pi/ops_tools/temp/sn.png -gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png

# print the result
lpr -P DYMO_LabelWriter_450_Turbo /home/pi/ops_tools/temp/label.png

# delete all the temp files
rm -rf /home/pi/ops_tools/temp/*
