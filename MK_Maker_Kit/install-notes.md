# How to flash your Public Radio
Oh hi! You're possibly entering the exciting world of hex compilation and firmware flashing for the very first time. If this is the case - welcome! If you're experienced with this stuff, you can skip ahead to the [installation instructions](#installation) for your operating system choice. 


## Installation
We currently support the major operating systems. Find your operating system below to get started.

+ [OSX instructions](#osx)
+ [Windows instructions](#windows)
+ [Linux instructions](#linux)

### OSX

So you're running on a Mac. Nice! We'll need a couple of tools to get started. This will help you compile your custom firmware and get it flashed onto your radio. Follow the steps below to get all set up.

1. Download and install [Crosspack](https://www.obdev.at/products/crosspack/index.html). 
2. Download our Public Radio Maker Kit app, and double click on it to start 'er up.
3. You're installed! Skip to the [next section](#using-the-public-radio-software) to learn which values to type in for successful flashing of your radio.

### Windows

To get this all going on windows, we need some cool software that communicates with the radio called **avrdude**. You can get this by downloading and installing **WinAVR**. Let's get started!

1. Download and install [WinAVR](http://sourceforge.net/projects/winavr/files/WinAVR/20100110/).
2. If you haven't already, install the drivers for your programmer device. You should have received an installation CD with the programmer. If not, you can probably get it set up by using a port of `libusb`. [The steps are well written up here](http://eliaselectronics.com/using-the-avrispmkii-with-avrdude-on-windows/).
3. Download our Public Radio Maker Kit software, and double click on the exe file.
5. You're installed! Skip to the [next section](#using-the-public-radio-software) to learn which values to type in for successful flashing of your radio.

### Linux

If you're running a flavour of Linux, you're probably already familar with using the Terminal. If not, you can find the Terminal application already installed on all Linux distros. Fire it up!

1. Install python-tk by running: `sudo apt-get install python-tk`
2. Next, we need to install avrdude, if you don't already have it. The following commands will install the latest verison for you:
`sudo add-apt-repository ppa:pmjdebruijn/avrdude-release`  
`sudo apt-get update`  
`sudo apt-get install avrdude`  
3. Download our Public Radio Maker Kit app
4. You'll need to run our app with admin privileges. The most straightforward way of doing this is to use Terminal to [cd](http://www.linfo.org/cd.html) to the directory where the app is, and run `sudo Maker`
5. You're installed! Skip to the [next section](#using-the-public-radio-software) to learn which values to type in for successful flashing of your radio.

## Using the Public Radio software

When you start up our application, you should see a window that resembles this:

![screenshot of public radio user interface](https://dl.dropboxusercontent.com/u/16732310/public-radio.png)

You may be able to already tell that there are two text boxes that need some info from you.

The first is labeled 'Radio Frequency'. Pretty self explanatory. This is where you'll need to enter which radio station you'd like to tune your radio to. Remember, **this needs to be a number between 87 and 108**. For example, if you're in NYC, WNYC station is 93.9

The second text box, 'Programmer', is asking you which programmer you're using to flash the radio's firmware. This is the fancy little box device that you have plugged into your computer's usb port at one end, and the radio at the other end. To know the 'codename' for your programmer to type in, [check this helpful and extensive list here](http://www.nongnu.org/avrdude/user-manual/avrdude_12.html)! As a common example, the AVR ISP MkII should be entered as simply `avrispmkii` in the text box.

The steps to programming your radio are:

1. Make sure the radio and programmer are hooked up correctly and plugged in via USB. You can double check [this section](#how-to-hook-up-your-public-radio-and-the-programmer) if you're unsure on how to do this.
2. Turn on the radio.
3. Enter the radio frequency and programmer codename of choice into the two text boxes.
4. Take a deep breath, and click 'Flash my Radio'.
5. Pause for a few seconds to let the hardware do its thing. If all went well, you should see a success message pop up at the bottom of the Public Radio software. Your radio will also start playing your station! If not, not to worry, check the [troubleshooting section](#troubleshooting) below.

## How to hook up your Public Radio and the programmer 

todo


## Troubleshooting

**I'm seeing the error `avrdude: error: could not find USB device [...]`**

1. Check that your programmer is plugged in correctly at both ends, and that the ISP header is not plugged into the Radio board backwards. Most programmers will have a red light if it's backwards, and a green light if it's correct.
2. Ensure that you typed in the correct programmer codename in the second text box within the Public Radio app.
3. Make sure your radio is turned on.

**I'm seeing the error `avrdude: error: ser_open(): can't open device "USB": File not found`**

1. Is your radio turned on? If not, switch it on and try again.
2. You may see this on Windows if the driver for your programmer is not correctly installed/being found. Try reinstalling the driver, or try again after locating an alternate driver source.

**I'm seeing a long, long error about `Operation not permitted`, halp!**

1. My hunch is that you're running this on Linux, and the software does not have the right privileges to communicate over USB with the programmer. Try running the app prefixed with the `sudo` command.
2. As always, make sure your radio is turned on.
