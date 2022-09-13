from binance.client import Client

class BinanceManager(object):
    def __init__(self, symbol) -> None:
        self.api_key='D5EARRxdMgM4sCDciZH9in35QK3InzQ0KWOrsOqk5jZ2cA9fdyliCNCFeMoSNEKw'
        self.api_secret='qQej89ACfrmXPbFKXxUj3uvelf05N4tDreshFCNWQrvBss9rCH0XRr0YetIhkArr'
        self.symbol=symbol

        self.client=Client(self.api_key, self.api_secret)
        self.default_symbol='BTCUSDT'
        self.default_interval='15m'

    def getKLines(self, symbol, interval, start_time, end_time):
        return self.client.futures_historical_klines(symbol, interval, start_time, end_time)