from PySide6.QtCore import Qt, Slot 
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QBarCategoryAxis, QValueAxis, QChart, QChartView

class ChartWidget(QWidget):
    def __init__(self, manager) -> None:
        super().__init__()

        self.manager=manager
        
        self.chart = QChart()

        chartView=QChartView(self.chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        layout=QHBoxLayout()
        layout.addWidget(chartView)

        self.setLayout(layout)

    def update(self, open_times, ohlc_list):
        series=QCandlestickSeries()
        series.setIncreasingColor(QColor(Qt.green))
        series.setDecreasingColor(QColor(Qt.red))
        for ohlc in ohlc_list:
            sets=QCandlestickSet(float(ohlc[0]), float(ohlc[1]), float(ohlc[2]), float(ohlc[3]), float(ohlc[4]))
            series.append(sets)
        self.chart.addSeries(series)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.createDefaultAxes()
        
        axisY = QValueAxis (self.chart.axes(Qt.Vertical)[0])
        axisY.setMax(axisY.max() * 1.01)
        axisY.setMin(axisY.min() * 0.99)

        axisX = QBarCategoryAxis (self.chart.axes(Qt.Horizontal)[0])
        axisX.setCategories(open_times)

    @Slot(str, str, str, str)
    def start_train(self, symbol, interval, start_time, end_time):
        klines=self.manager.get_futures_historical_klines(symbol, interval, start_time, end_time)
        open_times=[]
        ohlc=[]
        for kline in klines:
            open_times.append(kline[0])
            ohlc.append([kline[1], kline[2], kline[3], kline[4], kline[0]])
        self.update(open_times, ohlc)
