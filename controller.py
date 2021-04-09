import socket
import asyncio
from sys import exit
import threading
from time import sleep
import time
from json import load as load_json
from deviceview import DeviceType
from device import Device, BrightnessSensor, Router
from device import DeviceState

with open('config.json') as cf:
    config = load_json(cf)
# test change for git
HOST = config["socket"]["host"]
PORT2SERVER = config["socket"]["port1"]
PORT2DATA = config["socket"]["port2"]
eui = 0

class Controller:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.device_dict = dict()
        th_client_data = threading.Thread(target=self.client_data)
        th_client_data.start()


    # commands = [b"getLeaderState", "addDevice", b"networkReset", "removeDevice"]

    def getLeaderState(self):
        pass


    #testmethods
    def testAddDevice1(self,eui64):
        self.device_dict[eui64] = Device(eui64)
        device = self.device_dict[eui64]
        device.deviceState = DeviceState.UNDEFINED

    def testAddDevice2(self,eui64):
        self.device_dict[eui64] = Device(eui64)
        device = self.device_dict[eui64]
        device.deviceState = DeviceState.ADDED

    def testAddDevice3(self,eui64):
        self.device_dict[eui64] = BrightnessSensor(eui64)
        device = self.device_dict[eui64]
        device.deviceState = DeviceState.INITIALIZED

    def addDevice(self, eui64):
        d1 = Device(eui64)
        d1.deviceState = DeviceState.UNDEFINED
        self.device_dict[eui64] = d1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT2SERVER))
        req = bytes(("addDevice" + " " + eui64).encode('utf-8'))
        s.sendall(req)
        #s.close()

    def getDevices(self):
        return list(self.device_dict.values())


    def client_data(self):
        print("client data start")
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT2DATA))
                s.listen()
            except Exception as e:
                print(str(e))
                break
            else:
                print("else block")
                conn, addr = s.accept()
                with conn:
                    print('2 Connected by', addr)
                    while True:
                        data = conn.recv(config["socket"]["buffer_size"])
                        print(b"controller data" + data)
                        r_data = data.split(b" ")
                        #print("controller r_data" + str(r_data))
                        #Check AddDeviceResponse
                        if r_data[0] == b"addDeviceResponse":
                            data_info = r_data[1].split(b';')
                            print("data_info" + str(data_info))
                            if data_info[1] == b"OK":
                                eui = data_info[0].decode('utf-8')
                                print(eui)
                                print(str(self.device_dict.get(eui).deviceState))
                                self.device_dict.get(eui).deviceState = DeviceState.ADDED
                                print(str(self.device_dict.get(eui).deviceState))
                                print("OK")
                            else:
                                self.device_dict.pop(data_info[0])
                                print("ERROR addDeviceResponse")

                        #Check for deviceSetupInfo and deviceData
                        elif r_data[0] == b'deviceSetupInfo':
                            data_info = r_data[1].split(b';')
                            print("data_info" + str(data_info))
                            if data_info[1] == b'BRIGHTNESS':
                                eui = data_info[0].decode('utf-8')
                                print(str(self.device_dict.get(eui).deviceState))
                                self.device_dict.get(eui).deviceState = DeviceState.INITIALIZED
                                print(str(self.device_dict.get(eui).deviceState))
                            elif data_info[1] == b"ROUTER":
                                tempDevice = Router(data_info[0])
                                tempDevice.deviceState = DeviceState.INITIALIZED
                                self.device_dict[data_info[0]] = tempDevice
                            else:
                                print("error")
                        elif r_data[0] == b"deviceData":
                            data_info = r_data[1].split(b';')
                            eui = data_info[0].decode('utf-8')
                            self.device_dict.get(eui).lux = data_info[1]
                            print(str(self.device_dict.get(eui).lux))
                        #print(data)
                        #sleep(0.5)
