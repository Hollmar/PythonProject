from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from room import Room
from popups import CreateRoomPopup

room_list = []


class RoomManagerScreen(Screen):
    NoRoomsSet = True

    # function to delete room
    def delete_room(self, room):
        self.ids.stack_layout.remove_widget(room.Button)
        room_list.remove(room)
        if len(room_list) == 1:
            self.ids.bottom_label.text = str(len(room_list)) + " Room set"
        else:
            self.ids.bottom_label.text = str(len(room_list)) + " Rooms set"

    # function to change view to deviceview
    def change_screen(self, room):
        self.manager.current = "devices"
        self.manager.transition.direction = "left"
        devices = self.manager.get_screen("devices")
        devices.create_screen(room)
        room.updateEvent = Clock.schedule_interval(lambda x: devices.update_widgets(room), 0.1)

    # function to add a room
    def add_room(self, name):
        name_used = False
        for room in room_list:
            if room.RoomName == name:
                name_used = True
                self.ids.bottom_label.text = "Name already in use"
        if not name_used:
            self.ids.stack_layout.remove_widget(self.ids.add_button)
            btn = Button(size=(self.width / 6, self.height / 5), size_hint=(None, None), font_size=25, text=name)
            new_room = Room(name, btn)
            btn.bind(on_release=lambda x: self.change_screen(new_room))
            room_list.append(new_room)
            self.ids.stack_layout.add_widget(new_room.Button)
            self.ids.stack_layout.add_widget(self.ids.add_button)
            if len(room_list) == 1:
                self.ids.bottom_label.text = str(len(room_list)) + " Room set"
            else:
                self.ids.bottom_label.text = str(len(room_list)) + " Rooms set"

    # function to return screen "room"
    @staticmethod
    def get_current_room(name):
        for room in room_list:
            if room.RoomName == name:
                return room

    # function to activate CreateRoomPopup
    def create_room_show(self):
        show = CreateRoomPopup(self)
        popup_window = Popup(title="Name your Room", content=show, size_hint=(None, None), size=(400, 400),
                             auto_dismiss=False)
        show.ids.okButton.on_release = popup_window.dismiss
        show.ids.cancelButton.on_release = popup_window.dismiss
        popup_window.open()
