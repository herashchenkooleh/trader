from PySide6.QtCore import QDateTime
from binance.client import Client
from dateutil.relativedelta import relativedelta

class TradeManager(object):
    def __init__(self, symbol) -> None:
        self.api_key='D5EARRxdMgM4sCDciZH9in35QK3InzQ0KWOrsOqk5jZ2cA9fdyliCNCFeMoSNEKw'
        self.api_secret='qQej89ACfrmXPbFKXxUj3uvelf05N4tDreshFCNWQrvBss9rCH0XRr0YetIhkArr'
        self.symbol=symbol

        self.client=Client(self.api_key, self.api_secret)
        self.default_symbol='BTCUSDT'
        self.default_interval='15m'

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
        try:
            return self.client.futures_historical_klines(symbol, interval, start_time, end_time)
        except Exception as e:
            print(e)