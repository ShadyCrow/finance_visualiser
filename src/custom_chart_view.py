from PySide6.QtCharts import QChartView, QLineSeries, QXYSeries, QValueAxis
from PySide6.QtGui import QMouseEvent, QPen, QColor, QWheelEvent, QPainter, QBrush
from PySide6.QtWidgets import QLabel, QGraphicsTextItem, QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import QPointF, Qt, QRectF

class CustomChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setMouseTracking(True)
        self.chart = chart
        
        self.setRenderHint(QPainter.Antialiasing)
        
        self.hover_coordinate_label = None
        self.series_label = None
        
        self.highlighted_point = None
        self.original_point_size = 1
        self.highlighted_point_size = 8
        
        self.original_range_x = 0
        self.original_range_y = 0
        
        
        self.left_click_marker = None
        self.left_click_text = None
        self.right_click_marker = None
        self.right_click_text = None
        self.c_key_pressed = False

        # Create point configurations
        self.original_point_configuration = {
                QXYSeries.PointConfiguration.Size: self.original_point_size
            }
        
        self.highlighted_point_configuration = { 
                QXYSeries.PointConfiguration.Size: self.highlighted_point_size,
                QXYSeries.PointConfiguration.Color: QColor(Qt.red)
            }

    def set_hover_coordinate_label(self, label: QLabel):
        """Sets a QLabel to display the hovered coordinates."""
        self.hover_coordinate_label = label
        
    def set_series_label(self, label_2: QLabel):
        """Sets a QLabel to display the series coordinate."""
        self.series_label = label_2
        
    def mousePressEvent(self, event: QMouseEvent):
        # Check if the 'C' key is pressed to enable marker placement
        if self.c_key_pressed:
            scene_position = self.mapToScene(event.pos())
            chart_item_position = self.chart.mapFromScene(scene_position)
            value_coordinate = self.chart.mapToValue(chart_item_position)
            nearest_point = self.calculate_nearest_point(value_coordinate)
            
                
            if event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.RightButton:
                # Handle marker placement for both left and right clicks
                is_left = event.button() == Qt.MouseButton.LeftButton
                
                marker_radius = 5
                marker_size = QRectF(-marker_radius, -marker_radius, marker_radius * 2, marker_radius * 2)
                marker_pen = QPen(QColor(Qt.black), 1)
                
                
                # Remove existing marker if it exists
                marker = self.left_click_marker if is_left else self.right_click_marker
                marker_text = self.left_click_text if is_left else self.right_click_text
                
                if marker:
                    self.scene().removeItem(marker)
                if marker_text:
                    self.scene().removeItem(marker_text)
                
                # Create new marker
                marker_brush = QBrush(QColor(Qt.green if is_left else Qt.cyan))
                new_marker = QGraphicsEllipseItem(marker_size)
                new_marker.setPen(marker_pen)
                new_marker.setBrush(marker_brush)
                new_marker.setPos(self.chart.mapToPosition(nearest_point))
                self.scene().addItem(new_marker)
                
                # Update the marker reference
                if is_left:
                    self.left_point_value = nearest_point
                    self.left_click_marker = new_marker
                else:
                    self.right_point_value = nearest_point
                    self.right_click_marker = new_marker
                
                self.scene().update()
                event.accept()
                return
    
            # Important: Accept the event even if we don't have a valid point
            event.accept()
            return
    
        # Only call parent implementation if C is not pressed
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self.c_key_pressed and event.button() == Qt.MouseButton.RightButton:
            event.accept()
            return
        
        super().mouseReleaseEvent(event)    
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_C:
            self.c_key_pressed = True
            self.setDragMode(QChartView.DragMode.NoDrag)
            event.accept()
        else:
            return super().keyPressEvent(event)
        
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_C:
            self.c_key_pressed = False
            event.accept()
        else:
            return super().keyReleaseEvent(event)

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
            nearest_point = self.calculate_nearest_point(value_coordinate)
            
            if value_coordinate.y() >= 0 and value_coordinate.x() >= 0:
                self.highlight_nearest_point(nearest_point, series)
                
                if self.series_label:
                    self.series_label.setText(
                        f"X: {int(nearest_point.x())} years, Y: ${nearest_point.y():,.2f}")
            else:
                self.highlight_nearest_point(None, series)
                if self.series_label:
                    self.series_label.setText("")

    # Used to clear the labels when the mouse leaves the chart area.
    def leaveEvent(self, event):
        if self.chart.series():
            for point in self.chart.series()[0].points():
                reset_point = self.chart.series()[0].points().index(point)
                self.chart.series()[0].setPointConfiguration(reset_point, self.original_point_configuration)
            

        if self.hover_coordinate_label:
            self.hover_coordinate_label.setText("")

        if self.series_label:
            self.series_label.setText("")

        return super().leaveEvent(event)
    
    def calculate_nearest_point(self, value_coordinate):
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
            series.setPointConfiguration(previous_point_index, self.original_point_configuration)

        # Highlight new point
        if point is not None:
            series.setPointConfiguration(point_index, self.highlighted_point_configuration)

            self.highlighted_point = point
            
            
    def wheelEvent(self, event: QWheelEvent):
        mouse_position = event.position()
        plot_area = self.chart.plotArea()

        axis_tolerance = 50

        if mouse_position.x() < plot_area.left() + axis_tolerance and \
           mouse_position.y() > plot_area.top() and \
           mouse_position.y() < plot_area.bottom():
            
            difference = event.angleDelta().y()
           
            # Checks to ensure that the Y axis exists
            y_axis = None
            for axis in self.chart.axes(Qt.Orientation.Vertical):
                if isinstance(axis, QValueAxis):
                    y_axis = axis
                    break
            
            if y_axis:
                current_minimum = y_axis.min()
                current_maximum = y_axis.max()
                
                current_range = current_maximum - current_minimum
                
                zoom_factor = 0.1
                
                if difference > 0:
                    new_min = current_minimum + current_range * zoom_factor / 2
                    new_max = current_maximum - current_range * zoom_factor / 2
                elif difference <= 0:
                    new_min = current_minimum - current_range * zoom_factor / 2
                    new_max = current_maximum + current_range * zoom_factor / 2
                    
                if new_min < new_max:
                    y_axis.setRange(new_min, new_max)
                    self.update_marker_positions()
                else:
                    y_axis.setRange(new_min, new_max)
                event.accept()
                
            else:
                super().wheelEvent(event)
                
        elif mouse_position.y() > plot_area.bottom() - axis_tolerance and \
             mouse_position.x() > plot_area.left() and \
             mouse_position.x() < plot_area.right():
            
            # Refers to the angle of scrolling, not the axis on the graph
            difference_x = event.angleDelta().y()
            
            # Checks to ensure that the x axis exists           
            x_axis = None
            for axis in self.chart.axes(Qt.Orientation.Horizontal):
                if isinstance(axis, QValueAxis):
                    x_axis = axis
                    break
                
            if x_axis:
                current_minimum = x_axis.min()
                current_maximum = x_axis.max()
                
                current_range = current_maximum - current_minimum
                
                zoom_factor = 0.1
                
                if difference_x > 0:
                    new_min = current_minimum + current_range * zoom_factor / 2
                    new_max = current_maximum - current_range * zoom_factor / 2
                elif difference_x <= 0:
                    new_min = current_minimum - current_range * zoom_factor / 2
                    new_max = current_maximum + current_range * zoom_factor / 2
                    
                if new_min < new_max:
                    x_axis.setRange(new_min, new_max)
                    self.update_marker_positions()
                else:
                    x_axis.setRange(new_min, new_max)
                event.accept()
                
            else:
                super().wheelEvent(event)
            
            
        else:
            super().wheelEvent(event)

    def set_original_range(self):
         # Store the original range of the axes        
        for axis in self.chart.axes(Qt.Orientation.Horizontal):
                if isinstance(axis, QValueAxis):
                    self.original_range_x = (axis.min(), axis.max())
                    
        for axis in self.chart.axes(Qt.Orientation.Vertical):
            if isinstance(axis, QValueAxis):
                self.original_range_y = (axis.min(), axis.max())

    def reset_zoom(self):
        # Reset the zoom level to the original range
        x_axis = None
        for axis in self.chart.axes(Qt.Orientation.Horizontal):
            if isinstance(axis, QValueAxis):
                x_axis = axis
                break
            
        y_axis = None
        for axis in self.chart.axes(Qt.Orientation.Vertical):
            if isinstance(axis, QValueAxis):
                y_axis = axis
                break

        # Check if the original ranges are set and apply them
        if x_axis and y_axis:
            x_axis.setRange(float(self.original_range_x[0]), float(self.original_range_x[1]))
            y_axis.setRange(float(self.original_range_y[0]), float(self.original_range_y[1]))
            self.update_marker_positions()
            
    def update_marker_positions(self):
        """Updates the position of markers when chart view changes."""
        if self.left_click_marker and hasattr(self, 'left_point_value'):
            new_pos = self.chart.mapToPosition(self.left_point_value)
            self.left_click_marker.setPos(new_pos)
            
        if self.right_click_marker and hasattr(self, 'right_point_value'):
            new_pos = self.chart.mapToPosition(self.right_point_value)
            self.right_click_marker.setPos(new_pos)

