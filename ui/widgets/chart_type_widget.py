from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel

class ChartTypeWidget(QWidget):
    class ChartTypeWidgetSignals(QObject):
        selection_changes=Signal(str)        

    def __init__(self) -> None:
        super().__init__()

        self.signals=ChartTypeWidget.ChartTypeWidgetSignals()

        self.chart_type=QComboBox()

        self.chart_type.addItem('Candlestick')
        self.chart_type.addItem('Renko')

        self.chart_type.currentIndexChanged.connect(self.selectionChanges)

        title=QLabel('Chart type')

        layout=QHBoxLayout()
        layout.addWidget(title)        
        layout.addWidget(self.chart_type)

        self.setLayout(layout)

    def selectionChanges(self, index):
        self.signals.selection_changes.emit(self.chart_type.currentText())
