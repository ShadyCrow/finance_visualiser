from PySide6.QtCharts import QChartView, QLineSeries, QXYSeries
from PySide6.QtGui import QMouseEvent, QPen, QColor
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QPointF, Qt

class CustomChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setMouseTracking(True)
        self.chart = chart
        self.hover_coordinate_label = None
        self.series_label = None
        
        self.highlighted_point = None
        self.original_point_size = 2
        self.highlighted_point_size = 8

    def set_hover_coordinate_label(self, label: QLabel):
        """Sets a QLabel to display the hovered coordinates."""
        self.hover_coordinate_label = label
        
    def set_series_label(self, label_2: QLabel):
        """Sets a QLabel to display the series coordinate."""
        self.series_label = label_2

    def mouseMoveEvent(self, event: QMouseEvent):

        # Obtains the position of the mouse in the view, which is in terms of pixels.
        view_position = event.pos()

        # Maps the view position to the scene position of the chart view, which is in terms of the chart view's coordinate system.
        # This is necessary because the chart is in a different coordinate system.
        scene_position = self.mapToScene(view_position)

        # Maps the scene position to the chart item position, which is in terms of the chart's coordinate system.
        # This is necessary to get the actual data point in the chart.
        chart_item_position = self.chart.mapFromScene(scene_position)

        # Maps the chart item position to the value coordinate, which converts the chart item position to the actual data point in the chart.
        # The value coordinate is a QPointF object that contains the x and y values of the data point.
        value_coordinate = self.chart.mapToValue(chart_item_position)

        # Provides the x and y coordinates of the mouse position in the chart's coordinate system.
        if self.hover_coordinate_label and value_coordinate.y() >= 0 and value_coordinate.x() >= 0 and self.chart.series():
            self.hover_coordinate_label.setText(f"X: {value_coordinate.x():.2f}, Y: {value_coordinate.y():.2f}")
        elif self.hover_coordinate_label:
            self.hover_coordinate_label.setText("")
        
        # Provides the x coordinate and the nearest y value of the series at the mouse position.
        if self.chart.series():
            series = self.chart.series()[0]
            nearest_point = self.calculate_nearest_y_value(value_coordinate)
            
            if value_coordinate.y() >= 0 and value_coordinate.x() >= 0:
                self.highlight_nearest_point(nearest_point, series)
                
                if self.series_label:
                    self.series_label.setText(
                        f"X: {nearest_point.x():.2f} years, Y: ${nearest_point.y():.2f}")
            else:
                self.highlight_nearest_point(None, series)
                if self.series_label:
                    self.series_label.setText("")

    # Used to clear the labels when the mouse leaves the chart area.
    def leaveEvent(self, event):
        if self.chart.series():
            self.highlight_nearest_point(None, self.chart.series()[0])

        if self.hover_coordinate_label:
            self.hover_coordinate_label.setText("")

        if self.series_label:
            self.series_label.setText("")

        return super().leaveEvent(event)
    
    def calculate_nearest_y_value(self, value_coordinate):
        """Calculates the nearest y value and point to the given coordinate."""
        if not self.chart.series():
            return 0, None
            
        point_values = self.chart.series()[0].points()
        if not point_values:
            return 0, None
        
        nearest_point = point_values[0]
        min_distance = float('inf')
        target_x = value_coordinate.x()
        
        for point in point_values:
            x_distance = abs(point.x() - target_x)
            
            if x_distance < min_distance:
                min_distance = x_distance
                nearest_point = point
                
        
        return nearest_point
    
    def highlight_nearest_point(self, point, series):
        """Highlights the nearest point and resets the previous highlight"""
        # Calculate the index of the point to highlight
        if point is None:
            self.highlighted_point = None
            return
        if not series.points():
            return
        # Get the index of the point to highlight
        point_index = series.points().index(point) 
        
        # Get the index of the point to reset
        if self.highlighted_point is not None:
            try:
                previous_point_index = series.points().index(self.highlighted_point)
            except ValueError:
                previous_point_index = -1     
        
        # Reset previous highlighted point
        if self.highlighted_point is not None:
            original_point_configuration = {
                QXYSeries.PointConfiguration.Color: QColor(Qt.white),
                QXYSeries.PointConfiguration.Size: self.original_point_size
            }
            series.setPointConfiguration(previous_point_index, original_point_configuration)

        # Highlight new point
        if point is not None:
            highlighted_point_configuration = { 
                QXYSeries.PointConfiguration.Size: self.highlighted_point_size,
                QXYSeries.PointConfiguration.Color: QColor(Qt.red)
            }
            series.setPointConfiguration(point_index, highlighted_point_configuration)

            self.highlighted_point = point


