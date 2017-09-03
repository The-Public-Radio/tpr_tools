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



# Once you've done everything above, run:
#	$ sudo ./install.sh
# and everything should set itself up!

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

# Set up CUPS for your Dymo 4XL and 450 Turbo
# make user 'pi' a CUPS admin
usermod -a -G lpadmin pi
# make sure remote users can make changes to CUPS
cat > /etc/cups/cupsd.conf <<- EOM
# foo
#
# Sample configuration file for the CUPS scheduler.  See "man cupsd.conf" for a
# complete description of this file.
#

# Log general information in error_log - change "warn" to "debug"
# for troubleshooting...
LogLevel warn

# Deactivate CUPS' internal logrotating, as we provide a better one, especially
# LogLevel debug2 gets usable now
MaxLogSize 0

# Only listen for connections from the local machine.
# Listen localhost:631
Port 631

# Show shared printers on the local network.
Browsing On
BrowseLocalProtocols dnssd

# Default authentication type, when authentication is required...
DefaultAuthType Basic

# Web interface setting...
WebInterface Yes

# Restrict access to the server...
<Location />
  Order allow,deny
  Allow @local
</Location>

# Restrict access to the admin pages...
<Location /admin>
  Order allow,deny
  Allow @local
</Location>

# Restrict access to configuration files...
<Location /admin/conf>
 Order allow,deny
 Allow @local
</Location>

# Set the default printer/job policies...
<Policy default>
  # Job/subscription privacy...
  JobPrivateAccess default
  JobPrivateValues default
  SubscriptionPrivateAccess default
  SubscriptionPrivateValues default

  # Job-related operations must be done by the owner or an administrator...
  <Limit Create-Job Print-Job Print-URI Validate-Job>
    Order deny,allow
  </Limit>

  <Limit Send-Document Send-URI Hold-Job Release-Job Restart-Job Purge-Jobs Set-Job-Attributes Create-Job-Subscription Renew-Subscription Cancel-Subscription Get-Notifications Reprocess-Job Cancel-Current-Job Suspend-Current-Job Resume-Job Cancel-My-Jobs Close-Job CUPS-Move-Job CUPS-Get-Document>
    Require user @OWNER @SYSTEM
    Order deny,allow
  </Limit>

  # All administration operations require an administrator to authenticate...
  <Limit CUPS-Add-Modify-Printer CUPS-Delete-Printer CUPS-Add-Modify-Class CUPS-Delete-Class CUPS-Set-Default CUPS-Get-Devices>
    AuthType Default
    Require user @SYSTEM
    Order deny,allow
  </Limit>

  # All printer operations require a printer operator to authenticate...
  <Limit Pause-Printer Resume-Printer Enable-Printer Disable-Printer Pause-Printer-After-Current-Job Hold-New-Jobs Release-Held-New-Jobs Deactivate-Printer Activate-Printer Restart-Printer Shutdown-Printer Startup-Printer Promote-Job Schedule-Job-After Cancel-Jobs CUPS-Accept-Jobs CUPS-Reject-Jobs>
    AuthType Default
    Require user @SYSTEM
    Order deny,allow
  </Limit>

  # Only the owner or an administrator can cancel or authenticate a job...
  <Limit Cancel-Job CUPS-Authenticate-Job>
    Require user @OWNER @SYSTEM
    Order deny,allow
  </Limit>

  <Limit All>
    Order deny,allow
  </Limit>
</Policy>

# Set the authenticated printer/job policies...
<Policy authenticated>
  # Job/subscription privacy...
  JobPrivateAccess default
  JobPrivateValues default
  SubscriptionPrivateAccess default
  SubscriptionPrivateValues default

  # Job-related operations must be done by the owner or an administrator...
  <Limit Create-Job Print-Job Print-URI Validate-Job>
    AuthType Default
    Order deny,allow
  </Limit>

  <Limit Send-Document Send-URI Hold-Job Release-Job Restart-Job Purge-Jobs Set-Job-Attributes Create-Job-Subscription Renew-Subscription Cancel-Subscription Get-Notifications Reprocess-Job Cancel-Current-Job Suspend-Current-Job Resume-Job Cancel-My-Jobs Close-Job CUPS-Move-Job CUPS-Get-Document>
    AuthType Default
    Require user @OWNER @SYSTEM
    Order deny,allow
  </Limit>

  # All administration operations require an administrator to authenticate...
  <Limit CUPS-Add-Modify-Printer CUPS-Delete-Printer CUPS-Add-Modify-Class CUPS-Delete-Class CUPS-Set-Default>
    AuthType Default
    Require user @SYSTEM
    Order deny,allow
  </Limit>

  # All printer operations require a printer operator to authenticate...
  <Limit Pause-Printer Resume-Printer Enable-Printer Disable-Printer Pause-Printer-After-Current-Job Hold-New-Jobs Release-Held-New-Jobs Deactivate-Printer Activate-Printer Restart-Printer Shutdown-Printer Startup-Printer Promote-Job Schedule-Job-After Cancel-Jobs CUPS-Accept-Jobs CUPS-Reject-Jobs>
    AuthType Default
    Require user @SYSTEM
    Order deny,allow
  </Limit>

  # Only the owner or an administrator can cancel or authenticate a job...
  <Limit Cancel-Job CUPS-Authenticate-Job>
    AuthType Default
    Require user @OWNER @SYSTEM
    Order deny,allow
  </Limit>

  <Limit All>
    Order deny,allow
  </Limit>
</Policy>

#
#
EOM

# restart CUPS
/etc/init.d/cups restart

# extract the DYMO driver tarball that's inside ops_tools
tar -xvf /home/pi/ops_tools/dymo-cups-drivers-1.4.0.tar.gz -C /home/pi/ops_tools/temp

# change directories
cd /home/pi/ops_tools/temp/dymo-cups-drivers-1.4.0.5
./configure
make
make install

# Now open a web browser and log onto the pi's CUPS server using port 631. 
# Add the relevant DYMO printers and confirm that they work by printing test pages.