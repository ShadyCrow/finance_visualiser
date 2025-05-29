from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt
from menu_bar import MenuBar
from data_entry_widget import DataEntryWidget


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
        self._create_central_widget()
        
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
        
    def _create_central_widget(self):
        """Create the central widget for the main window.
        This method can be overridden to set a custom central widget.
        """
        # Set the central widget to None by default.
        # This can be overridden in subclasses to set a custom widget.
        #self.setCentralWidget(None)
        
        # Optionally, you can create a placeholder widget here
        # if you want to have a default central widget.
        # For example:
        # placeholder_widget = QWidget()
        # self.setCentralWidget(placeholder_widget)
    

        