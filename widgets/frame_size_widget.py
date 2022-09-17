from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel

class FrameSizeWidget(QWidget):
    class FrameSizeSignals(QObject):
        frame_size_changed=Signal(int)

    def __init__(self) -> None:
        super().__init__()

        self.signals=FrameSizeWidget.FrameSizeSignals()

        title=QLabel('Frame size')
        validator = QIntValidator(5, 1000, self)
        self.frame_size=QLineEdit('20')
        self.frame_size.setValidator(validator)
        self.frame_size.textChanged.connect(self.onChanged)

        layout=QHBoxLayout()
        layout.addWidget(title)        
        layout.addWidget(self.frame_size)

        self.setLayout(layout)

        
    def onChanged(self, text):
        if len(text) > 0:
            self.signals.frame_size_changed.emit(int(text))