# VUCTF-2024-Badge
This repository contains both the intended and final hardware challenge badge for the 2024 VU CTF. The challenge was built on the Waveshare RP2040 MCU board (https://www.waveshare.com/rp2040-lcd-1.28.htm)

## Installation
To install the challenge, hold the boot button on the Waveshare device while plugging it in, this should open up a new removable storage device on your computer.
From here simply drag and drop the MicroPython uf2 file into it, the device should automatically disconnect and reboot once this is completed.

Once MicroPython is installed, you can use a GUI like Thonny to upload the files onto the device. Make sure to maintain the folder structure (files in `lib` are in a folder called `lib` on the device after importing).

Once this is complete, the hardware challenge is set up. Simply disconnect and reconnect the device to get started!

## Source
#### Intended
These are all the files to install the challenge as it was origionally intended, during the CTF itself we encountered issues with the screen and decided to modify the challenge to be fully over serial. Special thanks to Martin Meyers for later identifying the issue and providing a fix.

#### Final
These are all the files needed to install the challenge as it was presented during the VU 2024 CTF. 

## References
- https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-the-waveshare-rp2040-1-28-round-touch-lcd
- https://www.waveshare.com/wiki/RP2040-LCD-1.28