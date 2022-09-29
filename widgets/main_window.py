from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from core.agent import Agent
from core.environment import Environment
from core.binance_manager import BinanceManager
from core.train_worker import TrainWorker
from core.settings import Settings

from widgets.mpl_canvas import MplCanvas
from widgets.settings_widget import SettingsWidget
from widgets.episode_end_widget import EpisodeEndWidget

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

        self.settings=Settings(self.binance_manager)
        self.env=Environment(self.binance_manager, self.settings)
        self.agent=Agent(self.env)

        self.agent.signals.on_episode_begin.connect(self.onEpisodeBegin)
        self.agent.signals.on_episode_end.connect(self.onEpisodeEnd)

        self.env.setAgent(self.agent)

        settings_widget=SettingsWidget(self.binance_manager)

        settings_widget.signals.char_type_changed.connect(self.onCharTypeChanged)
        settings_widget.signals.frame_size_changed.connect(self.onFrameSizeChanged)
        settings_widget.signals.interval_changed.connect(self.onIntervalChanged)
        settings_widget.signals.symbol_changed.connect(self.onSymbolChanged)
        settings_widget.signals.start_time_changed.connect(self.onStartTimeChanged)
        settings_widget.signals.end_time_changed.connect(self.onEndTimeChanged)
        settings_widget.signals.start_train.connect(self.startTrain)

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
        self.settings.settings.frame_size=size

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
        worker=TrainWorker(self.agent, self.settings)
        worker.start()

    @Slot()
    def onEpisodeBegin(self):
        pass

    @Slot()
    def onEpisodeEnd(self):
        widget=EpisodeEndWidget(self.env)
        widget.exec_()

    def updateChart(self, symbol, chart_type, interval, start_time, end_time):
        df=self.binance_manager.get_futures_historical_klines(symbol, interval, start_time, end_time)
        self.sc.updateChart(df, chart_type)