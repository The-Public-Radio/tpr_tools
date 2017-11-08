#!/bin/bash

# This script creates a packing list to be put inside the box.
#
# Usage: $ packinglist.sh <source> <order_no> <name> <address_1> <address_2> <zip> <city> <message> <radio_1> <radio_2> <radio_3>


# CONTAINS:
	#	FIELD			CHARS	NOTE
	#	----------------------------
	#	Name			32		[recipient, not buyer]
	#	Address 1		40
	#	Address 2		40
	#	City			40
	#	Zip				16
	#	Gift Message	140
	#	Order #			8
	#	UG address 		140 58th Street, Building B STE SAB, Brooklyn, NY 11220
	#	UG phone		+1.888.356.0056
	#	UG email		custom@uncommongoods.com
	#	UG logo
	#	UG Return Policy		Return Policy: Please contact Customer Service at +1.888­.398.­3542 or 
	#							help@uncommongoods.com for assistance. This item was custom­made for you and is non­ returnable.

# 


# check number of arguments and give feedback if it's not 11
if [ "$#" -ne 11 ]; then
  echo "Wrong number of arguments!"
  echo "Usage: $ packinglist.sh <order_source> <order_no> <name> <address_1> <address_2> <zip> <city> <message> <radio_1> <radio_2> <radio_3>" >&2
  exit 1
fi

order_source="$1"
order_no="$2"
name="$3"
address_1="$4"
address_2="$5"
zip="$6"
city="$7"
message="$8"
radio_1="$9"
radio_2="$10"
radio_3="$11"

# create order info
convert -density 300 -pointsize 18 -font /usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
-size 457.5x288 label:'$name\n$address_1\n$address_2\n$city\n$zip\n\n$order_no\n\n$message' /home/pi/ops_tools/temp/order_info.png

# create 
# create text image
#convert -density 300 -pointsize 10 -font \
#/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
#-size 637.5x1200 -gravity North \
#label:'' \
#/home/pi/ops_tools/temp/background.png
## merge two images into one
#convert /home/pi/ops_tools/temp/background.png /home/pi/ops_tools/temp/sn.png \
#-gravity center -geometry +0+300 -composite /home/pi/ops_tools/temp/packinglist.png

# print the result
#lpr -P DYMO_LabelWriter_450_Turbo /home/pi/ops_tools/temp/packinglist.png

# delete all the temp files
#srm -rf /home/pi/ops_tools/temp/*
