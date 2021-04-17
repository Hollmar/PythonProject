class Udp:
    """ Provides methods for the udp functionality of the nRF52480 Dongle """
    def __init__(self, ipv6: bytes, port_tx: bytes, port_rx: bytes):
        """
        IPv6    | Scope      | Delivered to
        ff02::1 | Link-Local | All FTDs and MEDs
        ff02::2 | Link-Local | All FTDs and Border Routers
        ff03::1 | Mesh-Local | All FTDs and MEDs
        ff03::2 | Mesh-Local | All FTDs and Border Routers
        """
        # Transcieve port & address
        self.__ipaddr = ipv6
        self.__port_tx = port_tx
        # Recieve port
        self.__port_rx = port_rx

    def open(self, ser: object) -> None:
        """ Open udp port of nRF52840 Dongle """
        ser.write(b'udp open\n')

    def send_broadcast(self, ser: object, message: bytes) -> None:
        """
        Send message using standard ipv6 and port
        send <ip> <port> <message>
        """
        ser.write(b'udp send ' + self.__ipaddr + b' ' + self.__port_tx + b' ' + message)

    def send(self, ser: object, ipv6: bytes, port: bytes, message: bytes):
        """ """
        ser.write(b'upd send ' + ipv6 + b' ' + port + b' ' + message )

    def bind(self, ser: object) -> None:
        """ Bind upd port of nRF52840 Dongle """
        ser.write(b'udp bind :: ' + self.__port_rx + b'\n')
