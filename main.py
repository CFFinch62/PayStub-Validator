import tkinter as tk
from tkinter import ttk
from data.data_manager import DataManager
from employee_operations import EmployeeOperations
from timesheet_operations import TimesheetOperations
from paystub_operations import PaystubOperations
from gui.gui_utils import center_window, center_elements
from gui.menus.timesheet_menu import TimesheetMenu
from gui.menus.paystub_menu import PaystubMenu
from gui.forms.employee_forms import EmployeeMenu

class WageCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PAYSTUB VALIDATOR")
        self.root.geometry("320x300")  # Increased height for new button
        center_window(self.root)
        
        # Initialize operations
        self.data_manager = DataManager()
        self.employee_ops = EmployeeOperations(self.data_manager)
        self.timesheet_ops = TimesheetOperations(self.data_manager)
        self.paystub_ops = PaystubOperations(self.data_manager)

        # Create main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initialize forms
        self.employee_menu = EmployeeMenu(self)
        self.timesheet_menu = TimesheetMenu(self, self)
        self.paystub_menu = PaystubMenu(self, self)

        # Create and show main menu
        self.create_main_menu()

    def auto_size_window(self, window):
        """Automatically size a window to fit its contents"""
        # Update the window to ensure all widgets are rendered
        window.update_idletasks()
        
        # Get the required width and height
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        
        # Add padding
        width += 20
        height += 20
        
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Ensure window doesn't exceed screen size
        width = min(width, screen_width - 40)
        height = min(height, screen_height - 40)
        
        # Set window size
        window.geometry(f"{width}x{height}")
        
        # Center the window
        center_window(window)

    def exit_application(self):
        """Properly exit the application"""
        self.root.destroy()

    def create_main_menu(self):
        # Clear existing widgets
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Create container frame
        self.menu_container = ttk.Frame(self.main_container, padding="20")
        self.menu_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(
            self.menu_container,
            text="PAYSTUB VALIDATOR",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Menu buttons
        ttk.Button(
            self.menu_container,
            text="Employee Information",
            command=self.show_employee_menu,
            width=30
        ).grid(row=1, column=0, pady=10)

        ttk.Button(
            self.menu_container,
            text="Timesheets",
            command=self.show_timesheet_menu,
            width=30
        ).grid(row=2, column=0, pady=10)

        ttk.Button(
            self.menu_container,
            text="Paystubs",
            command=self.show_paystub_menu,
            width=30
        ).grid(row=3, column=0, pady=10)

        ttk.Button(
            self.menu_container,
            text="Exit",
            command=self.exit_application,
            width=30
        ).grid(row=4, column=0, pady=10)

        # Center all elements in the container
        center_elements(self.menu_container)

    def show_employee_menu(self):
        """Show the employee menu and hide the main window"""
        self.root.withdraw()
        self.employee_menu.show()

    def show_timesheet_menu(self):
        """Show the timesheet menu and hide the main window"""
        self.root.withdraw()
        self.timesheet_menu.show()

    def show_paystub_menu(self):
        """Show the paystub menu and hide the main window"""
        self.root.withdraw()
        self.paystub_menu.show()

    def show_main_menu(self):
        """Show the main menu"""
        self.root.deiconify()

def main():
    root = tk.Tk()
    app = WageCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 