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
        s.close()

    def getDevices(self):
        return list(self.device_dict.values())

    def client_data(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((HOST, PORT2DATA))
                    s.listen()
            except:
                print("kein socket")
                break
            else:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = s.recv(config["socket"]["buffer_size"])
                        r_data = data.split(" ")
                        data_info = r_data[1].split(";")

                        #Check AddDeviceResponse
                        if r_data[0] == b"addDeviceResponse":
                            if data_info[1] == b"OK":
                                self.device_dict[data_info[0]] = DeviceState.ADDED
                                return DeviceType.OK
                            else:
                                self.device_dict.pop(data_info[0])
                                return DeviceType.ERROR

                        sensor_data = conn.recv(config["socket"]["buffer_size"])
                        s_data = sensor_data.split(" ")
                        s_info = s_data[1].split(";")

                        #Check for deviceSetupInfo and deviceData
                        if s_data[0] == b"deviceSetupInfo":
                            if s_info[1] == b"brightness":
                                tempDevice = BrightnessSensor(s_info[0])
                                tempDevice.deviceState = DeviceState.INITIALIZED
                                self.device_dict[s_info[0]] = tempDevice
                                return DeviceType.OK
                            elif s_info[1] == b"Router":
                                tempDevice = Router(s_info[0])
                                tempDevice.deviceState = DeviceState.INITIALIZED
                                self.device_dict[s_info[0]] = tempDevice
                                return DeviceType.OK
                            else:
                                return DeviceType.ERROR
                        elif s_data[0] == b"deviceData":
                            tempDevice = self.device_dict[s_info[0]]
                            tempDevice.lux = s_info[1]
                            return DeviceType.OK
                        else:
                            print("ERROR")
                            return
                        print(sensor_data)
                        sleep(0.001)

    th_client_data = threading.Thread(target=client_data)
    th_client_data.start()
