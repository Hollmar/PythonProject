# Standard library imports
import logging
from re import search
from socket import (socket, AF_INET, SOCK_STREAM)
from time import sleep
from threading import Lock

# Local application imports
from events import exit_event
from nrf.nrf import nRF52840
from req_response import req_response
from socket_config import SocketConfig

def data_thread(nrf: nRF52840, lock: Lock, socket_config: SocketConfig) -> None:
    """ Thread frequently checking buffer for data by child-nodes """
    logging.info( 'DATA_THREAD started...' )

    with lock:
        nrf.udp_open()
        nrf.udp_bind()

    data_socket = socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            data_socket.connect( socket_config.CONN )
        except ConnectionRefusedError:
            # wait till controller is ready
            sleep( 1 )
            continue
        else:
            break

    while True:
        if exit_event.is_set():
            break

        with lock:
            #logging.info( "DATA_SET=" + str(req_response.is_set()) )
            if req_response.is_set():
                data_socket.sendall( req_response.get() )
                req_response.clear()


        with lock:
            buffer = nrf.read_buffer(False)
            buffer = buffer + nrf.get_cache()

        logging.debug( 'BUF_ADD_' + str(buffer) )

        if buffer:
            for data in buffer:
                if search( b'bytes', data ):
                    logging.info( b'DATA_' + data )
                    data_socket.sendall(data)

        sleep( 0.1 )
