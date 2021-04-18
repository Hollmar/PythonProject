"""
# Standard library imports
from json import load as load_json
from platform import system
import sys

# Third party imports
from serial import Serial
from serial.tools import list_ports
from serial.serialutil import SerialException

# Local application imports
from .nrf import nRF52840



if system() == "Windows":
    port_type = "COM[^1|*]"

elif system() == "Linux":
    port_type = "ttyACM*"


# Read configuration
with open('../config.json') as cf:
    config = ( load_json(cf) )["dongle"]

#--- Auto port recognition ---#
__SERIAL_PORTS = []
try:
    __SERIAL_PORTS.append( str(*list_ports.grep(port_type)).split(' ')[0] )

    if __SERIAL_PORTS == ['']:
        raise FileNotFoundError

except (TypeError, FileNotFoundError):
    sys.stderr.write("No serial device found\n")
    sys.exit(-1)


for port in __SERIAL_PORTS:
    try:
        # Serial configuration
        # -Data bits: 8
        # -Stop bits: 1
        # -Parity: None
        # -Flow control: None
        __serial_conn = Serial( port, baudrate = config["baudrate"], timeout = config["timeout"] )

    except SerialException:
        # Try next port
        continue

    else:
        # Working port found
        break

# nRF-Dongle setup
__serial_conn.write( b'factoryreset\n' )

nrf_dongle = nRF52840(__serial_conn)

nrf_dongle.configure_leader()

# Reset input buffer
#logging.debug( "Bytes in RX Buff " + str(ser.inWaiting()) )
#sleep( 0.001 )
__serial_conn.reset_input_buffer()
#logging.debug( "Bytes in RX Buff " + str(ser.inWaiting()) )

# Export the serial connection
__all__ = [
    "nrf_dongle"
] """
