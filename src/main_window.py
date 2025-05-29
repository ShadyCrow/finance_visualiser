from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter
from PySide6.QtCore import Qt

from menu_bar import MenuBar
from data_entry_widget import DataEntryWidget
from central_widget_plot import GraphWidget
from calculate_data import CalculateDataWidget


class MainWindow(QMainWindow):
    """Main window class for the application.
    This class inherits from QMainWindow and sets up the main window
    with a title and an optional parent widget.
    """
    def __init__(self):
        """Initialize the main window.
        Args:
            parent: Optional parent widget for the main window.
        """
        super().__init__()
        
        # Set the main window title.
        self.setWindowTitle("Finance Visualiser")
        
        
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.close_requested.connect(self.close)
        
        self.data_entry_widget = DataEntryWidget()
        self.setCentralWidget(self.data_entry_widget)


        # Create the status bar for the main window.
        self._create_status_bar()
        
        # Create the tool bar for the main window.
        # self._create_tool_bar()
        
        # Create the central widget for the main window.
        self._create_central_layout()
        
        self._create_connections()
        
        # Maximize the main window to fill the screen.
        self.showMaximized()


    def _create_tool_bar(self):
        """Create the tool bar for the main window.
        This method can be overridden to add custom tool items.
        """
        # Create the tool bar for the main window.
        tool_bar = self.addToolBar("Main Toolbar")
        
    def _create_status_bar(self):
        """Create the status bar for the main window.
        This method can be overridden to add custom status messages.
        """
        status_bar = self.statusBar()
        
        status_bar.showMessage(f"Ready", 5000)
        self.setStatusBar(status_bar)
        
    def _create_central_layout(self):
        """Create the central layout for the main window.
        This method can be overridden to set a custom central layout.
        """
        
        central_container_widget = QWidget()
        self.setCentralWidget(central_container_widget)

        self.splitter = QSplitter(Qt.Horizontal, self)

        main_horizontal_layout = QHBoxLayout(central_container_widget)

        self.data_entry_widget = DataEntryWidget()
        self.graph_widget = GraphWidget()
        self.calculate_data_widget = CalculateDataWidget()
        
        self.splitter.addWidget(self.data_entry_widget)
        self.splitter.addWidget(self.graph_widget)
        self.splitter.addWidget(self.calculate_data_widget)
        
        self.splitter.setSizes([200, 500, 200])
        
        main_horizontal_layout.addWidget(self.splitter)
        
    def _create_connections(self):
        """Create connections between widgets and slots.
        This method can be overridden to set up custom connections.
        """
        self.data_entry_widget.data_updated.connect(self.graph_widget.update_graph_data)
        self.data_entry_widget.data_updated.connect(self.calculate_data_widget.update_data)