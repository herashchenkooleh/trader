from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.interval_widget import IntervalWidget
from widgets.select_symbol_widget import SelectSymbolWidget
from widgets.start_train_widget import StartTrainWidget
from widgets.time_widget import TimepickerWidget
from widgets.frame_size_widget import FrameSizeWidget
from widgets.chart_type_widget import ChartTypeWidget

class SettingsWidget(QWidget):
    class SettingsWidgetSignals(QObject):
        char_type_changed=Signal(str)
        frame_size_changed=Signal(int)
        interval_changed=Signal(str)
        symbol_changed=Signal(str)
        start_time_changed=Signal(str)
        end_time_changed=Signal(str)
        start_train=Signal()   

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

        chart_type=ChartTypeWidget()
        chart_type.signals.selection_changes.connect(self.chartTypeChanges)

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
        layout.addWidget(chart_type)
        layout.addWidget(intervals)
        layout.addWidget(start_time)
        layout.addWidget(end_time)
        layout.addWidget(frame_size)
        layout.addWidget(train)

        layout.addStretch()

        self.setLayout(layout)

    @Slot(str)
    def symbolChanges(self, symbol):
        self.signals.symbol_changed.emit(symbol)

    @Slot(str)
    def chartTypeChanges(self, type):
        self.signals.char_type_changed.emit(type)

    @Slot(str)
    def intervalChanges(self, interval):
        self.signals.interval_changed.emit(interval)

    @Slot(str)
    def startTimeChanges(self, time):
        self.signals.start_time_changed.emit(time)

    @Slot(str)
    def endTimeChanges(self, time):
        self.signals.end_time_changed.emit(time)

    @Slot(int)
    def frameSizeChanged(self, size):
        self.signals.frame_size_changed.emit(size)

    @Slot()
    def train(self):
        
        end_time=self.current_end_time
        if not isinstance(end_time, str):
            end_time=self.current_end_time.toString('dd/MM/yyyy hh:mm')

        self.signals.start_train.emit()