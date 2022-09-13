from PySide6.QtWidgets import QMainWindow
from finance_widget import FinanceWidget
from trade_manager import TradeManager

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Trader')
        
        tmanager=TradeManager('btcusdt')
        finance=FinanceWidget(tmanager)

        self.setCentralWidget(finance)