from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty


class UndefinedProgress(Image):
    angle = NumericProperty()


class CreateRoomPopup(FloatLayout):
    def __init__(self, obj, **kwargs):
        super(CreateRoomPopup, self).__init__(**kwargs)
        self.obj = obj


class AddDevicePopup(FloatLayout):
    def __init__(self, obj, **kwargs):
        super(AddDevicePopup, self).__init__(**kwargs)
        self.obj = obj


class DeleteRoomPopup(FloatLayout):
    def __init__(self, obj, **kwargs):
        super(DeleteRoomPopup, self).__init__(**kwargs)
        self.obj = obj


class LoadPopup(FloatLayout):
    pass


class AddDeviceFailedPopup(FloatLayout):
    pass
