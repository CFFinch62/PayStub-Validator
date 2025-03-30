import tkinter as tk
from tkinter import ttk

class BaseForm:
    def __init__(self, main_app, parent_window=None):
        self.main_app = main_app
        self.form_window = None
        self.parent_window = parent_window
        self.child_windows = []

    def show(self):
        """Show the form window. If it already exists, bring it to front."""
        if self.form_window and self.form_window.winfo_exists():
            self.form_window.lift()
            return

        # Create the window
        self.form_window = tk.Toplevel(self.main_app.root)
        self.form_window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Hide parent window if it exists and is a form window
        if self.parent_window and hasattr(self.parent_window, 'form_window') and self.parent_window.form_window:
            self.parent_window.form_window.withdraw()
        # If parent is the main app, hide the root window
        elif self.parent_window == self.main_app:
            self.main_app.root.withdraw()
        
        # Create the form content
        self.create_form()

    def create_form(self):
        """Create the form content. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement create_form()")

    def _on_close(self):
        """Handle window closing"""
        if self.form_window:
            # Show parent window if it exists and is a form window
            if self.parent_window and hasattr(self.parent_window, 'form_window') and self.parent_window.form_window:
                self.parent_window.form_window.deiconify()
            # If parent is the main app, show the root window
            elif self.parent_window == self.main_app:
                self.main_app.root.deiconify()
            
            # Close all child windows
            for child in self.child_windows:
                try:
                    if hasattr(child, 'form_window') and child.form_window and child.form_window.winfo_exists():
                        child.form_window.destroy()
                except Exception:
                    pass  # Ignore any errors when closing child windows
            
            # Destroy this window
            self.form_window.destroy()
            self.form_window = None

            # If this is a top-level form (no parent), ensure the main window is shown
            if not self.parent_window:
                self.main_app.root.deiconify()

    def auto_size_window(self):
        """Automatically size the form window to fit its contents"""
        if self.form_window:
            self.main_app.auto_size_window(self.form_window)

    def show_child_window(self, child_form):
        """Show a child window and track it"""
        child_form.parent_window = self
        self.child_windows.append(child_form)
        child_form.show()

    def center_window(self):
        """Center the form window on the screen"""
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_form(self):
        # Existing code...
        
        # Center the window on screen
        self.center_window() 