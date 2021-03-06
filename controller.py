import socket
import asyncio
from sys import exit
import threading
from time import sleep
import time
from json import load as load_json
from deviceview import DeviceType
from device import Device
from device import DeviceState

with open('config.json') as cf:
    config = load_json(cf)
# test change for git
HOST = config["socket"]["host"]
PORT2SERVER = config["socket"]["port1"]
PORT2DATA = config["socket"]["port2"]
eui = 0

#Test this

testDevice1 = Device("832813223233")
testDevice2 = Device("321919239129")
testDevice3 = Device("012312312312")
testDevice4 = Device("325435893748")
testDevice5 = Device("276834234343")

testDevice1.deviceState = DeviceState.UNDEFINED
testDevice2.deviceState = DeviceState.UNDEFINED
testDevice3.deviceState = DeviceState.ADDED
testDevice4.deviceState = DeviceState.ADDED
testDevice5.deviceState = DeviceState.INITIALIZED



class Controller:
    class __Controller:
        def __init__(self):
            pass
    instance = None

    def __init__(self, device_dict):
        self.device_dict = {}
        if not Controller.instance:
            Controller.instance = Controller.__Controller

    # commands = [b"getLeaderState", "addDevice", b"networkReset", "removeDevice"]

    def getLeaderState(self):
        pass

    def testDevices(self):
        self.device_dict[testDevice1.eui64] = testDevice1
        self.device_dict[testDevice2.eui64] = testDevice2
        self.device_dict[testDevice3.eui64] = testDevice3
        self.device_dict[testDevice4.eui64] = testDevice4
        self.device_dict[testDevice5.eui64] = testDevice5

    async def addDevice(self, eui64):
        #Delete later please
        self.testDevices()
        ####################
        d1 = Device(eui64)
        self.device_dict[eui64] = d1
        d1.deviceStatus = DeviceState.UNDEFINED
        self.device_dict[eui64] = d1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT2SERVER))

        req = bytes(("addDevice" + " " + eui64).encode('utf-8'))

        s.sendall(req)
        data = s.recv(config["socket"]["buffer_size"])
        s.close()

        d1.deviceStatus = DeviceState.ADDED
        if (b"OK" == data):
            d1.deviceStatus = DeviceState.INITIALIZED
            return DeviceType.OK
        else:
            self.device_dict.pop(eui64)
            return DeviceType.ERROR


    def getDevices(self):
        return list(self.device_dict.values())

    def between_callback(self, eui64):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.addDevice(eui64))
        loop.close()

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
                        sensor_data = conn.recv(config["socket"]["buffer_size"])
                        print(sensor_data)
                        sleep(0.001)

    th_requester = threading.Thread(target=between_callback)
    th_requester.start()

    th_client_data = threading.Thread(target=client_data)
    th_client_data.start()