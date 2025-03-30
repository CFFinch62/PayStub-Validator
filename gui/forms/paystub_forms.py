import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .base_form import BaseForm
from ..gui_utils import center_elements

class GeneratePaystubForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.paystub_ops = main_app.paystub_ops

    def create_form(self):
        """Create the generate paystub form"""
        self.form_window.title("Generate Paystub")
        self.form_window.geometry("500x350")  # Smaller size since it's just a list and buttons
        self.form_window.resizable(False, False)  # Prevent resizing

        # Create main container
        container = ttk.Frame(self.form_window, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(
            container,
            text="GENERATE PAYSTUB",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Timesheet selection frame
        select_frame = ttk.LabelFrame(container, text="Select Timesheet", padding="10")
        select_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        timesheet_listbox = tk.Listbox(select_frame, width=50, height=5)
        timesheet_listbox.grid(row=0, column=0, padx=5, pady=5)

        # Load timesheets
        timesheets = self.data_manager.get_timesheets()
        for timesheet in timesheets:
            timesheet_listbox.insert(tk.END, timesheet['week_end'])

        def generate_paystub():
            selection = timesheet_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a timesheet to generate paystub")
                return

            week_end = timesheet_listbox.get(selection[0])
            
            try:
                # Get the full timesheet object
                timesheet = self.data_manager.get_timesheet(week_end)
                if not timesheet:
                    messagebox.showerror("Error", "Timesheet not found")
                    return

                success, message = self.paystub_ops.generate_paystub(timesheet)
                if success:
                    messagebox.showinfo("Success", message)
                    self._on_close()
                else:
                    messagebox.showerror("Error", message)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(container)
        button_frame.grid(row=2, column=0, pady=20)

        ttk.Button(button_frame, text="Generate", command=generate_paystub, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')

class DisplayPaystubForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.paystub_ops = main_app.paystub_ops

    def create_form(self):
        """Create the display paystub form"""
        self.form_window.title("Display Paystub")
        self.form_window.geometry("800x800")

        # Create main container with scrollbar
        main_frame = ttk.Frame(self.form_window)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.form_window.grid_rowconfigure(0, weight=1)
        self.form_window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the scrollable frame
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create the window in the canvas
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)

        # Function to update the scroll region
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(frame_window, width=canvas.winfo_width())
            canvas.itemconfig(frame_window, height=canvas.winfo_height())

        # Bind events for resizing
        canvas.bind('<Configure>', update_scroll_region)
        scrollable_frame.bind('<Configure>', update_scroll_region)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Title
        title = ttk.Label(
            scrollable_frame,
            text="PAYSTUBS",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Paystub list
        paystub_frame = ttk.LabelFrame(scrollable_frame, text="Select Paystub", padding="10")
        paystub_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        # Configure grid weights for paystub frame
        paystub_frame.grid_columnconfigure(0, weight=1)
        paystub_frame.grid_rowconfigure(0, weight=1)

        # Create listbox for paystubs
        paystub_listbox = tk.Listbox(paystub_frame, height=5)  # Reduced height
        paystub_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Add scrollbar to listbox
        listbox_scrollbar = ttk.Scrollbar(paystub_frame, orient="vertical", command=paystub_listbox.yview)
        listbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        paystub_listbox.configure(yscrollcommand=listbox_scrollbar.set)

        # Populate paystub list
        success, result = self.paystub_ops.get_employee_paystubs()
        if success:
            for paystub in result:
                paystub_listbox.insert(tk.END, paystub['week_end'])

        # Create details frame for paystub details
        self.details_frame = ttk.Frame(scrollable_frame)
        self.details_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        def display_paystub():
            selection = paystub_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a paystub to display")
                return

            week_end = paystub_listbox.get(selection[0])
            
            try:
                success, result = self.paystub_ops.get_paystub_details(week_end)
                if not success:
                    messagebox.showerror("Error", result)
                    return

                paystub = result
                self.display_paystub(paystub)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=3, column=0, pady=20)

        ttk.Button(button_frame, text="Display", command=display_paystub, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Close", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')

    def display_paystub(self, paystub):
        """Display paystub details"""
        # Clear previous display
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Create two main rows
        top_row = ttk.Frame(self.details_frame)
        top_row.pack(fill=tk.X, padx=5, pady=5)

        bottom_row = ttk.Frame(self.details_frame)
        bottom_row.pack(fill=tk.X, padx=5, pady=5)

        # Top row: Hours/Wages and Pay sections
        # Hours and Wages section
        hours_frame = ttk.LabelFrame(top_row, text="Hours and Wages", padding="5")
        hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Create a frame for the grid layout
        grid_frame = ttk.Frame(hours_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        # Headers
        ttk.Label(grid_frame, text="Hours", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(grid_frame, text="Wages", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        # Display hours and wages side by side
        for i, (category, hours) in enumerate(paystub['hours'].items(), start=1):
            ttk.Label(grid_frame, text=f"{category}: {hours:.2f}").grid(row=i, column=0, padx=5, pady=1, sticky=tk.W)
            ttk.Label(grid_frame, text=f"${paystub['wages'][category]:.2f}").grid(row=i, column=1, padx=5, pady=1, sticky=tk.W)

        # Pay section
        pay_frame = ttk.LabelFrame(top_row, text="Pay Summary", padding="5")
        pay_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(pay_frame, text=f"Gross Pay: ${paystub['pay']['gross']:.2f}").pack(anchor=tk.W)
        ttk.Label(pay_frame, text=f"Adjusted Gross: ${paystub['pay']['adjusted_gross']:.2f}").pack(anchor=tk.W)
        ttk.Label(pay_frame, text=f"Net Pay: ${paystub['pay']['net']:.2f}").pack(anchor=tk.W)

        # Bottom row: Additions, Pre-tax Deductions, and Post-tax Deductions
        # Additions section
        additions_frame = ttk.LabelFrame(bottom_row, text="Additions", padding="5")
        additions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        for addition_id, amount in paystub['additions'].items():
            ttk.Label(additions_frame, text=f"{addition_id}: ${amount:.2f}").pack(anchor=tk.W)

        # Pre-tax Deductions section
        pre_tax_frame = ttk.LabelFrame(bottom_row, text="Pre-tax Deductions", padding="5")
        pre_tax_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        for deduction_id, amount in paystub['pre_tax_deductions'].items():
            ttk.Label(pre_tax_frame, text=f"{deduction_id}: ${amount:.2f}").pack(anchor=tk.W)

        # Post-tax Deductions section
        post_tax_frame = ttk.LabelFrame(bottom_row, text="Post-tax Deductions", padding="5")
        post_tax_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        for deduction_id, amount in paystub['post_tax_deductions'].items():
            ttk.Label(post_tax_frame, text=f"{deduction_id}: ${amount:.2f}").pack(anchor=tk.W)

class PrintPaystubForm(DisplayPaystubForm):
    def create_form(self):
        """Create the print paystub form"""
        super().create_form()
        # Add print button
        ttk.Button(self.button_frame, text="Print", command=self.print_paystub, width=15).grid(row=0, column=2, padx=5)

    def print_paystub(self):
        """Print the selected paystub"""
        # TODO: Implement printing functionality
        messagebox.showinfo("Print", "Printing functionality to be implemented")

class DeletePaystubForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.paystub_ops = main_app.paystub_ops
        self.form_window = None

    def create_form(self):
        """Create the delete paystub form"""
        self.form_window.title("Delete Paystub")
        self.form_window.geometry("500x350")
        self.form_window.resizable(False, False)

        # Create main container with scrollbar
        main_frame = ttk.Frame(self.form_window)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.form_window.grid_rowconfigure(0, weight=1)
        self.form_window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the scrollable frame
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Create the window in the canvas
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)

        # Function to update the scroll region
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(frame_window, width=canvas.winfo_width())
            canvas.itemconfig(frame_window, height=canvas.winfo_height())

        # Bind events for resizing
        canvas.bind('<Configure>', update_scroll_region)
        scrollable_frame.bind('<Configure>', update_scroll_region)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Title
        title = ttk.Label(
            scrollable_frame,
            text="DELETE PAYSTUB",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Paystub list
        paystub_frame = ttk.LabelFrame(scrollable_frame, text="Select Paystub to Delete", padding="10")
        paystub_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        # Configure grid weights for paystub frame
        paystub_frame.grid_columnconfigure(0, weight=1)
        paystub_frame.grid_rowconfigure(0, weight=1)

        # Create listbox for paystubs
        paystub_listbox = tk.Listbox(paystub_frame, height=8)
        paystub_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Add scrollbar to listbox
        listbox_scrollbar = ttk.Scrollbar(paystub_frame, orient="vertical", command=paystub_listbox.yview)
        listbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        paystub_listbox.configure(yscrollcommand=listbox_scrollbar.set)

        # Populate paystub list
        success, result = self.paystub_ops.get_employee_paystubs()
        if success:
            for paystub in result:
                paystub_listbox.insert(tk.END, paystub['week_end'])

        def delete_paystub():
            selection = paystub_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a paystub to delete")
                return

            week_end = paystub_listbox.get(selection[0])
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the paystub for {week_end}?")
            if not confirm:
                return
                
            try:
                success, result = self.paystub_ops.delete_paystub(week_end)
                if success:
                    messagebox.showinfo("Success", result)
                    # Refresh the listbox
                    paystub_listbox.delete(0, tk.END)
                    success, refreshed_paystubs = self.paystub_ops.get_employee_paystubs()
                    if success:
                        for paystub in refreshed_paystubs:
                            paystub_listbox.insert(tk.END, paystub['week_end'])
                else:
                    messagebox.showerror("Error", result)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=3, column=0, pady=20)

        ttk.Button(button_frame, text="Delete", command=delete_paystub, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Close", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')
