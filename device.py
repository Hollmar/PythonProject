from enum import Enum


class DeviceType(Enum):
    ERROR = 1
    ROUTER = 2
    BRIGHTNESS = 3


class Device:
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget


class Router(Device):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget


class BrightnessSensor(Device):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget
        self.sensorvalue = 0

    def update_sensorvalue(self, newvalue):
        self.sensorvalue = newvalue




