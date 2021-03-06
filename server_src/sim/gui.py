# Standard library imports
from json import load as load_json
import socket
from sys import exit
import threading
from time import sleep


with open('../../config.json') as cf:
    config = load_json(cf)

HOST = config["socket"]["host"]
PORT2SERVER = config["socket"]["port1"]
PORT2DATA = config["socket"]["port2"]

def request():
    req = ""
    commands = [b"getLeaderState",b"networkReset","addDevice"]

    while True:

        for i in range(len(commands)):
            print(str(i)+" - "+str(commands[i]))

        choice = input()

        if 'q' == choice:
            break

        elif '0' == choice:
            req = commands[0]

        elif '1' == choice:
            req = commands[1]

        elif '2' == choice:
            eui64 = input("EUI64: ")
            req = bytes((commands[2]+" "+eui64).encode('utf-8'))

        else:
            print("Unvalid option")
            exit(-1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT2SERVER))
        except ConnectionRefusedError:
            continue

        s.sendall(req)


def client_data():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.bind((HOST, PORT2DATA))
            s.listen()

            conn, addr = s.accept()

            with conn:
                print('Connected by', addr)
                while True:
                    sensor_data = conn.recv( config["socket"]["buffer_size"] )
                    print('>>> Received', repr(sensor_data))
                    sleep( 0.001 )
                    if sensor_data == b'':
                        exit()



th_requester = threading.Thread( target=request )
th_requester.start()

th_client_data = threading.Thread( target=client_data )
th_client_data.start()
