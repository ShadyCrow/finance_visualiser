from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QFrame
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtGui import QPainter, QMouseEvent, QPen
import numpy as np

class CustomChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setMouseTracking(True)
        self.chart = chart
        self.hover_coordinate_label = None

    def set_hover_coordinate_label(self, label: QLabel):
        """Sets a QLabel to display the hovered coordinates."""
        self.hover_coordinate_label = label

    def mouseMoveEvent(self, event: QMouseEvent):

        view_position = event.pos()
        
        scene_position = self.mapToScene(view_position)

        chart_item_position = self.chart.mapFromScene(scene_position)
        
        value_coordinate = self.chart.mapToValue(chart_item_position)
        
        if self.hover_coordinate_label:
            self.hover_coordinate_label.setText(f"X: {value_coordinate.x():.2f}, Y: {value_coordinate.y():.2f}")
        
    def leaveEvent(self, event):
        if self.hover_coordinate_label:
            self.hover_coordinate_label.setText("")
        return super().leaveEvent(event)


class GraphWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the vertical layout for the graph widget.
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        # Create the chart and chart view.
        self.graph = QChart()
        self.graph.setTitle("Investment Growth Over Time")
        self.graph.setAnimationOptions(QChart.SeriesAnimations)
        self.graph.setTheme(QChart.ChartThemeDark)
        
        
        # Create the chart view to display the graph.
        self.graph_view = CustomChartView(self.graph)
        # self.graph_view.setRenderHint(QPainter.Antialiasing)
        self.graph_view.setMinimumSize(800, 600)
        layout.addWidget(self.graph_view)
        
        # Set the style of the graph widget.
        self.setStyleSheet("background-color: lightgray;")
        
        # Create a label to display data.
        self.coordinate_label = QLabel("Mouse Coordinates:")
        self.coordinate_label.setAlignment(Qt.AlignCenter)
        self.graph_view.set_hover_coordinate_label(self.coordinate_label)

        # Set the alignment and word wrap for the label.
        self.coordinate_label.setWordWrap(True)
        
        layout.addWidget(self.coordinate_label)

    @Slot(str, str, int, float)
    def update_graph_data(self, starting_amount, growth_rate, investment_period, investment_per_year):
        # self.data_display_label.setText(f"Graph Widget: {starting_amount}, {growth_rate}, {investment_period} - Data updated successfully.")

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

        # self.data_display_label.setText(f"Graph Widget: {starting_amount}, {growth_rate}, {investment_period}, {investment_per_year} - Data updated successfully.")