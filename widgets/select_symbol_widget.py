from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel

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
