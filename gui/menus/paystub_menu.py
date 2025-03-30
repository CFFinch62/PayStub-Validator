import tkinter as tk
from tkinter import ttk, messagebox
from ..forms.paystub_forms import (
    GeneratePaystubForm,
    DisplayPaystubForm,
    PrintPaystubForm,
    DeletePaystubForm
)
from gui.gui_utils import center_elements
from ..forms.base_form import BaseForm

class PaystubMenu(BaseForm):
    def __init__(self, parent, main_app):
        super().__init__(main_app, parent)
        self.parent = parent

    def create_form(self):
        """Create the paystub menu form"""
        self.form_window.title("Paystub Menu")

        # Create container frame
        container = ttk.Frame(self.form_window, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(
            container,
            text="PAYSTUB MENU",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Paystub menu buttons
        ttk.Button(
            container,
            text="Generate Paystub",
            command=self.show_generate_paystub,
            width=30
        ).grid(row=1, column=0, pady=10)

        ttk.Button(
            container,
            text="Display Paystub",
            command=self.show_display_paystub,
            width=30
        ).grid(row=2, column=0, pady=10)

        ttk.Button(
            container,
            text="Print Paystub",
            command=self.show_print_paystub,
            width=30
        ).grid(row=3, column=0, pady=10)
        
        ttk.Button(
            container,
            text="Delete Paystub",
            command=self.show_delete_paystub,
            width=30
        ).grid(row=4, column=0, pady=10)

        ttk.Button(
            container,
            text="Back to Main Menu",
            command=self._on_close,
            width=30
        ).grid(row=5, column=0, pady=10)

        # Center all elements in the container
        center_elements(container)

        # Auto-size the window
        self.auto_size_window()

    def show_generate_paystub(self):
        """Show the generate paystub form"""
        self.show_child_window(GeneratePaystubForm(self.main_app))

    def show_display_paystub(self):
        """Show the display paystub form"""
        self.show_child_window(DisplayPaystubForm(self.main_app))

    def show_print_paystub(self):
        """Show the print paystub form"""
        self.show_child_window(PrintPaystubForm(self.main_app))
        
    def show_delete_paystub(self):
        """Show the delete paystub form"""
        self.show_child_window(DeletePaystubForm(self.main_app))
