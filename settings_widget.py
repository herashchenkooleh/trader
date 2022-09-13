from PySide6.QtCore import QObject, Signal, Slot, QDateTime, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QDateTimeEdit, QPushButton
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

class TimepickerWidget(QWidget):
    class TimepickerWidgetSignals(QObject):
        time_changes=Signal(str)

    def __init__(self, title, default_time) -> None:
        super().__init__()

        self.signals=TimepickerWidget.TimepickerWidgetSignals()

        title=QLabel(title)

        self.date_time=QDateTimeEdit()
        self.date_time.setDisplayFormat('dd/MM/yyyy hh:mm')
        self.date_time.setDateTime(default_time)
        self.date_time.dateTimeChanged.connect(self.timeChanges)

        layout=QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.date_time)

        self.setLayout(layout)

    def timeChanges(self):
        dt=self.date_time.dateTime()
        dt_string=dt.toString(self.date_time.displayFormat())
        self.signals.time_changes.emit(dt_string)

class StartTrainWidget(QWidget):
    class StartTrainWidgetSignals(QObject):
        train_signal=Signal()

    def __init__(self) -> None:
        super().__init__()

        self.signals=StartTrainWidget.StartTrainWidgetSignals()

        train=QPushButton('Train')
        train.clicked.connect(self.train_clicked)

        layout=QHBoxLayout()
        layout.addWidget(train)

        self.setLayout(layout)

    def train_clicked(self):
        self.signals.train_signal.emit()

class SelectSymbolWidget(QWidget):
    class SelectSymbolWidgetSignals(QObject):
        selection_changes=Signal(str)        

    def __init__(self, manager, default_symbol) -> None:
        super().__init__()

        self.signals=SelectSymbolWidget.SelectSymbolWidgetSignals()

        self.symbols=QComboBox()

        for symbol in manager.get_symbols_list():
            self.symbols.addItem(symbol)

        index = self.symbols.findText(default_symbol, Qt.MatchFixedString)
        if index >= 0:
            self.symbols.setCurrentIndex(index)

        self.symbols.currentIndexChanged.connect(self.selectionChanges)

        title=QLabel('Symbol')

        layout=QHBoxLayout()
        layout.addWidget(title)        
        layout.addWidget(self.symbols)

        self.setLayout(layout)

    def selectionChanges(self, index):
        self.signals.selection_changes.emit(self.symbols.currentText())

class SettingsWidget(QWidget):
    class SettingsWidgetSignals(QObject):
        start_train=Signal(str, str, str, str)   

    def __init__(self, manager) -> None:
        super().__init__()

        self.manager=manager

        self.current_symbol=self.manager.get_default_symbol()
        self.current_interval=self.manager.get_default_interval()
        self.current_start_time=self.manager.get_default_start_time()
        self.current_end_time=self.manager.get_default_end_time()

        self.signals=SettingsWidget.SettingsWidgetSignals()

        symbol=SelectSymbolWidget(self.manager, self.current_symbol)
        symbol.signals.selection_changes.connect(self.symbolChanges)

        intervals=IntervalWidget(self.current_interval)
        intervals.signals.selection_changes.connect(self.intervalChanges)

        start_time=TimepickerWidget('Start time', self.current_start_time)
        start_time.signals.time_changes.connect(self.startTimeChanges)

        end_time=TimepickerWidget('End time', self.current_end_time)
        end_time.signals.time_changes.connect(self.endTimeChanges)

        train=StartTrainWidget()
        train.signals.train_signal.connect(self.train)

        layout=QVBoxLayout()

        layout.addWidget(symbol)
        layout.addWidget(intervals)
        layout.addWidget(start_time)
        layout.addWidget(end_time)
        layout.addWidget(train)

        layout.addStretch()

        self.setLayout(layout)

    @Slot(str)
    def symbolChanges(self, symbol):
        self.current_symbol=symbol

    @Slot(str)
    def intervalChanges(self, interval):
        self.current_interval=interval

    @Slot(str)
    def startTimeChanges(self, time):
        self.current_start_time=time

    @Slot(str)
    def endTimeChanges(self, time):
        self.current_end_time=time

    @Slot()
    def train(self):
        start_time=self.current_start_time
        if not isinstance(start_time, str):
            start_time=self.current_start_time.toString('dd/MM/yyyy hh:mm')

        end_time=self.current_end_time
        if not isinstance(end_time, str):
            end_time=self.current_end_time.toString('dd/MM/yyyy hh:mm')

        self.signals.start_train.emit(self.current_symbol, self.current_interval, start_time, end_time)