# tools
Tools, scripts, etc
Created 2015.01.21 by Spencer Wright


## PROJECT DESCRIPTION
The Public Radio is a single channel, single speaker FM receiver. 
As a piece of hardware, it was intended to be as simple as possible. One midrange speaker mounted inside a simple enclosure, with a single switched knob which controls power and adjusts volume.


## CONTAINED HEREIN
A whole bunch of tools for assembling, programming, and debugging The Public Radio. 
* perso.py, a script for taking in personalization data and managing the eeprom image creation
* eeprom.py, a script for creating an eeprom image
* boxlabel.sh, a script for generating and printing a label that goes on the outside of The Public Radio's box
* install.sh, a shell script used to set up a Raspberry Pi for use as a Public Radio manufacturing station
* Compiled versions of The Public Radio's current firmware. Note, these are generated from source which is contained in https://github.com/The-Public-Radio/Firmware
* pc_setup.md, instructions for setting up a Windows PC to be used as a Public Radio manufacturing station

## NOTES
* Our tuning process currently works with https://github.com/markondej/fm_transmitter, which uses GPIO pin 4 on Raspberry Pi 2/3.

## CREDITS
This project was begun by Zach Dunham and Spencer Wright, but would not have been possible without the generous help of Andy Warner, Daniel Suo, Suz Hinton, Todd Bailey, Josh Levine, Jordan Husney, Gabe Ochoa, and others. Big ups.
In addition, early versions of the hardware and firmware was adapted directly from Nathan Seidle et al (Sparkfun).
