from enum import Enum


class DeviceState(Enum):
    UNDEFINED  : 1
    ADDED      : 2
    INITIALIZED: 3


class Device:

    eui64 = 0
    deviceState = 0
    deviceType = 0

    def __init__(self, eui):
        self.eui64 = eui
        self.deviceState = 0
    
    def setDeviceState(self, state):
        self.deviceState = state

    def setDeviceType(self, type):
        self.deviceType = type

    def getDeviceState(self):
        return self.deviceState

    def getDeviceType(self):
        return self.deviceType

class BrightnessSensor(Device):
    lux = 0

    def updateSensorValue(self, value):
        self.lux = value
    def getSensorValue(self):
        return self.lux

class Router(Device):
    children = 0