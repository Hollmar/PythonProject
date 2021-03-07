from enum import Enum


class DeviceType(Enum):
    ERROR = 1
    OK = 2


class DeviceView:
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget
        self.SensorValue = 0

    def update_sensorvalue(self, newvalue):
        self.sensorvalue = newvalue

"""class UndefinedDeviceView(DeviceView):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget

class RouterView(DeviceView):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget


class BrightnessSensorView(DeviceView):
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget
        self.sensorvalue = 0

    def update_sensorvalue(self, newvalue):
        self.sensorvalue = newvalue

"""


