#!/bin/bash

i=0
while true
do
	echo $i
	sudo /home/pi/fm_transmitter/fm_transmitter -f 97.1 /home/pi/ops_tools/data/1KTest_1s.wav
	sleep 1
	i=$((i + 1))
done
