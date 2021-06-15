from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from device import BrightnessSensor, Router, DeviceState
from deviceview import DeviceView
from popups import DeleteRoomPopup, AddDevicePopup, LoadPopup, AddDeviceFailedPopup, UndefinedProgress
from controller import Controller
from kivy.clock import Clock
import os

if os.name == 'Windows':
    sun_picture = 'images\sun.png'
    router_picture = 'images\Router.jpg'
    undefined_picture = 'images\loading.png'
else:
    sun_picture = 'images/sun.png'
    router_picture = 'images/Router.jpg'
    undefined_picture = 'images/loading.png'


class DeviceManagerScreen(Screen):
    def __init__(self, **kwargs):
        super(DeviceManagerScreen, self).__init__(**kwargs)
        self.c = Controller()  # reference to controller in order to get devicelist
        self.angle = 0  # angle used to rotate loading animation

    # function which adds every widget to the layout
    def create_screen(self, room):
        self.ids.stack_layout.clear_widgets()
        self.ids.label1.text = room.RoomName
        for key, value in room.device_dict.items():
            self.ids.stack_layout.add_widget(value.Widget)
        self.ids.stack_layout.add_widget(self.ids.add_button)

    # function which is called by the clock in regular time stamps to synchronize every widget with the device
    # dictionary of the controller
    def update_widgets(self, room):
        device_list = self.c.getDevices()
        for device in device_list:
            if device.eui64 in room.device_dict.keys():
                # checking the devicestate of each device for definition
                if device.getDeviceState() == DeviceState.UNDEFINED:
                    self.update_undefined(room.device_dict[device.eui64])
                elif device.getDeviceState() == DeviceState.ADDED:
                    self.update_added(room.device_dict[device.eui64], device)
                elif device.getDeviceState() == DeviceState.INITIALIZED:
                    if type(device) is BrightnessSensor:
                        room.device_dict.get(device.eui64).SensorValue = device.lux
                        self.update_brightness(room.device_dict.get(device.eui64))
                    if type(device) is Router:
                        self.update_router(room.device_dict[device.eui64])
        self.create_screen(self.get_current_room())

    # function to delete a room
    def delete_room(self):
        self.go_back()
        rooms = self.manager.get_screen("rooms")
        rooms.delete_room(self.get_current_room())

    # function to add a device uses addDevice function of Controller
    def add_device(self, eui64, name):
        # checking input
        if eui64 in self.get_current_room().device_dict:
            show = AddDeviceFailedPopup()
            popup_window = Popup(title="EUI64: " + eui64 + " already exists.", content=show,
                                 size_hint=(None, None), size=(400, 200))
            popup_window.open()
            show.ids.okButton.on_release = popup_window.dismiss
            return
        elif len(eui64) != 16:
            show = AddDeviceFailedPopup()
            popup_window = Popup(title="EUI64: " + eui64 + " has wrong format.", content=show,
                                 size_hint=(None, None), size=(400, 200))
            popup_window.open()
            show.ids.okButton.on_release = popup_window.dismiss
            return
        # every device is added as undefined first
        self.add_undefined(eui64, name)
        # using controller function addDevice
        self.c.addDevice(eui64)
        # testing different devices
        """
        if self.count % 3 == 1:
            self.c.testAddDevice1(eui64)
        elif self.count % 3 == 2:
            self.c.testAddDevice2(eui64)
        else:
            self.c.testAddDevice3(eui64)
        self.count += 1
        self.create_screen(self.get_current_room())"""

    # function to add an undefined device to a list first state of the three possible states
    def add_undefined(self, eui64, name):
        label = Label(size=(self.width / 6, self.height / 5), size_hint=(None, None), font_size=16, color=(0, 0, 0, 1),
                      text='Adding device\n' 'with eui64:\n' + eui64 + "...")
        device = DeviceView(eui64, name, label)
        room = self.get_current_room()
        room.device_dict[eui64] = device

    # function to update device as undefined
    def update_undefined(self, deviceview):
        self.angle = self.angle + 10
        deviceview.Widget = UndefinedProgress(source=undefined_picture, size=(self.width / 6, self.height / 5),
                                              allow_stretch=False, size_hint=(None, None), angle=self.angle)

        # Label(size_hint=(0.2,0.25), font_size=16, color=(0,0,0,1),
        # text='Adding device:\n' + DeviceView.Name + '\nwith eui64:\n' + Device.eui64)

    # function ot update device as added
    def update_added(self, deviceview, device):
        deviceview.Widget = Label(size=(self.width / 6, self.height / 5), size_hint=(None, None), font_size=16,
                                  color=(0, 0, 0, 1),
                                  text='Device with eui64:\n' + device.eui64 + '\nhas been added.')

    # function to update device as brightnesssensor
    def update_brightness(self, deviceview):
        btn = Button(size=(self.width / 6, self.height / 5), size_hint=(None, None), font_size=20, color=(0, 0, 0, 1),
                     background_normal=sun_picture)
        btn.bind(on_release=lambda x: self.brightness_change_screen(deviceview))
        btn.text = str(deviceview.SensorValue).lstrip("0") + " Lux" + "\n\n\n" + deviceview.Name
        deviceview.Widget = btn

    # function to update device as router
    def update_router(self, deviceview):
        btn = Button(size=(self.width / 6, self.height / 5), size_hint=(None, None), font_size=16,
                     text=deviceview.Name + "\n\n\n" + deviceview.EUI64,
                     background_disabled_normal=router_picture, disabled=True, color=(0, 0, 0, 1))
        deviceview.Widget = btn

    # function to change screen to brightnesssensor screen and to set display_sensorvalue function to be called
    # every 0.1 seconds
    def brightness_change_screen(self, deviceView):
        self.manager.current = "brightness"
        self.manager.transition.direction = "left"
        brightness = self.manager.get_screen("brightness")
        brightness.create_screen(deviceView)
        deviceView.updateEvent = Clock.schedule_interval(lambda x: brightness.display_sensorvalue(deviceView), 0.1)

    # function to get a reference to the current room
    def get_current_room(self):
        rooms = self.manager.get_screen("rooms")
        current_room = rooms.get_current_room(self.ids.label1.text)
        return current_room

    # function to show popup after delete room button press
    def delete_room_show(self):
        show = DeleteRoomPopup(self)
        popup_window = Popup(title="Are you sure you want to delete the Room?", content=show, size_hint=(None, None),
                             size=(400, 400))
        show.ids.okButton.on_press = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()

    # function to show popup after pressing "+" button
    def add_device_show(self):
        show = AddDevicePopup(self)
        popup_window = Popup(title="Give Devicename and EUI64 ", content=show, size_hint=(None, None), size=(400, 400),
                             auto_dismiss=False)
        # keyboard = VKeyboard()
        # self.ids.float.add_widget(keyboard)
        show.ids.okButton.on_press = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()

    # function to go back to roommananagerscreen
    def go_back(self):
        self.manager.current = "rooms"
        self.manager.transition.direction = "right"
        self.get_current_room().updateEvent.cancel()

    # function to return devicelist
    def get_devices(self):
        return self.c.getDevices()
