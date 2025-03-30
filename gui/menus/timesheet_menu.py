import tkinter as tk
from tkinter import ttk, messagebox
from ..forms.timesheet_forms import (
    EnterTimesheetForm,
    EditTimesheetForm,
    DeleteTimesheetForm,
    DisplayTimesheetForm,
    PrintTimesheetForm
)
from gui.gui_utils import center_elements, center_frame
from ..forms.base_form import BaseForm

class TimesheetMenu(BaseForm):
    def __init__(self, parent, main_app):
        super().__init__(main_app, parent)
        self.parent = parent

    def create_form(self):
        """Create the timesheet menu form"""
        self.form_window.title("Timesheet Menu")

        # Create outer frame and get centered inner frame
        container = ttk.Frame(self.form_window)
        content_frame = center_frame(container, self.form_window)
        
        # Title
        title = ttk.Label(
            content_frame, 
            text="TIMESHEET MENU",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)
        
        # Timesheet menu buttons
        ttk.Button(
            content_frame,
            text="Enter New Timesheet",
            command=self.show_enter_timesheet,
            width=30
        ).grid(row=1, column=0, pady=10)

        ttk.Button(
            content_frame,
            text="Edit Timesheet",
            command=self.show_edit_timesheet,
            width=30
        ).grid(row=2, column=0, pady=10)

        ttk.Button(
            content_frame,
            text="Delete Timesheet",
            command=self.show_delete_timesheet,
            width=30
        ).grid(row=3, column=0, pady=10)

        ttk.Button(
            content_frame,
            text="Display Timesheet",
            command=self.show_display_timesheet,
            width=30
        ).grid(row=4, column=0, pady=10)

        ttk.Button(
            content_frame,
            text="Print Timesheet",
            command=self.show_print_timesheet,
            width=30
        ).grid(row=5, column=0, pady=10)

        ttk.Button(
            content_frame,
            text="Back to Main Menu",
            command=self._on_close,
            width=30
        ).grid(row=6, column=0, pady=10)
        
        # Center elements within the content frame
        center_elements(content_frame)

        # Auto-size the window
        self.auto_size_window()

    def show_enter_timesheet(self):
        """Show the enter timesheet form"""
        self.show_child_window(EnterTimesheetForm(self.main_app))

    def show_edit_timesheet(self):
        """Show the edit timesheet form"""
        self.show_child_window(EditTimesheetForm(self.main_app))

    def show_delete_timesheet(self):
        """Show the delete timesheet form"""
        self.show_child_window(DeleteTimesheetForm(self.main_app))

    def show_display_timesheet(self):
        """Show the display timesheet form"""
        self.show_child_window(DisplayTimesheetForm(self.main_app))

    def show_print_timesheet(self):
        """Show the print timesheet form"""
        self.show_child_window(PrintTimesheetForm(self.main_app))
