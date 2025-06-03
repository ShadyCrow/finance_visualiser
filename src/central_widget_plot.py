from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, Signal, Slot, QPointF
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPainter
import numpy as np

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        self.graph = QChart()
        self.graph.setTitle("Investment Growth Over Time")
        self.graph.setAnimationOptions(QChart.SeriesAnimations)
        self.graph.setBackgroundBrush(Qt.lightGray)
        
        self.graph_view = QChartView(self.graph)
        self.graph_view.setRenderHint(QPainter.Antialiasing)
        self.graph_view.setMinimumSize(800, 600)
        layout.addWidget(self.graph_view)
        
        
        self.setStyleSheet("background-color: lightgray;")
        self.data_display_label = QLabel("No data available to display.")

        self.data_display_label.setWordWrap(True)
        layout.addWidget(self.data_display_label)
    
    @Slot(str, str, int, float)
    def update_graph_data(self, starting_amount, growth_rate, investment_period, investment_per_year):
        self.data_display_label.setText(f"Graph Widget: {starting_amount}, {growth_rate}, {investment_period} - Data updated successfully.")

        self.series = QLineSeries()

        starting_amount = float(starting_amount)
        growth_rate = float(growth_rate)/100

        x_values = np.arange(0, investment_period + 1)
        total = starting_amount
        y_values = [starting_amount]
         
        for year in range(1, investment_period + 1):
             total *= (1 + growth_rate)
             total += investment_per_year
             y_values.append(total)
 
        # y_values = starting_amount*(1 + growth_rate)**x_values
        
        self.series.clear()
        points = [QPointF(x, y) for x, y in zip(x_values, y_values)]
        self.series.append(points)
        self.graph.addSeries(self.series)
        self.graph.createDefaultAxes()

        self.data_display_label.setText(f"Graph Widget: {starting_amount}, {growth_rate}, {investment_period}, {investment_per_year} - Data updated successfully.")