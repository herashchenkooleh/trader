from PySide6.QtCore import QDateTime
from binance.client import Client
from dateutil.relativedelta import relativedelta

import configparser

class BinanceManager(object):
    def __init__(self, config_file) -> None:
        parser=configparser.ConfigParser()
        parser.read(config_file)

        try:
            self.api_key=parser.get('Binance', 'api_key')
        except configparser.NoOptionError:
            pass #TODO

        try:
            self.api_secret=parser.get('Binance', 'api_secret')
        except configparser.NoOptionError:
            pass #TODO

        self.client=Client(self.api_key, self.api_secret) #TODO select test net in UI
        self.default_symbol='BTCUSDT'
        self.default_interval='1d'

    def get_symbols_list(self):
        symbols=[]

        for symbol in self.client.get_exchange_info()['symbols']:
            if symbol['status'] == 'TRADING':
                symbols.append(symbol['symbol'])
        symbols.sort()

        return symbols

    def get_futures_historical_klines(self, symbol, interval, start_time, end_time):
        return self.client.futures_historical_klines(symbol, interval, start_time, end_time)