class SocketConfig:
    def __init__(self, host, port, buffer_size):
        self.CONN = (host, port)
        self.BUFFER_SIZE = buffer_size