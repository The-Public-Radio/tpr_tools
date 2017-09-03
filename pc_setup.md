# Setting up a new PC

The Public Radio's manufacturing process depends on having a working PC (Windows 10). Here's how to set this computer up.

## Create your user
Make one administrator account and one "operator" account. Neither should have a Microsoft account.

## Remove preinstalled apps
Log in as the administrator account. Open powershell as administrator and run:

  > Get-AppxPackage -AllUsers | Remove-AppxPackage
  
## Uninstall the crap that Windows won't remove automatically.
Go to Settings > System and uninstall the following:
* App Explorer
* Bubble Witch 3 Saga
* Candy Crush Soda Saga
* March of Empires: War of Lords
* McAfee LiveSafe
* McAfee WebAdvisor
* Microsoft Office 365
* Minecraft: Windows 10 Edition
Then click Start and get rid of anything else there.

## Turn off notifications & suggestions
* Go to Settings > System > Notifications & actions and turn off everything
* Go to Settings > Personalization > Start and turn off everything

## Install a few things
* Chrome
* Sublime Text 3
* Dymo Label
* Tulip player https://s3.amazonaws.com/download.tulip.co/releases/prod/win/Tulip%20Player%20Setup.exe
* Shipstation Connect

## Register software to our accounts
* Shipstation
* Tulip
