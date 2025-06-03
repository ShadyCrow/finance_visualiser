from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QFormLayout
from PySide6.QtCore import Qt, Signal, Slot

class DataEntryWidget(QWidget):
    data_updated = Signal(str, str, int, float)
    
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
        
        self.investment_per_year_label = QLabel("Amount invested per year:")
        self.investment_per_year_line_edit = QLineEdit()
        self.investment_per_year_line_edit.setPlaceholderText("e.g. 5000")
        self.investment_per_year_line_edit.setToolTip("Enter the amount invested per year.")
        form_layout.addRow(self.investment_per_year_label, self.investment_per_year_line_edit)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self._on_calculate)
        form_layout.addRow(self.calculate_button)
        
        main_layout.addLayout(form_layout)
        
    
    @Slot()
    def _on_calculate(self):
        try:
            starting_amount = float(self.starting_amount_line_edit.text())
            growth_rate = float(self.growth_rate_line_edit.text()) / 100
            investment_period = int(self.investment_period_line_edit.text())
            investment_per_year = float(self.investment_per_year_line_edit.text())
            
            # Calculate the future including the investment per year.
            future_value = starting_amount * ((1 + growth_rate) ** investment_period)
            for year in range(1, investment_period + 1):
                future_value += investment_per_year * ((1 + growth_rate) ** (investment_period - year))


            # Emit the data_updated signal with the calculated values.
            self.data_updated.emit(
                str(starting_amount), 
                str(growth_rate * 100), 
                investment_period,
                investment_per_year
            )
            print("Data updated:", starting_amount, growth_rate * 100, investment_period)
            print(f"Future Value: {future_value:.2f}")
            QMessageBox.information(self, "Future Value", f"The future value is: ${future_value:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")

