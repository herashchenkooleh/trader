from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from mpl_canvas import MplCanvas
from trading.binance_manager import BinanceManager

from widgets.settings_widget import SettingsWidget

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
        settings.signals.start_train.connect(self.startTrain)

        main_layout=QHBoxLayout()
        main_layout.addWidget(widget)
        main_layout.addWidget(settings)

        main_widget=QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.show()

    @Slot(str, str, str, str, int)
    def startTrain(self, symbol, interval, start_time, end_time, frame_size):
        self.updateChart(symbol, interval, start_time, end_time)

    def updateChart(self, symbol, interval, start_time, end_time):
        df=self.binance_manager.get_futures_historical_klines(symbol, interval, start_time, end_time)
        self.sc.updateCandlesticks(df)