#!/bin/bash

# This script creates a label that's used for the outside of TPR's 
# shipping box.
#
# Usage: $ boxlabel.sh <frequency> <serial number>

# check number of arguments and give feedback if it's not 3
if [ "$#" -ne 1 ]; then
  echo "Wrong number of arguments!"
  echo "Usage: $ boxlabel.sh <frequency> <serial number>" >&2
  exit 1
fi


# create text image
convert -density 300 -pointsize 12 -font \
/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
-size 637.5x1200 -gravity North \
label:'\n\nYour Public Radio\nis tuned to\n'"$1"' MHz\n\n\nEnjoy :)\n\n\n--------------------' \
/home/pi/ops_tools/temp/text.png

# create QR code for serial number
qrencode -o /home/pi/ops_tools/temp/sn.png "$2"

# resize QR code
convert -resize 300% /home/pi/ops_tools/temp/sn.png /home/pi/ops_tools/temp/sn.png

# merge two images into one
convert /home/pi/ops_tools/temp/text.png /home/pi/ops_tools/temp/sn.png -gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png

# print the result
lpr /home/pi/ops_tools/temp/label.png

# delete all the temp files
rm /home/pi/ops_tools/temp/*
