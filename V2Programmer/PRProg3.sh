#!/usr/bin/env bash
FREQ=$1
pifmcommand="sudo ./pifm 1KTest.wav $FREQ 44100"
while true; do
	$pifmcommand; break;
done
