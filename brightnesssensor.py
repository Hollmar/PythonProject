from kivy.uix.screenmanager import ScreenManager, Screen
from device import Device

class BrightnessSensor(Screen):
    def create_screen(self,device):
        self.ids.label1.text = device.Name
        self.ids.label3.text = "EUI64: "+device.EUI64

