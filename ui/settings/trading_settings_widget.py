from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class TradingSettingsWidget(QWidget):
    class Signals(QObject):
        start_trading_signal=Signal()
        stop_trading_signal=Signal()

    def __init__(self) -> None:
        super().__init__()

        self.signals=TradingSettingsWidget.Signals()

        layout=QHBoxLayout()

        self.start_trainig_button=QPushButton("Start trading")
        self.start_trainig_button.clicked.connect(self.on_start_trading)

        self.stop_trainig_button=QPushButton("Sop trading")
        self.stop_trainig_button.clicked.connect(self.on_stop_trading)
        self.stop_trainig_button.setEnabled(False)

        layout.addWidget(self.start_trainig_button)
        layout.addWidget(self.stop_trainig_button)

        main_layout=QVBoxLayout()
        main_layout.addLayout(layout)

        main_layout.addStretch()

        self.setLayout(main_layout)

    @Slot()
    def on_start_trading(self):
        self.stop_trainig_button.setEnabled(True)
        self.start_trainig_button.setEnabled(False)
        self.signals.start_trading_signal.emit()

    @Slot()
    def on_stop_trading(self):
        self.stop_trainig_button.setEnabled(False)
        self.start_trainig_button.setEnabled(True)
        self.signals.stop_trading_signal.emit()

    def enable(self, status):
        self.start_trainig_button.setEnabled(status)
        self.stop_trainig_button.setEnabled(status)