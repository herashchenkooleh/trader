from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel
from binance.client import Client


class IntervalWidget(QWidget):
    class IntervalWidgetSignals(QObject):
        selection_changes=Signal(str)        

    def __init__(self, default_interval) -> None:
        super().__init__()

        self.signals=IntervalWidget.IntervalWidgetSignals()

        self.intervals=QComboBox()
        self.intervals.addItem(Client.KLINE_INTERVAL_1MINUTE)
        self.intervals.addItem(Client.KLINE_INTERVAL_3MINUTE)
        self.intervals.addItem(Client.KLINE_INTERVAL_5MINUTE)
        self.intervals.addItem(Client.KLINE_INTERVAL_15MINUTE)
        self.intervals.addItem(Client.KLINE_INTERVAL_30MINUTE)
        self.intervals.addItem(Client.KLINE_INTERVAL_1HOUR)
        self.intervals.addItem(Client.KLINE_INTERVAL_2HOUR)
        self.intervals.addItem(Client.KLINE_INTERVAL_4HOUR)
        self.intervals.addItem(Client.KLINE_INTERVAL_6HOUR)
        self.intervals.addItem(Client.KLINE_INTERVAL_8HOUR)
        self.intervals.addItem(Client.KLINE_INTERVAL_12HOUR)
        self.intervals.addItem(Client.KLINE_INTERVAL_1DAY)
        self.intervals.addItem(Client.KLINE_INTERVAL_3DAY)
        self.intervals.addItem(Client.KLINE_INTERVAL_1WEEK)
        self.intervals.addItem(Client.KLINE_INTERVAL_1MONTH)
        self.intervals.currentIndexChanged.connect(self.selectionChanges)

        index = self.intervals.findText(default_interval, Qt.MatchFixedString)
        if index >= 0:
            self.intervals.setCurrentIndex(index)

        title=QLabel('Time interval')

        layout=QHBoxLayout()
        layout.addWidget(title)        
        layout.addWidget(self.intervals)

        self.setLayout(layout)

    def selectionChanges(self, index):
        self.signals.selection_changes.emit(self.intervals.currentText())
