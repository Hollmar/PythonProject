from kivy.uix.screenmanager import ScreenManager, Screen
from deviceview import DeviceView

class BrightnessScreen(Screen):

    def create_screen(self, sensor):
        self.display_sensorvalue(sensor, 110)
        self.ids.label1.text = sensor.Name
        self.ids.label3.text = "EUI64: "+sensor.EUI64

    def display_sensorvalue(self, sensor, newvalue):
        sensor.update_sensorvalue(newvalue)
        self.ids.label2.text = "Current brightness: " + str(sensor.sensorvalue) + " Lux"

