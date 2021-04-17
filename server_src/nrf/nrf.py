# Standard library imports
import logging
from re import search
from time import sleep

# Local application imports
from .msg import ERROR_MSG, SUCCESS_MSG
from .buffer_cache import Cache
from .udp import Udp


class nRF52840:
    """ Provides methods for serial communication with a nRF52480 Dongle """
    def __init__(self, ser: object):
        self.__PSKD = b'J01NME' # Pre-shared-key for network joining
        self._serial_conn = ser # FIXME Make private
        self.__udp = Udp(b'ff03::1', b'1212', b'2121')
        self.__cache = Cache()

    ####################################
    # Methods for startup and shutdown #
    ####################################
    def configure_leader(self) -> None:
        """ Configure and start the nRF-Dongle as Leader """
        self._serial_conn.write(b'dataset init new\n')
        self._serial_conn.write(b'dataset commit active\n')
        self._serial_conn.write(b'ifconfig up\n')
        self._serial_conn.write(b'thread start\n')

    def reset_device(self) -> None:
        """ Takes all radios down and makes a hard reset """
        self._serial_conn.write(b'thread stop\n')
        self._serial_conn.write(b'ifconfig down\n')
        self._serial_conn.write(b'factoryreset\n')

    ##############################
    # Methods for adding devices #
    ##############################
    def start_commissioner(self) -> None:
        """ Starts the commissioner """
        self._serial_conn.write(b'commissioner start\n')

    def add_device(self, eui64: bytes) -> None:
        """ Commissioner tries to join a device with the given eui64 """
        self._serial_conn.write(b'commissioner joiner add ' + eui64 + b' ' + self.__PSKD + b'\n')

    # NOTE Only for testing purposes - delete in final version
    def start_joiner(self) -> None:
        self._serial_conn.write(b'ifconfig up\n')
        self._serial_conn.write(b'joiner start ' + self.__PSKD + b'\n')

    ########################################
    # Methods for reading/searching buffer #
    ########################################
    def read_buffer(self, save_buffer: bool = False) -> list:
        """ Read the input buffer """
        buffer = None
        buffer = self._serial_conn.readlines()

        logging.debug( 'BUF_RD_' + str(buffer) + ' ' + str(save_buffer) )

        if save_buffer and buffer:
            for data in buffer:
                # x bytes from <address> / deviceSetupInfo <eui64;Type;ipv6>
                if search( b'bytes', data ) or search( b'deviceSetupInfo', data):
                    self.__cache.write_cache( data )
                    logging.info( 'Buffer saved ' + str(self.__cache.get_cache()) )

        return buffer

    def check_state(self, expected_state: bytes, save_buffer: bool = False) -> bytes:
        """ Check if nRF52480 Dongle is in the expected state """
        res = b""
        timeout_cnt = 10
        found = None

        while not found:
            self._serial_conn.write(b'state\n')

            buffer = self.read_buffer(save_buffer)

            for data in buffer:
                found = search(expected_state, data)
                if found:
                    res = SUCCESS_MSG
                    break

            logging.debug("STATE_"+str(buffer)+" "+str(found)+" "+str(timeout_cnt))

            timeout_cnt -= 1
            if timeout_cnt == 0:
                res = ERROR_MSG
                break

            sleep(0.01)

        return res

    ######################################
    # Wrapper methods for UDP-connection #
    ######################################
    def udp_open(self) -> None:
        """ Open UDP-port """
        self.__udp.open( self._serial_conn )

    def udp_send(self, message: bytes) -> None:
        """ Send given message via UDP as broadcast """
        self.__udp.send_broadcast( self._serial_conn, message)

    def udp_bind(self) -> None:
        """ Bind udp port """
        self.__udp.bind( self._serial_conn )

    ###################
    # Access to cache #
    ###################
    def get_cache(self) -> list:
        """ Returns the input buffer cache """
        return self.__cache.get_cache()
