from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, Signal, Slot

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        label = QLabel("Graph Widget Placeholder")
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        
        self.setStyleSheet("background-color: lightgray;")
        self.data_display_label = QLabel("No data available to display.")

        self.data_display_label.setWordWrap(True)
        layout.addWidget(self.data_display_label)
    
    @Slot(str, str, int)
    def update_graph_data(self, starting_amount, growth_rate, investment_period):
        print("DEBUG: Slot received signal in GraphWidget")
        print(f"Updating graph data with: {starting_amount}, {growth_rate}, {investment_period}")
        self.data_display_label.setText(f"Graph Widget: {starting_amount}, {growth_rate}, {investment_period} - Data updated successfully.")