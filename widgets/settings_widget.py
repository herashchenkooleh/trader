from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.interval_widget import IntervalWidget
from widgets.select_symbol_widget import SelectSymbolWidget
from widgets.start_train_widget import StartTrainWidget
from widgets.time_widget import TimepickerWidget
from widgets.frame_size_widget import FrameSizeWidget

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
        self.frame_size=20 #TODO init by default value from ?

        self.signals=SettingsWidget.SettingsWidgetSignals()

        symbol=SelectSymbolWidget(self.manager, self.current_symbol)
        symbol.signals.selection_changes.connect(self.symbolChanges)

        intervals=IntervalWidget(self.current_interval)
        intervals.signals.selection_changes.connect(self.intervalChanges)

        start_time=TimepickerWidget('Start time', self.current_start_time)
        start_time.signals.time_changes.connect(self.startTimeChanges)

        end_time=TimepickerWidget('End time', self.current_end_time)
        end_time.signals.time_changes.connect(self.endTimeChanges)

        frame_size=FrameSizeWidget()
        frame_size.signals.frame_size_changed.connect(self.frameSizeChanged)

        train=StartTrainWidget()
        train.signals.train_signal.connect(self.train)

        layout=QVBoxLayout()

        layout.addWidget(symbol)
        layout.addWidget(intervals)
        layout.addWidget(start_time)
        layout.addWidget(end_time)
        layout.addWidget(frame_size)
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

    @Slot(int)
    def frameSizeChanged(self, size):
        self.frame_size=size
        print(self.frame_size)

    @Slot()
    def train(self):
        start_time=self.current_start_time
        if not isinstance(start_time, str):
            start_time=self.current_start_time.toString('dd/MM/yyyy hh:mm')

        end_time=self.current_end_time
        if not isinstance(end_time, str):
            end_time=self.current_end_time.toString('dd/MM/yyyy hh:mm')

        self.signals.start_train.emit(self.current_symbol, self.current_interval, start_time, end_time)