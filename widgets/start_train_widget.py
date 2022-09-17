from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

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