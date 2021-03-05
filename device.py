class device:

    eui64 = 0
    deviceStatus = 0
    deviceType = 0

    def __init__(self, eui):
        self.eui64 = eui
        self.deviceStatus = 0
        self.deviceType = 0
    
    def setDeviceStatus(self, status):
        self.deviceStatus= status

    def setDeviceType(self, type):
        self.deviceType = type

    def getDeviceStatus(self):
        return self.deviceStatus

    def getDeviceType(self):
        return self.deviceType
