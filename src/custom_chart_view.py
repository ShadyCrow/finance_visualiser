
from PySide6.QtCharts import QChartView, QLineSeries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QPointF

class CustomChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setMouseTracking(True)
        self.chart = chart
        self.hover_coordinate_label = None
        self.series_label = None

    def set_hover_coordinate_label(self, label: QLabel):
        """Sets a QLabel to display the hovered coordinates."""
        self.hover_coordinate_label = label
        
    def set_series_label(self, label_2: QLabel):
        """Sets a QLabel to display the series coordinate."""
        self.series_label = label_2

    def mouseMoveEvent(self, event: QMouseEvent):

        view_position = event.pos()
        
        scene_position = self.mapToScene(view_position)

        chart_item_position = self.chart.mapFromScene(scene_position)
        
        value_coordinate = self.chart.mapToValue(chart_item_position)
        
        if self.hover_coordinate_label:
            self.hover_coordinate_label.setText(f"X: {value_coordinate.x():.2f}, Y: {value_coordinate.y():.2f}")
            
        if self.series_label and value_coordinate.y() >= 0 and value_coordinate.x() >= 0:
            self.series_label.setText(f"X: {value_coordinate.x():.2f} years, Y: ${self.calculate_nearest_y_value(value_coordinate):.2f}")
        elif self.series_label:
            self.series_label.setText("")

    def leaveEvent(self, event):
        if self.hover_coordinate_label:
            self.hover_coordinate_label.setText("")

        if self.series_label:
            self.series_label.setText("")

        return super().leaveEvent(event)
    
    def calculate_nearest_y_value(self, value_coordinate):
        """Calculates the nearest y value to the given point."""
        

        point_values = self.chart.series.points().y()

        nearest_y = 0
        
        for point in point_values:
            current_difference = abs(value_coordinate.y() - point)
            if current_difference < abs(value_coordinate.y() - nearest_y):
                nearest_y = point

        return nearest_y
    