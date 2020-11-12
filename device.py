from kivy.graphics import *
from kivy.uix.screenmanager import Screen


class Device:
    def __init__(self, eui64, name, widget):
        self.EUI64 = eui64
        self.Name = name
        self.Widget = widget



