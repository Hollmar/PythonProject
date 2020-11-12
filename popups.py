from kivy.uix.floatlayout import FloatLayout


class CreateRoomPopup(FloatLayout):
    def __init__(self, obj, **kwargs):
        super(CreateRoomPopup, self).__init__(**kwargs)
        self.obj = obj


class AddDevicePopup(FloatLayout):
    def __init__(self, obj, **kwargs):
        super(AddDevicePopup, self).__init__(**kwargs)
        self.obj2 = obj


class DeleteRoomPopup(FloatLayout):
    def __init__(self, obj, **kwargs):
        super(DeleteRoomPopup, self).__init__(**kwargs)
        self.obj = obj
