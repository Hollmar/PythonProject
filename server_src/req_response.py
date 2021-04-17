class ReqResponse:
    """ Response to GUI request """
    def __init__(self) -> None:
        self.__rsp = b''

    def is_set(self) -> bool:
        """ Check if a response was set """
        is_set = False
        if self.__rsp != b'':
            is_set = True

        return is_set

    def get(self) -> bytes:
        """ Get response """
        return self.__rsp

    def set(self, rsp: bytes) -> None:
        """ Set the request response """
        self.__rsp = rsp

    def clear(self) -> None:
        """ Clear response """
        self.__rsp = b''

# Global variable
req_response = ReqResponse()
