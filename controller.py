import socket 
from sys import exit 
import threading 
from time import sleep
from json import load as load_json
from device import DeviceType

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

#commands = [b"getLeaderState", "addDevice", b"networkReset", "removeDevice"]

    def getLeaderState():
        

    def addDevice(eui64):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT2SERVER))

        req = bytes(("addDevice" + " " + eui64).encode('utf-8'))

        s.sendall(req)
        data = s.recv( config["socket"]["buffer_size"] )
        r_data = (data.split(b" "))[1].split(b";")
        s.close()

        if (eui64 == r_data[0]):
            if(r_data[1] == "brightness"): #TODO
                return DeviceType.BRIGHTNESS
            elif(r_data[1] == "router"): #TODO
                return DeviceType.ROUTER
        else:
            return DeviceType.ERROR
        
        
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
        

        

