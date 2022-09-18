import numpy as np        
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.dates import DateFormatter, epoch2num
from mplfinance.original_flavor import candlestick_ohlc as candlestick

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.xaxis.set_major_formatter(DateFormatter('%Y-%m-%D %H:%M'))
        self.axes.grid(True)
        super(MplCanvas, self).__init__(self.fig)

    def updateCandlesticks(self, df):
        df=pd.DataFrame(df)
        df=df.reset_index(drop=True)
        df.columns=['date', 'open', 'high', 'low', 'close', 'volume', '1', '2', '3', '4', '5', '6']
        df['date']=epoch2num(df['date'] / 1000.0)
        df=df.drop(columns=['1', '2', '3', '4', '5', '6'])
        df['open']=df['open'].astype(np.float)
        df['high']=df['high'].astype(np.float)
        df['low']=df['low'].astype(np.float)
        df['close']=df['close'].astype(np.float)
        df['volume']=df['close'].astype(np.float)
        ohlc=np.asarray(df.loc[:, ['date', 'open', 'high', 'low', 'close']])
        candlestick(self.axes, ohlc, width=0.6, colorup='g', colordown='r')

        self.fig.canvas.draw()