class Base:
    def __init__(self):
        self.__config = {}

    def get_config(self, key: str):
        return self.__config.get(key, '')

