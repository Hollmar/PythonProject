from enum import Enum


class DeviceState(Enum):
    UNDEFINED = 1
    ADDED = 2
    INITIALIZED = 3


class Device:
    def __init__(self, eui):
        self.eui64 = eui
        self.deviceState = DeviceState.UNDEFINED
    
    def setDeviceState(self, state):
        self.deviceState = state

    def getDeviceState(self):
        return self.deviceState

class BrightnessSensor(Device):
    lux = 0

    def updateSensorValue(self, value):
        self.lux = value
    def getSensorValue(self):
        return self.lux

class Router(Device):
    children = 0