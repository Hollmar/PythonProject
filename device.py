from enum import Enum

#TODO: add enum for different device types
#TODO: potentially use inheritance
class DeviceType(Enum):
    ERROR = 1
    ROUTER = 2
    BRIGHTNESS = 3

class Device:
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget



