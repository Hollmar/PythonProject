import socket 
from sys import exit 
import threading 
from time import sleep
from json import load as load_json
from device import DeviceType
from enum import Enum
from device import Device

with open('config.json') as cf:
    config = load_json(cf)
#test change for git
HOST = config["socket"]["host"]
PORT2SERVER = config["socket"]["port1"]
PORT2DATA = config["socket"]["port2"]
eui = 0

class deviceStatus(Enum):
    UNDEFINED  : 1
    ADDED      : 2
    INITIALIZED: 3

class Controller:
    class __Controller:
        def __init__(self):
            pass
    instance = None
    def __init__(self,device_dict, device_list):
        self.device_dict = {}
        self.device_list = list(())
        if not Controller.instance:
            Controller.instance = Controller.__Controller

#commands = [b"getLeaderState", "addDevice", b"networkReset", "removeDevice"]

    def addDevice(eui64):
        device_list.append(eui64)
        device_dict[eui64] = deviceStatus.UNDEFINED
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT2SERVER))

        req = bytes(("addDevice" + " " + eui64).encode('utf-8'))

        s.sendall(req)
        data = s.recv( config["socket"]["buffer_size"] )
        s.close()

        device_dict[eui64] = deviceStatus.ADDED

        if (eui64 == data):
            device_dict[eui64] = deviceStatus.INITIALIZED
            return DeviceType.OK
        else:
            deivce_list.remove(eui64)
            device_dict.pop(eui64)
            return DeviceType.ERROR
    
    def checkDict(dict, list):
        for x in list:
            for y in dict:
                if(x == y):
                    continue
                else:

        
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

    th_requester = threading.Thread( target=adddevice )
    th_requester.start()

    th_client_data = threading.Thread( target=client_data )
    th_client_data.start()