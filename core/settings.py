class Settings(object):
    def __init__(self, binance_manager) -> None:
        self.binance_manager=binance_manager
        self.reset()

    def reset(self):
        self.symbol=self.binance_manager.get_default_symbol()
        self.interval=self.binance_manager.get_default_interval()
        self.start_time=self.binance_manager.get_default_start_time().toString('dd/MM/yyyy hh:mm')
        self.end_time=self.binance_manager.get_default_end_time().toString('dd/MM/yyyy hh:mm')
        self.frame_size=20
        self.chart_type='Candlestick'
        self.epochs=50
