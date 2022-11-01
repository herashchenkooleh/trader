from matplotlib.pyplot import scatter
import numpy as np        
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from mplfinance.original_flavor import candlestick2_ohlc as candlestick
import matplotlib.ticker as ticker
from datetime import datetime
from stocktrends import Renko

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.grid(True)
        super(MplCanvas, self).__init__(self.fig)

    def get_date(self, x, pos):
        try:
            return self.dates[int(x)]
        except KeyError:
            return ''

    def updateChart(self, data_frame):
        self.axes.clear()
        self.axes.grid(True)
        
        self.dates=data_frame.dates

        df=data_frame.data
        candlestick(self.axes, df.loc[:,'open'].values, df.loc[:, 'high'].values, df.loc[:, 'low'].values, df.loc[:, 'close'].values, width=1, colorup='g', colordown='r')

        self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.get_date))
        self.fig.autofmt_xdate()
        self.fig.tight_layout()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def updateScatter(self, env):
        self.axes.plot(env.actions_index, env.buy_price, '^', label="marker=buy")
        self.axes.plot(env.actions_index, env.sell_price, 'v', label="marker=sell")