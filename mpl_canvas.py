from dataclasses import replace
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

    def updateChart(self, df, chart_type):
        if chart_type == 'Candlestick':
            self.updateCandlestick(df)
        elif chart_type == 'Renko':
            self.updateRenko(df)

    def df_to_renko(self, data, number):
        data =pd.DataFrame(data)
        data.reset_index(inplace=True)
        data.columns=['date', 'open', 'high', 'low', 'close', 'volume', '1', '2', '3', '4', '5', '6', '7']
        data=data.loc[: , ['date', 'open', 'high', 'low', 'close']]
        data=data.astype(np.float)
        df=Renko(data)
        df.brick_size=number
        renko_df=df.get_ohlc_data()
    
        return renko_df

    def updateRenko(self, df):
        self.axes.clear()        
        self.axes.grid(True)
        self.renko_number=500    
        renko_df=self.df_to_renko(df, self.renko_number)
        candlestick(self.axes, renko_df.loc[:,'open'].values, renko_df.loc[:, 'high'].values, renko_df.loc[:, 'low'].values, renko_df.loc[:, 'close'].values, width=1, colorup='g', colordown='r')            
        self.fig.autofmt_xdate()
        self.fig.tight_layout()

        self.fig.canvas.draw()

    def updateCandlestick(self, df):
        self.axes.clear()
        self.axes.grid(True)
        df=pd.DataFrame(df)
        df=df.reset_index(drop=True)
        df.columns=['date', 'open', 'high', 'low', 'close', 'volume', '1', '2', '3', '4', '5', '6']
        ohlc=df.loc[: , ['date', 'open', 'high', 'low', 'close']]
        ohlc=ohlc.astype(np.float)
        self.dates=ohlc['date'].apply(lambda x: datetime.fromtimestamp(float(x) / 1000.0))
        candlestick(self.axes, ohlc.loc[:,'open'].values, ohlc.loc[:, 'high'].values, ohlc.loc[:, 'low'].values, ohlc.loc[:, 'close'].values, width=0.5, colorup='g', colordown='r')            
        self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.get_date))
        self.fig.autofmt_xdate()
        self.fig.tight_layout()

        self.fig.canvas.draw()