import sys, os
import RPi.GPIO as GPIO
import time
import subprocess

# Semantic exit codes in this script:
# * Exit 1 due to file and/or argument errors
# * Exit 3 due to programming errors
# * Exit 0 if programming is successful


default_firmware = '/home/pi/ops_tools/data/3044a9415d9b2becb2ee44bd759a0c9f6be66109.hex'
default_eeprom = '/home/pi/ops_tools/temp/eeprom'



if len(sys.argv) == 3:
	#this means that three arguments were given: the command, the firmware, and the eeprom
	eeprom = sys.argv[1]
	firmware = sys.argv[2]
elif len(sys.argv) == 1:
	# this means that just one argument was given: the command
	# so set firmware and eeprom to defaults
	eeprom = default_eeprom
	firmware = default_firmware
else:
	# the user needs to specify either eeprom AND firmware, or accept the default values
	# if the user specified only one parameter, fail with exit 1
	# or if the user specified more than two parameters, fail with exit 1
	print('ERROR: Wrong number of arguments.\n')
	print('Usage: $ python program_radio.py (path_to_eeprom_file) (path_to_firmware_file)\n')
	exit(1)

# confirm which parameters you're using

print('\neeprom: '+eeprom)
print('firmware: '+firmware+'\n')

# now check to see that they're valid files
if not os.path.exists(eeprom):
	print('Specified eeprom file does not exist. You specified:')
	print(eeprom)
	print('Exiting.\n')
	exit(1)
elif not os.path.exists(firmware):
	print('Specified firmware file does not exist. You specified:')
	print(firmware)
	print('Exiting.\n')
	exit(1)


print('Setting up GPIO input...')
# turn off GPIO warnings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set pin 2 as input and enable internal pull up resistor. Button must be active low.
# See https://pinout.xyz/ for pinout 
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print('Waiting for button press...')
while True:
	print('.')
	input_state = GPIO.input(2)
	if input_state == True:
		time.sleep(0.01)
	else:
		break

print('\nProgramming...\n')

p = subprocess.Popen(['sudo', 'avrdude', '-P', 'usb', '-c', 'avrispmkii', '-p', 'attiny25', '-B', '5', '-b', '9600', '-U', 'flash:w:'+firmware, '-U', 'eeprom:w:'+eeprom], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#stdout, stderr = process.communicate()


try:
    # Filter stdout
    for line in iter(p.stdout.readline, ''):
        sys.stdout.flush()
        # Print status
        print(">>> " + line.rstrip())
        sys.stdout.flush()
except:
    sys.stdout.flush()

# Wait until process terminates
while p.poll() is None:
    # Process hasn't exited yet, let's wait some
    time.sleep(0.5)

# Get return code from process
avrdude_exit = p.returncode
print('avrdude exit code is ', avrdude_exit)




if avrdude_exit == 0:
	print('Programming successful!')
	exit(0)
else:
	print('Programming FAILED with exit code:')
	print(avrdude_exit)
	exit(3)




#while True:
#    #input_state = GPIO.input(2)
#    if input_state == False:
#    	print('\nProgramming...\n')
#    	#p = subprocess.Popen(['sudo', 'avrdude', '-P', 'usb', '-c', 'avrispmkii', '-p', 'attiny25', '-B', '5', '-b', '9600', '-U', 'flash:w:'+firmware, '-U', 'eeprom:w:'+eeprom], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#    	p = subprocess.Popen(['sudo', 'avrdude', '-P', 'usb', '-c', 'avrispmkii', '-p', 'attiny25', '-B', '5', '-b', '9600', '-U', 'flash:w:foo', '-U', 'eeprom:w:foo'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#		stdout, stderr = process.communicate()
#		#try:
#		#    # Filter stdout
#		#    for line in iter(p.stdout.readline, ''):
#		#        sys.stdout.flush()
#		#        # Print status
#		#        print(">>> " + line.rstrip())
#		#        sys.stdout.flush()
#		#except:
#		#    sys.stdout.flush()
#		#
#		## Wait until process terminates (without using p.wait())
#		#while p.poll() is None:
#		#    # Process hasn't exited yet, let's wait some
#		#    time.sleep(0.5)
#		
#		# Get return code from process
#		avrdude_exit = p.returncode
#		print(avrdude_exit)
#		
#
#    	#avrdude_exit = os.WEXITSTATUS('sudo avrdude -P usb -c avrispmkii -p attiny25 -B 5 -b 9600 -U \
#    	#	flash:w:'+firmware+ ' -U eeprom:w:'+eeprom)
#        if avrdude_exit == 0:
#        	print('Programming successful!')
#        	exit(0)
#        else:
#        	print('Programming FAILED with exit code:')
#        	print(avrdude_exit)
#        	exit(3)
