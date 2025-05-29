from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, Signal, Slot

class CalculateDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        
        self.data_display_label = QLabel("No data available to display.")
        self.data_display_label.setAlignment(Qt.AlignCenter)
        self.data_display_label.setWordWrap(True)
        
        layout.addWidget(self.data_display_label)

    @Slot(str, str, int)
    def update_data(self, starting_amount, growth_rate, investment_period):
        print("DEBUG: Slot received signal in CalculateDataWidget")
        print(f"Updating data with: {starting_amount}, {growth_rate}, {investment_period}")
        graph_widget = f"Starting Amount: {starting_amount}, Growth Rate: {growth_rate}%, Investment Period: {investment_period} years"
        self.data_display_label.setText(graph_widget)  # Update the label to verify data receipt
        