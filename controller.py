import socket 
from sys import exit 
import threading 
from time import sleep
from json import load as load_json

with open('config.json') as cf:
    config = load_json(cf)
#test change for git
HOST = config["socket"]["host"]
PORT2SERVER = config["socket"]["port1"]
PORT2DATA = config["socket"]["port2"]
eui = 0

class Controller:
    class __Controller:
        def __init__(self):
            pass
    instance = None
    def __init__(self):
        if not Controller.instance:
            Controller.instance = Controller.__Controller

    def addDevice(eui64):
        eui = eui64

    def status():
        print("Device has been added!")

    def request():
        req = ""
        commands = [b"getLeaderState", b"networkReset", "addDevice"]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT2SERVER))

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
                req = bytes((commands[2] + " " + eui64).encode('utf-8'))
            else:
                print("Unvalid option")
                exit(-1)
            s.sendall(req)
            data = s.recv( config["socket"]["buffer_size"] )

            if data == b"OK":
                status()
            elif data == b"ERROR":
                break

            print('>>> Received', repr(data))

    def client_data():
        while True:
            with socket.socket(socket.AF_INET, socket. socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT2DATA))
                s.listen()
                conn, addr = s.accept()

                with conn:
                    print('Connected by', addr)
                    while True:
                        sensor_data = conn.recv( config["socket"]["buffer_size"] )
                        print(sensor_data)
                        sleep( 0.001 )

    th_requester = threading.Thread( target=request )
    th_requester.start()

    th_client_data = threading.Thread( target=client_data )
    th_client_data.start()
        

        

