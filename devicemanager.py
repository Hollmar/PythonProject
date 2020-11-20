from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from device import DeviceType,Device
from popups import DeleteRoomPopup, AddDevicePopup, LoadPopup
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

#TODO: add loading Popup
#TODO: add funcionality to distinguish device types
    def add_device(self, eui64,name):
        show = LoadPopup(self)
        popup_window = Popup(title="Waiting for response...",content=show, size_hint=(None, None),size=(400, 200))
        popup_window.open();
        room = self.get_current_room()
        c = Controller
        devicetype = c.addDevice(eui64)
        if devicetype == DeviceType.ERROR:
            popup_window.title = "An error occured trying to add the device! :("
        elif devicetype == DeviceType.BRIGHTNESS:
            popup_window.dismiss()
            btn = Button(size_hint=(0.2, 0.25), font_size=20, text="BrightnessSensor", id=eui64)
            device = Device(eui64, name, btn)
            btn.bind(on_release=lambda x: self.brightness_change_screen(device))
            room.device_list.append(device)
        elif devicetype == DeviceType.ROUTER:
            popup_window.dismiss()
            label = Label(size_hint=(0.2, 0.25), font_size=20, text="Router", id=eui64, color=(1,0,0,1))
            device = Device(eui64, name, label)
            room.device_list.append(device)
        self.create_screen(room)

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
