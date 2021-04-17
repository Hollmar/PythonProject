# Standard library imports
import logging
from re import (
    compile as make_pattern,
    match,
    search
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from threading import Lock
from time import sleep, time

# Local application imports
from events import exit_event
from nrf.msg import ERROR_MSG, SUCCESS_MSG
from nrf.nrf import nRF52840
from nrf.states import States
from req_response import req_response
from socket_config import SocketConfig

def cmd_thread(nrf: nRF52840, lock: Lock, socket_config: SocketConfig, pairing_time_s: int) -> None:
    """ Thread handling requests by GUI """
    logging.info( 'SERVER_THREAD started...' )

    # Main thread loop
    while True:
        if exit_event.is_set():
            break

        with socket(AF_INET, SOCK_STREAM) as cmd_server:
            cmd_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

            cmd_server.bind( socket_config.CONN )
            cmd_server.listen()
            conn, addr = cmd_server.accept()

            with conn:
                logging.info( 'Connected by' + str(addr) )

                request = conn.recv( socket_config.BUFFER_SIZE )

                logging.debug( 'REQ_' + str(request) )

                if request == b"getLeaderState":
                    with lock:
                        req_response.set(
                            nrf.check_state(
                                States.STATE_LEADER,
                                save_buffer=True
                            )
                        )


                elif request == b"networkReset": # NOTE Coming soon
                    return
                    with lock:
                        nrf.reset_device()

                        #XXX Reset msgs over UDP
                        #udp = nrf.Udp(b'ff03::1', b'1212')
                        #udp.open(ser)
                        #udp.send(ser, b'networkReset')

                        nrf.check_state( States.STATE_DISABLED, True )
                    response = SUCCESS_MSG

                elif match( b"addDevice", request ):
                    eui64: bytes = request.split(b':')[1]

                    response = add_device(nrf, eui64, lock, pairing_time_s)

                    with lock:
                        req_response.set( response )
                        #logging.info( "CMD_SET=" + str(req_response.is_set()) )

                with lock:
                    logging.info(">>> Response: " + repr( req_response.get() ))

    # End main loop


def add_device(nrf: nRF52840, eui64: bytes, lock: Lock, pairing_time: int) -> bytes:
    """ Try to add an end device """
    response = b'addDeviceResponse:' + eui64 + b';'
    sleep_time_s = 0.01

    lock.acquire()

    if not add_device.first_dev_conn:
        add_device.first_dev_conn = True
        nrf.start_commissioner() # only needed once

    nrf.add_device( eui64 )

    lock.release()

    # compile to pattern object
    dev_connect_condition = make_pattern(b'Commissioner: Joiner connect *')

    # remove the sleep time from total time
    pairing_time = int( pairing_time - (pairing_time * sleep_time_s) )

    start_time = time()

    lock.acquire()

    for _ in range(0, pairing_time):
        #lock.acquire()
        buffer = nrf.read_buffer(save_buffer=True)
        #lock.release()

        if list( filter( dev_connect_condition.match, buffer ) ):
            add_device.first_dev_conn = True

            response += SUCCESS_MSG
            break

        sleep( sleep_time_s )

    lock.release()

    logging.debug("--- %s seconds ---" % (time() - start_time))

    if not search( SUCCESS_MSG, response ):
        response += ERROR_MSG

    return response

# static variable
add_device.first_dev_conn = False
