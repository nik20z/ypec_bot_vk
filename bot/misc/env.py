from os import environ
from typing import Final


class Keys:
    VK_TOKEN: Final = environ.get('VK_TOKEN', '123456789')


class DataBase:
    SETTINGS: Final = environ.get('SETTINGS', {'user': "ypec",
                                               'password': "123456789",
                                               'host': "localhost",
                                               'port': 5432,
                                               'database': "ypec_bot"})
