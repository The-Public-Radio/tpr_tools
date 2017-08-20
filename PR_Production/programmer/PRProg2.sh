#!/usr/bin/env bash

avrcommand="sudo avrdude -P usb -c usbtiny -p attiny45 -B 5 -b 9600 -e -U flash:w:TPR_firmwareATTINY45.hex -U eeprom:w:tempEEprom"
while true; do
	$avrcommand; break;
done
