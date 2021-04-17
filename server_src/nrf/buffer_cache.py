class Cache:
    """ Cache for saving data sent by child-devices """
    def __init__(self):
        self.__cache: list = []

    def write_cache(self, data: bytes) -> None:
        self.__cache.append( data )

    def get_cache(self) -> list:
        cache = self.__cache.copy()
        self.__cache.clear()
        return cache
