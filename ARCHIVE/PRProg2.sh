#!/bin/bash

sudo avrdude -P usb -c usbtiny -p attiny25 -B 5 -b 9600 -e -U\ 
flash:w:TPR_firmwareATTINY25.hex -U eeprom:w:/home/pi/TPR_ops/temp/eeprom

#avrcommand="sudo avrdude -P usb -c usbtiny -p attiny25 -B 5 -b 9600 -e -U\ 
#flash:w:/home/pi/TPR_ops/tools/programmer/TPR_firmwareATTINY25.hex -U eeprom:w:/home/pi/TPR_ops/temp/eeprom"
#while true; do
#	$avrcommand; break;
#done
