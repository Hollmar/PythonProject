class Room:
    def __init__(self, room_name, button):
        self.RoomName = room_name
        self.Button = button
        self.device_dict = dict()
        self.updateEvent = 0

