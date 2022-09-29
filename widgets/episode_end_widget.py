from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QVBoxLayout

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT

from widgets.mpl_canvas import MplCanvas

class EpisodeEndWidget(QDialog):
    def __init__(self, env) -> None:
        super().__init__()
        self.env=env

        self.sc=MplCanvas(self, width=5, height=4, dpi=100)

        toolbar=NavigationToolbar2QT(self.sc, self)

        layout=QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        self.setLayout(layout)

        #self.sc.updateChart(self.env.getData('BTCUSDR', '1d', ''), "Renko")