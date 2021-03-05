from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from roommanagerscreen import RoomManagerScreen
from devicemanagerscreen import DeviceManagerScreen
from brightnessscreen import BrightnessScreen
from controller import Controller

Window.clearcolor = (1, 1, 1, 1)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class GUI(App):
    def build(self):
        return kv


if __name__ == "__main__":
    GUI().run()
