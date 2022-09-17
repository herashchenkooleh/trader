from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDateTimeEdit

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
