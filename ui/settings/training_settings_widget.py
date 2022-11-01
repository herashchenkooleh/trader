from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ui.widgets.interval_widget import IntervalWidget
from ui.widgets.select_symbol_widget import SelectSymbolWidget  
from ui.widgets.time_widget import TimepickerWidget
from ui.widgets.frame_size_widget import FrameSizeWidget
from ui.widgets.chart_type_widget import ChartTypeWidget

class TrainingSettingsWidget(QWidget):
    class Signals(QObject):
        start_training_signal=Signal()

    def __init__(self, manager, settings) -> None:
        super().__init__()
        
        self.signals=TrainingSettingsWidget.Signals()
        self.settings=settings

        layout=QVBoxLayout()

        self.start_trainig_button=QPushButton("Start training")
        self.start_trainig_button.clicked.connect(self.on_start_training)

        self.symbol=SelectSymbolWidget(manager, self.settings.default_symbol)
        self.symbol.signals.selection_changes.connect(self.symbolChanges)

        self.chart_type=ChartTypeWidget()
        self.chart_type.signals.selection_changes.connect(self.chartTypeChanges)

        self.intervals=IntervalWidget(self.settings.default_interval)
        self.intervals.signals.selection_changes.connect(self.intervalChanges)

        self.start_time=TimepickerWidget('Start time', self.settings.default_start)
        self.start_time.signals.time_changes.connect(self.startTimeChanges)

        self.end_time=TimepickerWidget('End time', self.settings.default_end)
        self.end_time.signals.time_changes.connect(self.endTimeChanges)

        self.frame_size=FrameSizeWidget()
        self.frame_size.signals.frame_size_changed.connect(self.frameSizeChanged)

        layout.addWidget(self.symbol)
        layout.addWidget(self.chart_type)
        layout.addWidget(self.intervals)
        layout.addWidget(self.start_time)
        layout.addWidget(self.end_time)
        layout.addWidget(self.frame_size)
        layout.addWidget(self.start_trainig_button)

        layout.addStretch()

        self.setLayout(layout)

    @Slot()
    def on_start_training(self):
        self.enable(False)
        self.signals.start_training_signal.emit()

    @Slot(str)
    def symbolChanges(self, symbol):
        self.settings.set_symbol(symbol)

    @Slot(str)
    def chartTypeChanges(self, type):
        pass
        #self.settings.emit(type)

    @Slot(str)
    def intervalChanges(self, interval):
        self.settings.set_interval(interval)

    @Slot(str)
    def startTimeChanges(self, time):
        self.settings.set_start(time)

    @Slot(str)
    def endTimeChanges(self, time):
        self.settings.set_end(time)

    @Slot(int)
    def frameSizeChanged(self, size):
        #self.signals.frame_size_changed.emit(size)
        pass

    def enable(self, status):
        self.symbol.setEnabled(status)
        self.intervals.setEnabled(status)
        self.chart_type.setEnabled(status)
        self.start_time.setEnabled(status)
        self.end_time.setEnabled(status)
        self.frame_size.setEnabled(status)
        self.start_trainig_button.setEnabled(status)