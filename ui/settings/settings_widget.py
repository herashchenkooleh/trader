from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QTabWidget

from ui.settings.trading_settings_widget import TradingSettingsWidget
from ui.settings.training_settings_widget import TrainingSettingsWidget

class SettingsWidget(QTabWidget):
    class Signals(QObject):
        start_trainig=Signal()
        start_traiding=Signal()
        stop_traiding=Signal()

    def __init__(self, traiding_settings, training_settings, manager) -> None:
        super().__init__()

        self.traiding_settings=traiding_settings
        self.training_settings=training_settings

        self.signals=SettingsWidget.Signals()

        self.traiding_widget=TradingSettingsWidget()
        self.addTab(self.traiding_widget, "Trading Settings")

        self.traiding_widget.signals.start_trading_signal.connect(self.on_start_traiding)
        self.traiding_widget.signals.stop_trading_signal.connect(self.on_stop_traiding)
        
        self.training_widget=TrainingSettingsWidget(manager, self.training_settings)
        self.addTab(self.training_widget, "Training Settings")

        self.training_widget.signals.start_training_signal.connect(self.on_start_training)

    @Slot()
    def on_start_training(self):
        self.traiding_widget.enable(False)
        self.signals.start_trainig.emit()

    @Slot()
    def on_start_traiding(self):
        self.training_widget.enable(False)
        self.signals.start_traiding.emit()

    @Slot()
    def on_stop_traiding(self):
        self.training_widget.enable(True)
        self.signals.stop_traiding.emit()