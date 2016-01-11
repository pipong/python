# Pi Pong Guide
========================

## Raspberry Pi B+ Set Up Instruction

Install **Raspbian** onto the Raspberry Pi B+.  Once installed run the following commands in the terminal.

*sudo apt-get update*  
*sudo apt-get install python-dev python-pip*  
*sudo pip install --upgrade distribute*  
*sudo pip install ipython*  

Install GPIO Library for using the GPIO pins.

*sudo pip install --upgrade RPi.GPIO*  

Connect the buttons to the 3.3V supply source to a 330 Ohm resistor.  Split this to two individual momentary switches.  One switch to be connect to the GPIO pin position **4** and the other **18**.
