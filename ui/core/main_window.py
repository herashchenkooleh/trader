from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication,QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from core.settings.trading_settings import TradingSettings
from core.settings.training_settings import TrainingSetting
from core.brokers.binance_manager import BinanceManager
from core.nn.training_worker import TrainingWorker
from core.data.data_frame import DataFrame

from ui.core.mpl_canvas import MplCanvas
from ui.settings.settings_widget import SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.sc=MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.setEnabled(False)

        toolbar=NavigationToolbar2QT(self.sc, self)
        toolbar.setEnabled(False)

        layout=QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        widget=QWidget()
        widget.setLayout(layout)
        
        self.traiding_settings=TradingSettings()
        self.training_settings=TrainingSetting(QApplication.arguments()[1])

        self.manager=BinanceManager(QApplication.arguments()[1])
        settings_widget=SettingsWidget(self.traiding_settings, self.training_settings, self.manager)

        settings_widget.signals.start_training.connect(self.on_start_training)

        main_layout=QHBoxLayout()
        main_layout.addWidget(widget, stretch=3)
        main_layout.addWidget(settings_widget, stretch=1)

        main_widget=QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.show()

    @Slot()
    def on_start_training(self):
        worker=TrainingWorker(self.training_settings)
        worker.start()