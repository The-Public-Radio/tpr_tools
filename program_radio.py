import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Pin that our button is connected to. I think that GPIO 2 is open, currently
# Set this pin as input and enable internal pull up resistor. Our button is active low.  
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(2)
    if input_state == False:
        sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U flash:w:/home/pi/ops_tools/data/3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex -U eeprom:w:/home/pi/ops_tools/temp/eeprom
        # debounce button 
        time.sleep(0.5) 
        exit()