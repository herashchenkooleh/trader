from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from mpl_canvas import MplCanvas
from trading.binance_manager import BinanceManager

from widgets.settings_widget import SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc=MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        toolbar=NavigationToolbar2QT(sc, self)

        layout=QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        widget=QWidget()
        widget.setLayout(layout)
        
        binance_manager=BinanceManager()
        settings=SettingsWidget(binance_manager)

        main_layout=QHBoxLayout()
        main_layout.addWidget(widget)
        main_layout.addWidget(settings)

        main_widget=QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.show()