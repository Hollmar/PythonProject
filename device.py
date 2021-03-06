from enum import Enum


class deviceStatus(Enum):
    UNDEFINED  : 1
    ADDED      : 2
    INITIALIZED: 3


class Device:

    eui64 = 0
    deviceStatus = 0
    deviceType = 0

    def __init__(self, eui):
        self.eui64 = eui
        self.deviceStatus = 0
    
    def setDeviceStatus(self, status):
        self.deviceStatus= status

    def setDeviceType(self, type):
        self.deviceType = type

    def getDeviceStatus(self):
        return self.deviceStatus

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