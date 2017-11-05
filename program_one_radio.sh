#!/bin/bash
# usage:
# $ program_one_radio.sh <freq>

sudo /home/pi/ops_tools/perso.py foo $1 US 

sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U flash:w:/home/pi/ops_tools/data/TPR_firmware.hex -U eeprom:w:/home/pi/ops_tools/temp/eeprom

sudo /home/pi/fm_transmitter/fm_transmitter -f $1 /home/pi/ops_tools/data/1KTest_3s.wav