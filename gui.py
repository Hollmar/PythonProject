from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import kivy.core.window
from roommanagerscreen import RoomManagerScreen
from devicemanagerscreen import DeviceManagerScreen
from brightnessscreen import BrightnessScreen
from controller import Controller
from kivy.core.image import Image
from kivy.properties import NumericProperty
from kivy.uix.vkeyboard import VKeyboard

from kivy.core.window import Window

Window.size = (800, 460)
Window.fullscreen = True
#Window.top = -15

Window.clearcolor = (1, 1, 1, 1)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class GUI(App):
    def build(self):
        return kv


if __name__ == "__main__":
    GUI().run()
