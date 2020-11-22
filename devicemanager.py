from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from device import DeviceType, Router, BrightnessSensor
from popups import DeleteRoomPopup, AddDevicePopup, LoadPopup, AddDeviceFailedPopup
from controller import Controller


class DeviceManager(Screen):
    def create_screen(self, room):
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
        show = LoadPopup()
        popup_window = Popup(title="Waiting for response...",content=show, size_hint=(None, None),size=(400, 200))
        popup_window.open()
        room = self.get_current_room()
        c = Controller
        devicetype = c.addDevice(eui64)
        if devicetype == DeviceType.ERROR:
            self.add_error(eui64)
        elif devicetype == DeviceType.BRIGHTNESS:
            self.add_brightness_sensor(eui64, name)
        elif devicetype == DeviceType.ROUTER:
            self.add_router(eui64, name)
        popup_window.dismiss()
        self.create_screen(room)

    def add_error(self, eui64):
        show = AddDeviceFailedPopup()
        popup_window = Popup(title="Connecting to device with the EUI64 "+eui64+" failed.", content=show,
                             size_hint=(None, None), size=(400, 200))
        popup_window.open()
        show.ids.okButton.on_release = popup_window.dismiss

    def add_brightness_sensor(self, eui64, name):
        btn = Button(size_hint=(0.2, 0.25), font_size=20, text="BrightnessSensor", id=eui64)
        device = BrightnessSensor(eui64, name, btn)
        btn.bind(on_release=lambda x: self.brightness_change_screen(device))
        room = self.get_current_room()
        room.device_list.append(device)

    def add_router(self, eui64, name):
        label = Label(size_hint=(0.2, 0.25), font_size=20, text="Router", id=eui64, color=(1, 0, 0, 1))
        device = Router(eui64, name, label)
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
        show.ids.okButton.on_release = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()

    def add_device_show(self):
        show = AddDevicePopup(self)
        popup_window = Popup(title="Give Devicename and EUI64 ", content=show, size_hint=(None, None), size=(400, 400))
        show.ids.okButton.on_release = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()
