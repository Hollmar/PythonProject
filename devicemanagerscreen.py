from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from device import Device, BrightnessSensor, Router, DeviceState
from deviceview import DeviceView
#from deviceview import BrightnessSensorView, DeviceView, DeviceType, RouterView, UndefinedDeviceView
from popups import DeleteRoomPopup, AddDevicePopup, LoadPopup, AddDeviceFailedPopup
from controller import Controller
import os


if os.name == 'Windows':
    sun_picture = 'images\Sonne_HD.jpg'
    router_picture = 'images\Router.jpg'
else:
    sun_picture = 'images/Sonne_HD.jpg'
    router_picture = 'images/Router.jpg'



class DeviceManagerScreen(Screen):

    def __init__(self, **kwargs):
        super(DeviceManagerScreen, self).__init__(**kwargs)
        self.c = Controller()
        self.count = 0 #testing attribute will be removed

    def create_screen(self, room):
        self.ids.stack_layout.clear_widgets()
        self.ids.label1.text = room.RoomName
        for key,value in room.device_dict.items():
            self.ids.stack_layout.add_widget(value.Widget)
        self.ids.stack_layout.add_widget(self.ids.add_button)

    def update_widgets(self, room):
        device_list = self.c.getDevices()
        for device in device_list:
            if device.eui64 in room.device_dict.keys():
                if device.getDeviceState() == DeviceState.UNDEFINED:
                    self.update_undefined(room.device_dict[device.eui64], device)
                elif device.getDeviceState() == DeviceState.ADDED:
                    self.update_undefined(room.device_dict[device.eui64], device)
                elif device.getDeviceState() == DeviceState.INITIALIZED:
                    if type(device) is BrightnessSensor:
                        self.update_brightness(room.device_dict[device.eui64], device.getSensorValue())
                    if type(device) is Router:
                        self.update_router(room.device_dict[device.eui64])
        self.create_screen(self.get_current_room())

    def delete_room(self):
        self.go_back()
        rooms = self.manager.get_screen("rooms")
        rooms.delete_room(self.get_current_room())

    def add_device(self, eui64, name):
        #self.add_undefined(eui64,name)
        self.c.addDevice(eui64)
        #testing different devices
        """
        self.count += 1
        if self.count % 3 == 0:
            self.c.testAddDevice1(eui64)
        elif self.count % 3 == 1:
            self.c.testAddDevice2(eui64)
        else:
            self.c.testAddDevice3(eui64)
        """
        self.create_screen(self.get_current_room())


    def add_error(self, eui64):
        show = AddDeviceFailedPopup()
        popup_window = Popup(title="Connection to device with the EUI64 "+eui64+" failed.", content=show,
                             size_hint=(None, None), size=(400, 200))
        popup_window.open()
        show.ids.okButton.on_release = popup_window.dismiss

    def loading_popup(self):
        show = LoadPopup()
        popup_window = Popup(title="loading..", content=show, size_hint=(None, None), size=(400, 200))
        popup_window.open()
        show.ids.okButton.on_release = popup_window.dismiss

    def add_undefined(self, eui64, name):
        label = Label(size_hint=(0.2,0.25), font_size=16, color=(0,0,0,1), text='Adding device:\n' + name + '\nwith eui64:\n' + eui64)
        device = DeviceView(eui64, name, label)
        room = self.get_current_room()
        room.device_dict[eui64] = device

    def update_undefined(self, DeviceView, Device):
        DeviceView.Widget = Label(size_hint=(0.2,0.25), font_size=16, color=(0,0,0,1), text='Adding device:\n' + DeviceView.Name + '\nwith eui64:\n' + Device.eui64)

    def update_brightness(self, DeviceView, sensorValue):
        btn = Button(size_hint=(0.2, 0.25), font_size=20, color=(1,1,1,1), background_normal = sun_picture)
        btn.bind(on_release=lambda x: self.brightness_change_screen(DeviceView))
        btn.text = str(sensorValue)+" Lux"+"\n\n\n"+ DeviceView.Name
        DeviceView.Widget = btn

    def add_router(self, eui64, name):
        btn = Button(size_hint=(0.2, 0.25), font_size=20, text="\n\n\n"+name,background_disabled_normal=router_picture,disabled=True, id=eui64, color=(0, 0, 0, 1))
        device = DeviceView(eui64, name, btn)
        room = self.get_current_room()
        room.device_dict.append(device)

    def brightness_change_screen(self, deviceView):
        self.manager.current = "brightness"
        self.manager.transition.direction = "left"
        brightness = self.manager.get_screen("brightness")
        brightness.create_screen(deviceView)

    def get_current_room(self):
        rooms = self.manager.get_screen("rooms")
        current_room = rooms.get_current_room(self.ids.label1.text)
        return current_room

    def delete_room_show(self):
        show = DeleteRoomPopup(self)
        popup_window = Popup(title="Are you sure you want to delete the Room?", content=show, size_hint=(None, None),
                             size=(400, 400))
        show.ids.okButton.on_press = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()

    def add_device_show(self):
        show = AddDevicePopup(self)
        popup_window = Popup(title="Give Devicename and EUI64 ", content=show, size_hint=(None, None), size=(400, 400))
        show.ids.okButton.on_press = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()

    def go_back(self):
        self.manager.current = "rooms"
        self.manager.transition.direction = "right"
        self.get_current_room().updateEvent.cancel()
