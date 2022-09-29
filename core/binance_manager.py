from PySide6.QtCore import QDateTime
from binance.client import Client
from dateutil.relativedelta import relativedelta

class BinanceManager(object):
    def __init__(self) -> None:
        self.api_key='jhG8KfWiueDCrmG96719XmPtjTBjkisnZrWIpKppdxe8VD7JLgF4OEfrrxIRJmLI'
        self.api_secret='ZYkxRqYzvB3RIHCVWB1ujfjjRT76E1uwkOKyNwtavlpLf8c5g5NpK24c66cyc0pj'

        self.client=Client(self.api_key, self.api_secret, testnet=True) #TODO select test net in UI
        self.default_symbol='BTCUSDT'
        self.default_interval='1d'

    def get_default_symbol(self):
        if self.client.get_symbol_info(self.default_symbol)['status']=='TRADING':
            return self.default_symbol

        return None

    def get_default_interval(self):
        return self.default_interval

    def get_default_start_time(self):
        return QDateTime.currentDateTime().addYears(-1)

    def get_default_end_time(self):
        return QDateTime.currentDateTime()

    def get_symbols_list(self):
        symbols=[]

        for symbol in self.client.get_exchange_info()['symbols']:
            if symbol['status'] == 'TRADING':
                symbols.append(symbol['symbol'])
        symbols.sort()

        return symbols

    def get_futures_historical_klines(self, symbol, interval, start_time, end_time):
        return self.client.futures_historical_klines(symbol, interval, start_time, end_time)