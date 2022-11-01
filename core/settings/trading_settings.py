class TradingSettings(object):
    def __init__(self) -> None:
        self.__private_symbol=""
        self.__private_interval=""
        self.__private_nn_model=""

    @property
    def symbol(self):
        return self.__private_symbol
    
    @property
    def interval(self):
        return self.__private_interval

    @property
    def nn_model(self):
        return self.__private_nn_model

    def set_symbol(self, symbol):
        self.__private_symbol = symbol
    
    def set_interval(self, interval):
        self.__private_interval = interval

    def set_nn_model(self, nn_model):
        self.__private_nn_model = nn_model