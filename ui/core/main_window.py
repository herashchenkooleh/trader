from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication,QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from core.settings.trading_settings import TradingSettings
from core.settings.training_settings import TrainingSetting
from core.trading.binance_manager import BinanceManager

from ui.core.mpl_canvas import MplCanvas
from ui.settings.settings_widget import SettingsWidget

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
        
        self.traiding_settings=TradingSettings()
        self.training_settings=TrainingSetting(QApplication.arguments()[1])

        self.manager=BinanceManager(QApplication.arguments()[1])
        settings_widget=SettingsWidget(self.traiding_settings, self.training_settings, self.manager)

        main_layout=QHBoxLayout()
        main_layout.addWidget(widget, stretch=3)
        main_layout.addWidget(settings_widget, stretch=1)

        main_widget=QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.show()

    @Slot(str)
    def onCharTypeChanged(self, type):
        self.settings.chart_type=type

    @Slot(int)
    def onFrameSizeChanged(self, size):
        self.settings.frame_size=size
        self.env.update()

    @Slot(str)
    def onIntervalChanged(self, interval):
        self.settings.interval=interval

    @Slot(str)
    def onSymbolChanged(self, symbol):
        self.settings.symbol=symbol

    @Slot(str)    
    def onStartTimeChanged(self, time):
        self.settings.start_time=time
        if not isinstance(self.settings.start_time, str):
            self.settings.start_time=self.settings.start_time.toString('dd/MM/yyyy hh:mm')
    
    @Slot(str)
    def onEndTimeChanged(self, time):
        self.settings.end_time=time
        if not isinstance(self.settings.end_time, str):
            self.settings.end_time=self.settings.end_time.toString('dd/MM/yyyy hh:mm')

    @Slot()
    def startTrain(self):
        self.sc.updateChart(self.env)
        worker=TrainWorker(self.agent, self.settings)
        worker.start()

    @Slot()
    def onEpisodeBegin(self):
        pass

    @Slot()
    def onEpisodeEnd(self):
        widget=EpisodeEndWidget(self.env, self.settings)
        widget.exec_()
        pass