import configparser
from PySide6.QtCore import QDateTime

class TrainingSetting(object):
    def __init__(self, config_file) -> None:
        parser=configparser.ConfigParser()
        parser.read(config_file)

        try:
            self.__private_default_symbol=parser.get('TrainingSection', 'default_symbol')
        except configparser.NoOptionError:
            self.__private_default_symbol='BTCUSDT'

        try:
            self.__private_default_interval=parser.get('TrainingSection', 'default_interval')
        except configparser.NoOptionError:
            self.__private_default_interval='1d'

        try:
            self.__private_default_start=parser.get('TrainingSection', 'default_start')
        except configparser.NoOptionError:
            self.__private_default_start=QDateTime.currentDateTime()

        try:
            self.__private_default_end=parser.get('TrainingSection', 'default_end')
        except configparser.NoOptionError:
            self.__private_default_end=QDateTime.currentDateTime().addYears(-1)

        self.__private_symbol=""
        self.__private_interval=""
        self.__private_nn_model=""
        self.__private_start=""
        self.__private_end=""

    @property
    def default_symbol(self):
        return self.__private_default_symbol

    @property
    def default_interval(self):
        return self.__private_default_interval

    @property
    def default_start(self):
        return self.__private_default_start

    @property
    def default_end(self):
        return self.__private_default_end

    @property
    def symbol(self):
        return self.__private_symbol
    
    @property
    def interval(self):
        return self.__private_interval

    @property
    def nn_model(self):
        return self.__private_nn_model

    @property
    def start(self):
        return self.__private_start

    @property
    def end(self):
        return self.__private_end

    def set_symbol(self, symbol):
        self.__private_symbol = symbol
    
    def set_interval(self, interval):
        self.__private_interval = interval

    def set_nn_model(self, nn_model):
        self.__private_nn_model = nn_model

    def set_start(self, start):
        self.__private_start=start

    def set_end(self, end):
        self.__private_end=end