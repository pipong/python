# Pi Pong Guide

## Raspberry Pi B+ Set Up Instruction

Install **Raspbian** onto the Raspberry Pi B+.  Once installed run the following commands in the terminal. Ensure you are connected to the internet when running these commands.  Be patient as some of the commands will take several minutes to execute.

*sudo apt-get update*  
*sudo apt-get install python-dev python-pip*  
*sudo pip install --upgrade distribute*  
*sudo pip install ipython*  

Install GPIO Library for using the GPIO pins.

*sudo pip install --upgrade RPi.GPIO*  

## Github Install

Run the following command at the terminal on the Raspberry Pi. (This has not been fully tested yet and command may be out of date)

*sudo apt-get install git*

## To Do Items

- Reverse the blue and white colors
- Turn off the screensaver to the Pi (or set to something very long)
    http://www.etcwiki.org/wiki/Disable_screensaver_and_screen_blanking_Raspberry_Pi
    Optional: Have pi come out of screen saver or blanking when button is pressed
- Add functions for the master reset button
- Determine wiring schematic for master reset button
- Font size should change depending on screen size
- Have program begin on start up
- Winner screen to display once game ends
