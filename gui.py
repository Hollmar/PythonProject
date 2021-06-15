from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

#window settings
Window.size = (800, 480)
Window.fullscreen = True
Window.clearcolor = (1, 1, 1, 1)

#Screenmanager needed to navigate between different views
class WindowManager(ScreenManager):
    pass

#loading kv-file
kv = Builder.load_file("my.kv")


class GUI(App):
    def build(self):
        return kv


if __name__ == "__main__":
    GUI().run()
