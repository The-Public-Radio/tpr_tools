#!/bin/bash

# This script creates a label that's used for the outside of TPR's 
# shipping box.
#
# Usage: $ boxlabel.sh <frequency> <serial number> <source>

# check number of arguments and give feedback if it's not 3
if [ "$#" -ne 3 ]; then
  echo "Wrong number of arguments!"
  echo "Usage: $ boxlabel.sh <frequency> <serial number> <source>" >&2
  exit 1
fi

# create QR code for serial number
qrencode -o /home/pi/ops_tools/temp/sn.png "$2"

# resize QR code
convert -resize 300% /home/pi/ops_tools/temp/sn.png /home/pi/ops_tools/temp/sn.png

customers=("KUER" "WMBR" "WBEZ" "WFAE" "uncommon_goods" \
	"LGA" "KERA" "KXT" "KOSU" "WMFE" "WNYC" "GPB" "WAMU")

# check to see if source is a known customer
match=0
for customer in "${customers}"; do
	echo "customer is $customer"
	echo "source is $3"
	if [[ $customer = "$3" ]]; then
		match=1
		break
	fi
done

echo "match is $match"

# if order_source is NOT a known customer
#if [ $3 != "KUER" ] && [ $3 != "WMBR" ] && [ $3 != "WBEZ" ] && [ $3 != "WFAE" ] && [ $3 != "uncommon_goods" ] && [ $3 != "LGA" ] && [ $3 != "KERA" ] && [ $3 != "KXT" ] && [ $3 != "KOSU" ] && [ $3 != "WMFE" ]; then
if ! [ match = 0 ]; then
	# create text image
	convert -density 300 -pointsize 12 -font \
	/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 637.5x1200 -gravity North \
	label:'\n\nYour Public Radio\nis tuned to\n'"$1"' MHz\n\n\nEnjoy :)\n\n\n--------------------' \
	/home/pi/ops_tools/temp/background.png
	# merge two images into one
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/temp/sn.png \
	-gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png
elif [ $3 = "uncommon_goods" ]; then
	# create text image
	convert -density 300 -pointsize 12 -font \
	/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 637.5x1200 -gravity North \
	label:'\n\n\nYour Public Radio\nis tuned to\n'"$1"' MHz\n\n\nEnjoy :)\n\n--------------------' \
	/home/pi/ops_tools/temp/background.png
	# merge with uncommon_goods logo
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/data/uncommongoods_logo.png \
	-gravity center -geometry +0-500 -composite /home/pi/ops_tools/temp/background.png
	# merge two images into one
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/temp/sn.png \
	-gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png
elif [ $3 = "LGA" ]; then
	# create text image
	convert -density 300 -pointsize 12 -font \
	/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 637.5x1200 -gravity North \
	label:'\n\n\n\nYour Public Radio\nis tuned to\n'"$1"' MHz\n\nEnjoy :)\n\n--------------------' \
	/home/pi/ops_tools/temp/background.png
	# merge with uncommon_goods logo
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/data/LGA_logo.png \
	-gravity center -geometry +0-525 -composite /home/pi/ops_tools/temp/background.png
	# merge two images into one
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/temp/sn.png \
	-gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png
elif [ $3 = "KOSU" ]; then
	# create text image
	convert -density 300 -pointsize 12 -font \
	/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
	-size 637.5x1200 -gravity North \
	label:'\n\n\n\nYour Public Radio\nis tuned to\n'"$1"' MHz\n\nEnjoy :)\n\n--------------------' \
	/home/pi/ops_tools/temp/background.png
	# merge with uncommon_goods logo
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/data/KOSU_logo.png \
	-gravity center -geometry +0-525 -composite /home/pi/ops_tools/temp/background.png
	# merge two images into one
	convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/temp/sn.png \
	-gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png


# else, i.e. if order_source IS a radio station
else
	bgname=/home/pi/ops_tools/data/label_$3.png
	convert $bgname /home/pi/ops_tools/temp/sn.png \
	-gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/label.png
fi

# print the result
lpr -P DYMO_LabelWriter_450_Turbo /home/pi/ops_tools/temp/label.png

# delete all the temp files
#rm -rf /home/pi/ops_tools/temp/*
