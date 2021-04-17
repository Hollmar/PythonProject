# primitives Testskript #
#from nrf.nrf import nRF52840, States
from time import sleep
from json import load as load_json
import serial

def start_joiner(_serial_conn) -> None:
    _serial_conn.write(b'ifconfig up\n')
    _serial_conn.write(b'joiner start J01NME\n')

def reset_device(_serial_conn) -> None:
    """ Takes all radios down and makes a hard reset """
    _serial_conn.write(b'thread stop\n')
    _serial_conn.write(b'ifconfig down\n')
    _serial_conn.write(b'factoryreset\n')

#fdc0:de7a:b5c0:0:0:ff:fe00:fc00      -> Leader Anycast Locator (ALOC)
#fdc0:de7a:b5c0:0:0:ff:fe00:c00       -> Routing Locator (RLOC)
#fe80:0:0:0:1cd6:87a9:cb9d:4b1d       -> Link-Local Address (LLA)
#fdc0:de7a:b5c0:0:6394:5a75:a1ad:e5a  -> Mesh-Local EID (ML-EID)

with open('../config.json') as cf:
    config = load_json(cf)

#port = input("Port: ")
ser = serial.Serial('COM4', baudrate = config["dongle"]["baudrate"], timeout = config["dongle"]["timeout"])

#nrf = nRF52840(ser)

ser.write(b'factoryreset\n')

ser.write(b'eui64\n')
sleep(0.5)

ans = ser.readlines()

print(ans[-3].decode('utf-8').strip('\n'))
input("Waiting...")

start_joiner(ser)

for i in range(5):
    print( ser.readlines() )
    sleep(0.5)

ser.write(b'thread start\n')

#nrf.check_state(States.STATE_CHILD)

ser.write(b'rloc16\n')
res = ser.readlines()
print( "RLOC16_"+str(res) )

ser.write(b'udp open\n')
ser.write(b'udp bind :: 1212\n')
print( ser.readlines() )

try:
    i = 1
    while True:
        ser.write( b'udp send ' + b'ff02::1' + b' ' + b'2121' + b' ' +  (i.to_bytes(1, byteorder='big')) + b'\n' )
        print( ser.readlines() )
        i = i + 1
        sleep(0.5)

except KeyboardInterrupt:
    reset_device(ser)

    #nrf.check_state(States.STATE_DISABLED)
