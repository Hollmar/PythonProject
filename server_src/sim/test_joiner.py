# primitives Testskript #

# Standard library imports
from json import load as load_json
from platform import system

import sys
from time import sleep

# Third party imports
import serial
from os import getcwd


sys.path.append( getcwd() ) #< Bypass pythons useless import system
from nrf.nrf import nRF52840

# Load config
with open('../config.json') as cf:
    config = load_json(cf)

# Choose port
port = input("Port: ")

if system() == "Windows":
    port_type = "COM[^1|*]"

elif system() == "Linux":
    port_type = "/dev/ttyACM*"

# Init serial device and nrf dongle
ser = serial.Serial(port_type+port, baudrate = config["dongle"]["baudrate"], timeout = config["dongle"]["timeout"])

nrf = nRF52840(ser)

ser.write(b'factoryreset\n')

# Get eui64
ser.write(b'eui64\n')
sleep(0.5)

eui64 = ser.readlines()
eui64 = eui64[-3].decode('utf-8').strip('\n')

print( eui64 )

# wait till server is in pairing mode
input("Waiting...")

# Start joiner and print input buffer
nrf.start_joiner()

for i in range(5):
    print( ser.readlines() )
    sleep(0.5)

ser.write(b'thread start\n')

#nrf.check_state(States.STATE_CHILD)

ser.write(b'udp open\n')
ser.write(b'udp bind :: 1212\n')
print( ser.readlines() )

ser.write( bytes(eui64) + b'' )

# send deviceData
try:
    i = 1
    while True:
        ser.write( b'udp send ' + b'ff02::1' + b' ' + b'2121' + b' ' +  (i.to_bytes(1, byteorder='big')) + b'\n' )
        print( ser.readlines() )
        i = i + 1
        sleep(0.5)

except KeyboardInterrupt:
    nrf.reset_device()
