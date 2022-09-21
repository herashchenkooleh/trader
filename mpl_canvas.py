import numpy as np        
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from mplfinance.original_flavor import candlestick2_ohlc as candlestick
import matplotlib.ticker as ticker
from datetime import datetime

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

    def updateCandlesticks(self, df):
        print(len(df))
        df=pd.DataFrame(df)
        df=df.reset_index(drop=True)
        df.columns=['date', 'open', 'high', 'low', 'close', 'volume', '1', '2', '3', '4', '5', '6']
        ohlc=df.loc[: , ['date', 'open', 'high', 'low', 'close']]
        ohlc=ohlc.astype(np.float)
        self.dates=ohlc['date'].apply(lambda x: datetime.fromtimestamp(float(x) / 1000.0))
        print(self.dates)
        candlestick(self.axes, ohlc.loc[:,'open'].values, ohlc.loc[:, 'high'].values, ohlc.loc[:, 'low'].values, ohlc.loc[:, 'close'].values, width=0.5, colorup='g', colordown='r')            
        self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.get_date))
        self.fig.autofmt_xdate()
        self.fig.tight_layout()

        self.fig.canvas.draw()