from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QFormLayout
from PySide6.QtCore import Qt 

class DataEntryWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setAlignment(Qt.AlignTop)
        
        form_layout = QFormLayout()
        
        self.starting_amount_label = QLabel("Starting amount:")
        self.starting_amount_line_edit = QLineEdit()
        self.starting_amount_line_edit.setPlaceholderText("e.g. 1000")
        self.starting_amount_line_edit.setToolTip("Enter the starting amount in your currency.")
        form_layout.addRow(self.starting_amount_label, self.starting_amount_line_edit)
        
        self.growth_rate_label = QLabel("Growth rate (%):")
        self.growth_rate_line_edit = QLineEdit()
        self.growth_rate_line_edit.setPlaceholderText("e.g. 5")
        self.growth_rate_line_edit.setToolTip("Enter the expected growth rate.")
        form_layout.addRow(self.growth_rate_label, self.growth_rate_line_edit)

        self.investment_period_label = QLabel("Investment period (years):")
        self.investment_period_line_edit = QLineEdit()
        self.investment_period_line_edit.setPlaceholderText("e.g. 10")
        self.investment_period_line_edit.setToolTip("Enter the investment period in years.")
        form_layout.addRow(self.investment_period_label, self.investment_period_line_edit)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self._on_calculate)
        form_layout.addRow(self.calculate_button)
        
        main_layout.addLayout(form_layout)

    def _on_calculate(self):
        try:
            starting_amount = float(self.starting_amount_line_edit.text())
            growth_rate = float(self.growth_rate_line_edit.text()) / 100
            investment_period = int(self.investment_period_line_edit.text())
            
            future_value = starting_amount * ((1 + growth_rate) ** investment_period)
            
            QMessageBox.information(self, "Future Value", f"The future value is: ${future_value:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")

