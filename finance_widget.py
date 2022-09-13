from typing import Container
from PySide6.QtWidgets import QWidget, QHBoxLayout

from chart_widget import ChartWidget
from settings_widget import SettingsWidget

class FinanceWidget(QWidget):
    def __init__(self, manager) -> None:
        super().__init__()

        layout=QHBoxLayout()

        chart=ChartWidget(manager)
        settings=SettingsWidget(manager)

        settings.signals.start_train.connect(chart.start_train)

        layout.addWidget(chart)
        layout.addWidget(settings)

        self.setLayout(layout)