from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtCore import Signal


class MenuBar(QMenuBar):
    close_requested = Signal()
    
    def __init__(self, parent=None):
        # Initialize the menu bar for the main window.
        super().__init__(parent)
        
        self.main_window = parent

        # Create the File menu.
        self._create_file_menu()

        # Create the View menu.
        self._create_view_menu()

        # Create the Help menu.
        self._create_help_menu()
        
    def _create_file_menu(self):
        """ Create the file menu for the main window.
        This method sets up the file menu with common actions.
        """
        # Create a File menu.
        file_menu = QMenu("&File", self)
        self.addMenu(file_menu)

        # Adds an Exit action in the File menu.
        self._exit_action(file_menu)

        # Adds a Save action in the File menu.
        self._save_action(file_menu)

        # Adds an Export to Excel action in the File menu.
        self._export_to_excel_action(file_menu)
                       
        
    def _exit_action(self, file_menu):
        """Create an exit action for the main window.
        This method can be overridden to add custom exit functionality.
        """
        # Create an Exit action in the File menu.
        exit_action = file_menu.addAction("Exit")
        
        # Allow the user to exit the application
        # using a keyboard shortcut.
        exit_action.setShortcut("Ctrl+Q")

        # Shows the user a tooltip when the user hovers over the action.
        exit_action.setStatusTip("Exit the application.")

        # Connect the exit action to the close method
        # of the main window to exit the application.
        exit_action.triggered.connect(self._emit_close_signal)
        
        file_menu.addSeparator()
        
    def _emit_close_signal(self):
        self.close_requested.emit()

        
    def _save_action(self, file_menu):
        """Create a save action for the main window.
        This method can be overridden to add custom save functionality.
        """
        save_action = file_menu.addAction("Save")

        # Allow the user to save the current file
        # using a keyboard shortcut.
        save_action.setShortcut("Ctrl+S")

        save_action.setStatusTip("Save the current file.")
        
        file_menu.addSeparator()
    
    def _export_to_excel_action(self, file_menu):
        """Create an export to Excel action for the main window.
        This method can be overridden to add custom export functionality.
        """
        export_action = file_menu.addAction("Export to Excel")
        
        export_action.setShortcut("Ctrl+Shift+E")
        
        export_action.setStatusTip("Export data to an Excel file.")
        
        file_menu.addSeparator()
        
        
    def _create_view_menu(self):
        """Create the view menu for the main window.
        This method can be overridden to add custom view options.
        """
        # Create a View menu.
        view_menu = QMenu("&View", self)
        
        # Add the View menu to the menu bar.
        self.addMenu(view_menu)

        # Add the Fullscreen action to the View menu.
        self._fullscreen_action(view_menu)
        
        # Add the escape fullscreen action to the View menu.
        self._exit_fullscreen_action(view_menu)
        
        # Add actions to the View menu as needed.
        # For example, you can add a toggle for a sidebar or toolbar.
        
    def _fullscreen_action(self, view_menu):
        """Create a fullscreen action for the main window.
        This method can be overridden to add custom fullscreen functionality.
        """
        # Create a Fullscreen action in the View menu.
        fullscreen_action = view_menu.addAction("Fullscreen")
        
        # Allow the user to toggle fullscreen mode
        # using a keyboard shortcut.
        fullscreen_action.setShortcut("F11")
        
        fullscreen_action.setStatusTip("Enter fullscreen mode.")
        
        # Connect the action to the toggle_fullscreen method.
        fullscreen_action.triggered.connect(self.main_window.showFullScreen)

        
    def _exit_fullscreen_action(self, view_menu):
        """Create an exit fullscreen action for the main window.
        This method can be overridden to add custom exit fullscreen functionality.
        """
        # Create an Exit Fullscreen action in the View menu.
        exit_fullscreen_action = view_menu.addAction("Exit Fullscreen")
        
        # Allow the user to exit fullscreen mode
        # using a keyboard shortcut.
        exit_fullscreen_action.setShortcut("Esc")
        
        exit_fullscreen_action.setStatusTip("Exit fullscreen mode.")
        
        # Connect the action to the showNormal method of the main window.
        exit_fullscreen_action.triggered.connect(self.main_window.showNormal)
        
        
    def _create_help_menu(self):
        """Create the help menu for the main window.
        This method can be overridden to add custom help options.
        """
        # Create a Help menu.
        help_menu = QMenu("&Help", self)
        
        # Add the Help menu to the menu bar.
        self.addMenu(help_menu)
        
        # Add actions to the Help menu as needed.
        # For example, you can add an "About" action or a "Documentation" link.
        

                