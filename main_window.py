from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from mpl_canvas import MplCanvas
from trading.binance_manager import BinanceManager
from widgets.settings_widget import SettingsWidget

from train_worker import TrainWorker

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.sc=MplCanvas(self, width=5, height=4, dpi=100)

        toolbar=NavigationToolbar2QT(self.sc, self)

        layout=QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        widget=QWidget()
        widget.setLayout(layout)
        
        self.binance_manager=BinanceManager()
        settings=SettingsWidget(self.binance_manager)

        self.symbol=self.binance_manager.get_default_symbol()
        self.interval=self.binance_manager.get_default_interval()
        self.start_time=self.binance_manager.get_default_start_time().toString('dd/MM/yyyy hh:mm')
        self.end_time=self.binance_manager.get_default_end_time().toString('dd/MM/yyyy hh:mm')
        self.frame_size=20 #TODO init by default value from ?
        self.chart_type='Candlestick'

        settings.signals.char_type_changed.connect(self.onCharTypeChanged)
        settings.signals.frame_size_changed.connect(self.onFrameSizeChanged)
        settings.signals.interval_changed.connect(self.onIntervalChanged)
        settings.signals.symbol_changed.connect(self.onSymbolChanged)
        settings.signals.start_time_changed.connect(self.onStartTimeChanged)
        settings.signals.end_time_changed.connect(self.onEndTimeChanged)
        settings.signals.start_train.connect(self.startTrain)

        main_layout=QHBoxLayout()
        main_layout.addWidget(widget, stretch=3)
        main_layout.addWidget(settings, stretch=1)

        main_widget=QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.show()

    @Slot(str)
    def onCharTypeChanged(self, type):
        self.chart_type=type

    @Slot(int)
    def onFrameSizeChanged(self, size):
        self.frame_size=size

    @Slot(str)
    def onIntervalChanged(self, interval):
        self.interval=interval

    @Slot(str)
    def onSymbolChanged(self, symbol):
        self.symbol=symbol

    @Slot(str)    
    def onStartTimeChanged(self, time):
        self.start_time=time
        if not isinstance(self.start_time, str):
            self.start_time=self.start_time.toString('dd/MM/yyyy hh:mm')
    
    @Slot(str)
    def onEndTimeChanged(self, time):
        self.end_time=time
        if not isinstance(self.end_time, str):
            self.end_time=self.end_time.toString('dd/MM/yyyy hh:mm')

    @Slot()
    def startTrain(self):
        self.updateChart(self.symbol, self.chart_type, self.interval, self.start_time, self.end_time)
    
        worker=TrainWorker(self.binance_manager, self.frame_size, self.symbol, self.interval, self.start_time, self.end_time)

    def updateChart(self, symbol, chart_type, interval, start_time, end_time):
        df=self.binance_manager.get_futures_historical_klines(symbol, interval, start_time, end_time)
        self.sc.updateChart(df, chart_type)