"""
Main file
Read configuration and start threads
Stuff:
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/establish-serial-connection.html#adding-user-to-dialout-on-linux
deviceSetupInfo <eui64;Type;ipv6> -> Type=[Light,Router]
deviceData <eui64; data>
"""

# Standard library imports
from json import load as load_json
import logging
import threading

# Local application imports
from nrf import nrf_dongle
from socket_config import SocketConfig

from cmd_thread import cmd_thread
from data_thread import data_thread


def main():
    # Global logging level
    logging.basicConfig(level=logging.INFO,
                        #filename='myapp.log',
                        format='%(asctime)s::%(levelname)s: %(message)s'
                        )


    # Read configuration
    with open('../config.json') as cf:
        config = load_json( cf )

    # Socket arguments
    socket_conf_server = SocketConfig(
        config["socket"]["host"],
        config["socket"]["port1"],
        config["socket"]["buffer_size"]
    )

    socket_conf_client = SocketConfig(
        config["socket"]["host"],
        config["socket"]["port2"],
        config["socket"]["buffer_size"]
    )

    lock = threading.Lock()

    th_server = threading.Thread( target=cmd_thread, args=[ nrf_dongle,
                                                            lock,
                                                            socket_conf_server,
                                                            config["network"]["pairing_time_s"]
                                                        ])
    th_server.name = "cmd_server"
    th_server.daemon = True
    th_server.start()

    th_client = threading.Thread( target=data_thread, args=[ nrf_dongle,
                                                            lock,
                                                            socket_conf_client
                                                        ])
    th_client.name = "data_client"
    th_client.daemon = True
    th_client.start()

    th_server.join()
    th_client.join()

if __name__ == "__main__":
    main()
