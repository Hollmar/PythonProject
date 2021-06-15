from kivy.uix.screenmanager import Screen

class BrightnessScreen(Screen):

    # setting labels
    def create_screen(self, sensor):
        self.ids.label1.text = sensor.Name
        self.ids.label2.text = "Current brightness: 200 Lux"
        self.ids.label3.text = "EUI64: "+sensor.EUI64

    # function which is called regularly to update sensor value
    def display_sensorvalue(self, deviceview):
        devices = self.manager.get_screen("devices")
        device_list = devices.getDevices()
        for device in device_list:
            if device.eui64 == deviceview.EUI64:
                # checking the devicestate of each device for definition
                self.ids.label2.text = "Current brightness: " + str(device.lux).lstrip("0") + " Lux"

