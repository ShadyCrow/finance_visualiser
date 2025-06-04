from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtCharts import QChart, QLineSeries, QChartView
from custom_chart_view import CustomChartView
from PySide6.QtGui import QAction, QPainter, QKeySequence

import numpy as np




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
        self.graph_view.setRenderHint(QPainter.Antialiasing)
        self.graph_view.setMinimumSize(800, 600)
        self.graph_view.setRubberBand(CustomChartView.RectangleRubberBand)
        layout.addWidget(self.graph_view)
        
        # Set the style of the graph widget.
        self.setStyleSheet("background-color: lightgray;")
        
        
        reset_action = QAction("Reset Graph", self)
        reset_action.setShortcut("Ctrl+R")
        reset_action.triggered.connect(self.graph.zoomReset)
        self.addAction(reset_action)
        
        # Create a label to display data.
        self.coordinate_label = QLabel("Mouse Coordinates:")
        self.coordinate_label.setAlignment(Qt.AlignCenter)
        self.graph_view.set_hover_coordinate_label(self.coordinate_label)
        
        # Create a label to display the series name and value.
        self.series_label = QLabel("Series Information:")
        self.series_label.setAlignment(Qt.AlignCenter)
        self.graph_view.set_series_label(self.series_label)

        # Set the alignment and word wrap for the label.
        self.coordinate_label.setWordWrap(True)
        self.series_label.setWordWrap(True) 
        
        layout.addWidget(self.coordinate_label)
        layout.addWidget(self.series_label)

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
        
        print(f"{type(self.series)}")
        print(f"Series Points: {self.series.points()}") 
        print(f"Series Points Count: {self.series.count()}")
        
        # Set tooltip for the series
        self.series.setPointsVisible(True)
        self.series.setPointLabelsVisible(False)
        
        self.graph.addSeries(self.series)
        self.graph.createDefaultAxes()

        # self.data_display_label.setText(f"Graph Widget: {starting_amount}, {growth_rate}, {investment_period}, {investment_per_year} - Data updated successfully.")