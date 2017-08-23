#!/bin/bash
# 
# The Public Radio - Raspberry Py installation script
# NOTE: MUST BE RUN AS ROOT
#

# Start by generating a SSH key pair by:
# $ ssh-keygen
# (use the default location, no passphrase)

# Authenticate the SSH key you created into GitHub
# For this, go to https://github.com/The-Public-Radio/ops_tools/settings/keys and paste the contents of ~/.ssh/id_rsa.pub

# start ssh-agent, add your ssh key to it
eval "$(ssh-agent -s)"
ssh-add /home/pi/.ssh/id_rsa


# update apt-get
apt-get update
apt-get -y upgrade

# install apt-get packages
apt-get -y install cups
apt-get -y install libcups2-dev
apt-get -y install libcupsimage2-dev
apt-get -y install ImageMagick
apt-get -y install msttcorefonts
apt-get -y install qrencode
apt-get -y install barcode
apt-get -y install gcc-avr
apt-get -y install binutils-avr
apt-get -y install gdb-avr
apt-get -y install avr-libc
apt-get -y install avrdude

# install pip packages
pip install intelhex
pip install crcmod
pip install RPi.GPIO

# Clone ops_tools
git clone git@github.com:The-Public-Radio/ops_tools.git /home/pi/ops_tools
mkdir /home/pi/ops_tools/temp

# Clone fm_transmitter
git clone git@github.com:markondej/fm_transmitter.git /home/pi/fm_transmitter