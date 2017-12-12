#!/bin/bash
# usage:
# $ program_one_radio.sh <freq> <production>

sudo /home/pi/ops_tools/perso.py foo $1 US 

sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U flash:w:/home/pi/ops_tools/data/3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex -U eeprom:w:/home/pi/ops_tools/temp/eeprom

sudo /home/pi/fm_transmitter/fm_transmitter -f $1 /home/pi/ops_tools/data/1KTest_1s.wav

if [[ -z "$2" ]] && [[ $2 = "production" ]]; then
	echo 'Removing parts from inventory...'
	sudo python /home/pi/ops_tools/inventory_event.py fulfill
else
	echo 'NOT IN PRODUCTION. Parts may still be in inventory.'
fi