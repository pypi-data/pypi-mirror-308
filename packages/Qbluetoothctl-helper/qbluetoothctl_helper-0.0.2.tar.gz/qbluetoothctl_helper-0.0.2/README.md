# Qbluetoothctl Helper

Python Qt interface to the linux **bluetoothctl** program.

This class provides methods to perform 
  - pairing / removing
  - connecting / disconnecting 
  - scanning
  - trusting / distrusting
  - getting device info
  - finding device by name or mac

Many of these methods are not available in other bluetooth libraries.

## Install
Download the library and ```pip3 install -e .``` or omit the -e switch to install into python's site packages.

## Testing
The main file ```Qbluetoothctl_helper.py``` can be run and will conduct a couple of test.
User will need to update them to fit their device and test needs.

## Dependencies
- PyQt 5
- PyQt 6 untested

