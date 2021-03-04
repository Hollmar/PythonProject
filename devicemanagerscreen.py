from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from deviceview import BrightnessSensor, DeviceView, DeviceType, Router, UndefinedDeviceView
from popups import DeleteRoomPopup, AddDevicePopup, LoadPopup, AddDeviceFailedPopup
from controller import Controller
import os


if os.name == 'Windows':
    sun_picture = 'images\Sonne_HD.jpg'
    router_picture = 'images\Router.jpg'
else:
    sun_picture = 'images/Sonne_HD.jpg'
    router_picture = 'images/Router.jpg'


c = Controller

class DeviceManagerScreen(Screen):

    def update_widgets(self, room):
        self.ids.stack_layout.clear_widgets()
        self.ids.label1.text = room.RoomName
        for device in room.device_list:
            self.ids.stack_layout.add_widget(device.Widget)
        self.ids.stack_layout.add_widget(self.ids.add_button)

    def delete_room(self):
        rooms = self.manager.get_screen("rooms")
        rooms.delete_room(self.get_current_room())
        self.manager.current = "rooms"
        self.manager.transition.direction = "right"

    def add_device(self, eui64, name):
        #self.c.addDevice(eui64)
        self.add_undefined(eui64,name)

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
        device = UndefinedDeviceView(eui64, name, label)
        room = self.get_current_room()
        room.device_list.append(device)

    def add_brightness_sensor(self, eui64, name):
        btn = Button(size_hint=(0.2, 0.25), font_size=20, color=(1,1,1,1), background_normal = sun_picture, id=eui64)
        device = BrightnessSensor(eui64, name, btn)
        btn.bind(on_release=lambda x: self.brightness_change_screen(device))
        btn.text = str(device.sensorvalue)+" Lux"+"\n\n\n"+name
        room = self.get_current_room()
        room.device_list.append(device)

    def add_router(self, eui64, name):
        btn = Button(size_hint=(0.2, 0.25), font_size=20, text="\n\n\n"+name,background_disabled_normal=router_picture,disabled=True, id=eui64, color=(0, 0, 0, 1))
        device = Router(eui64, name, btn)
        room = self.get_current_room()
        room.device_list.append(device)

    def brightness_change_screen(self,device):
        self.manager.current = "brightness"
        self.manager.transition.direction = "left"
        brightness = self.manager.get_screen("brightness")
        brightness.create_screen(device)

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
