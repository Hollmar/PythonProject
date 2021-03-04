from enum import Enum


class DeviceType(Enum):
    ERROR = 1
    OK = 2


class DeviceView:
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget

class UndefinedDeviceView(DeviceView):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget

class Router(DeviceView):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget


class BrightnessSensor(DeviceView):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget
        self.sensorvalue = 0

    def update_sensorvalue(self, newvalue):
        self.sensorvalue = newvalue




