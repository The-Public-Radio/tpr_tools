//Updated 4/8/15
//Credits
Zach Dunham, Spencer Wright, Andy Warner, Jonathan Dehan

Public Radio Maker Kit Firmware Install 
---------------------------------------

The maker kit software package includes these items

 * PR.hex    
 	Compiled firmware for the radio
 * eeprom.py 
 	A python script which generates a hex file for the radio's presets 
 * Maker.sh  
 	A script to execute eeprom.py with a user's desired presets 

 Overview
 --------------------------------------
 The Public Radio is programmed with firmware which takes its marching 
 orders from the mcu's eeprom fields (frequency preset, band, de-emphasis, etc).  This main firmware file is PR.hex.  The eeprom hex file which holds this preset information is created by running eeprom.py and specifying these values.  
 
 Then, a radio is ready to be flashed by calling:
 avrdude -qq -P usb -c usbtiny -p attiny45  -B 15 -e -U flash:w:pr.hex -U eeprom:w:my_eeprom.hex 

 To simplfy things a little bit, running Maker.sh takes user prompts and invokes eeprom.py, passing off the presets, and then creates the eeprom.hex and then calls avrdude to flash the radio.  

Installation
 --------------------------------------
*On a MAC follow these steps* 

Open terminal and run the following
1. sudo easy_install pip
2. sudo pip install intelHex
3. sudo pip install crcmod 
 (prompts install dev tools) accept
4. open a browser and go to http://www.obdev.at/products/crosspack/index.html
   download and install cross pack 
5. relaunch terminal 
6. Navigate to the MakrKit directory cd …/MaKrKT/
7. Attach your avrisp to the radio and connect the other end to your usb drive. 
8. Type ./Maker.sh in the terminal
9. Follow the steps in the prompts to enter your desired frequency

*On Windows follow these steps* 


*On Ubuntu follow these steps* 


 Links
 ---------------------------------------
 Python Download
 https://www.python.org/downloads/release/python-279/
 Avrdude Download
 http://download.savannah.gnu.org/releases/avrdude/
 

 License
 --------------------------------------





