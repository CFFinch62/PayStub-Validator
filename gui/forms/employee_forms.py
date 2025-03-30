import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .base_form import BaseForm
from ..gui_utils import center_elements

class EmployeeMenu(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.employee_ops = main_app.employee_ops

    def create_form(self):
        """Create the employee menu window"""
        self.form_window.title("Employee Information Menu")
        self.form_window.geometry("320x300")

        # Create main container
        container = ttk.Frame(self.form_window, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(
            container,
            text="EMPLOYEE INFORMATION",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Menu buttons
        ttk.Button(
            container,
            text="Basic Information",
            command=self.show_basic_info,
            width=30
        ).grid(row=1, column=0, pady=10)

        ttk.Button(
            container,
            text="Union Information",
            command=self.show_union_info,
            width=30
        ).grid(row=2, column=0, pady=10)

        ttk.Button(
            container,
            text="Deductions",
            command=self.show_deductions,
            width=30
        ).grid(row=3, column=0, pady=10)

        ttk.Button(
            container,
            text="Back to Main Menu",
            command=self._on_close,
            width=30
        ).grid(row=4, column=0, pady=10)

        # Center all elements
        center_elements(container)

        # Center the window on screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def show_basic_info(self):
        """Show the basic information form"""
        self.show_child_window(BasicInfoForm(self.main_app))

    def show_union_info(self):
        """Show the union information form"""
        self.show_child_window(UnionInfoForm(self.main_app))

    def show_deductions(self):
        """Show the deductions form"""
        self.show_child_window(DeductionsForm(self.main_app))

class BasicInfoForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.employee_ops = main_app.employee_ops
        self.form_window = None

    def create_form(self):
        """Create the basic information form"""
        self.form_window.title("Basic Employee Information")
        self.form_window.geometry("500x400")

        # Create main container
        container = ttk.Frame(self.form_window, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(
            container,
            text="BASIC EMPLOYEE INFORMATION",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Load existing data
        employee = self.employee_ops.get_employee_data()

        # Create fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Hire Date (YYYY-MM-DD):", "hire_date"),
            ("Filing Status (S/M):", "filing_status"),
            ("Pay Rate:", "pay_rate"),
            ("Filing Dependents:", "filing_dependents")
        ]

        # Create entry widgets and store them as instance variables
        self.entries = {}
        for i, (label_text, field_name) in enumerate(fields, start=1):
            ttk.Label(container, text=label_text).grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            
            if field_name == "filing_status":
                entry = ttk.Combobox(container, values=['S', 'M'], width=30)
            else:
                entry = ttk.Entry(container, width=30)
            
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.W)
            self.entries[field_name] = entry

            # Load existing data if available
            if employee and employee.get(field_name):
                if field_name == "filing_status":
                    entry.set(employee.get(field_name))
                else:
                    entry.insert(0, str(employee.get(field_name)))
            elif field_name == "filing_dependents":
                # Set default value of 0 for filing dependents if no data exists
                entry.insert(0, "0")

        # Buttons
        button_frame = ttk.Frame(container)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self._on_save, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def _on_save(self):
        """Handle save button click"""
        try:
            # Get existing data first to preserve all other sections
            existing_data = self.employee_ops.get_employee_data()
            
            # Collect form data
            basic_info = {
                'first_name': self.entries['first_name'].get(),
                'last_name': self.entries['last_name'].get(),
                'hire_date': self.entries['hire_date'].get(),
                'filing_status': self.entries['filing_status'].get().upper(),
                'filing_dependents': int(self.entries['filing_dependents'].get() or 0),
                'pay_rate': self.entries['pay_rate'].get()
            }
            
            # Update only basic info fields in the existing data
            for key, value in basic_info.items():
                existing_data[key] = value

            # Save employee - use the updated existing data
            success, errors = self.employee_ops.save_employee_data(existing_data)
            if success:
                messagebox.showinfo("Success", "Basic information saved successfully!")
                self._on_close()
            else:
                messagebox.showerror("Error", "\n".join(errors))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

class UnionInfoForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.employee_ops = main_app.employee_ops
        self.form_window = None

    def create_form(self):
        """Create the union information form"""
        self.form_window.title("Union Information")
        self.form_window.geometry("400x400")

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
        scrollable_frame.grid_columnconfigure(1, weight=1)

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
            text="UNION INFORMATION",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Load existing data
        employee = self.employee_ops.get_employee_data()
        current_row = 1

        # Union Deductions Frame
        deductions_frame = ttk.LabelFrame(scrollable_frame, text="Union Deductions", padding="10")
        deductions_frame.grid(row=current_row, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        current_row += 1

        # Create union deduction fields
        self.union_deductions = []
        deductions = employee.get('union', {}).get('deductions', [])
        for i, ded in enumerate(deductions):
            ttk.Label(deductions_frame, text=f"{ded.get('name', f'Union Deduction {i+1}')}:").grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(deductions_frame)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.W)
            amount = ded.get('amount', 0) if ded.get('type') == 'fixed' else ded.get('rate', 0) * 100
            entry.insert(0, str(amount))
            self.union_deductions.append(entry)

        # Union Additions Frame
        additions_frame = ttk.LabelFrame(scrollable_frame, text="Union Additions", padding="10")
        additions_frame.grid(row=current_row, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        current_row += 1

        # Create union addition fields
        self.union_additions = []
        additions = employee.get('union', {}).get('additions', [])
        for i, add in enumerate(additions):
            ttk.Label(additions_frame, text=f"{add.get('name', f'Union Addition {i+1}')}:").grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(additions_frame)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.W)
            # Handle different types of additions: fixed, percentage, or per-day
            if add.get('type') in ['fixed', 'per-day']:
                amount = add.get('amount', 0)
            elif add.get('type') == 'percentage':
                amount = add.get('rate', 0) * 100
            else:
                amount = add.get('amount', 0)
            entry.insert(0, str(amount))
            self.union_additions.append(entry)

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self._on_save, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def _on_save(self):
        """Handle save button click"""
        try:
            # Get existing data
            employee_data = self.employee_ops.get_employee_data()

            # Get original deductions and additions to preserve names
            orig_deductions = employee_data.get('union', {}).get('deductions', [])
            orig_additions = employee_data.get('union', {}).get('additions', [])

            # Update union deductions
            deductions = []
            for i, entry in enumerate(self.union_deductions):
                if i < len(orig_deductions):  # Use original name if available
                    name = orig_deductions[i].get('name')
                    category = orig_deductions[i].get('category', 'pre-tax')
                    ded_type = orig_deductions[i].get('type', 'fixed')
                else:
                    name = f"Union Deduction {i+1}"
                    category = "pre-tax"
                    ded_type = 'fixed'
                
                value = entry.get().strip()
                if value:
                    try:
                        amount = float(value)
                        deduction = {
                            'name': name,
                            'category': category,
                            'type': ded_type
                        }
                        
                        # Set amount or rate based on type
                        if ded_type in ['fixed', 'per-day']:
                            deduction['amount'] = amount
                        elif ded_type == 'percentage':
                            deduction['rate'] = amount/100
                            deduction['amount'] = 0.0
                        
                        deductions.append(deduction)
                    except ValueError:
                        pass

            # Update union additions
            additions = []
            for i, entry in enumerate(self.union_additions):
                if i < len(orig_additions):  # Use original name if available
                    name = orig_additions[i].get('name')
                    category = orig_additions[i].get('category', 'pre-tax')
                    add_type = orig_additions[i].get('type', 'fixed')
                else:
                    name = f"Union Addition {i+1}"
                    category = "pre-tax"
                    add_type = 'fixed'
                
                value = entry.get().strip()
                if value:
                    try:
                        amount = float(value)
                        addition = {
                            'name': name,
                            'category': category,
                            'type': add_type
                        }
                        
                        # Set amount or rate based on type
                        if add_type in ['fixed', 'per-day']:
                            addition['amount'] = amount
                        elif add_type == 'percentage':
                            addition['rate'] = amount/100
                            addition['amount'] = 0.0
                        
                        additions.append(addition)
                    except ValueError:
                        pass

            # Update the union section
            employee_data['union'] = {
                'deductions': deductions,
                'additions': additions
            }

            # Save employee
            success, errors = self.employee_ops.save_employee_data(employee_data)
            if success:
                messagebox.showinfo("Success", "Union information saved successfully!")
                self._on_close()
            else:
                messagebox.showerror("Error", "\n".join(errors))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

class DeductionsForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.employee_ops = main_app.employee_ops
        self.form_window = None

    def create_form(self):
        """Create the deductions form"""
        self.form_window.title("Deductions")
        self.form_window.geometry("500x550")

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
            text="DEDUCTIONS",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Load existing data
        employee = self.employee_ops.get_employee_data()
        current_row = 1

        # Special Deductions Frame
        special_frame = ttk.LabelFrame(scrollable_frame, text="Special Deductions", padding="10")
        special_frame.grid(row=current_row, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        current_row += 1

        # Create special deduction fields
        self.special_deductions = []
        special_deds = employee.get('special_deductions', [])
        for i, ded in enumerate(special_deds):
            ttk.Label(special_frame, text=f"{ded.get('name', f'Special Deduction {i+1}')}:").grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(special_frame)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.W)
            # Handle different types of deductions
            if ded.get('type') in ['fixed', 'per-day']:
                amount = ded.get('amount', 0)
            elif ded.get('type') == 'percentage':
                amount = ded.get('rate', 0) * 100
            else:
                amount = ded.get('amount', 0)
            entry.insert(0, str(amount))
            self.special_deductions.append(entry)

        # Payroll Deductions Frame
        payroll_frame = ttk.LabelFrame(scrollable_frame, text="Payroll Deductions", padding="10")
        payroll_frame.grid(row=current_row, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        current_row += 1

        # Create payroll deduction fields
        self.payroll_deductions = []
        payroll_deds = employee.get('payroll_deductions', [])
        for i, ded in enumerate(payroll_deds):
            ttk.Label(payroll_frame, text=f"{ded.get('name', f'Payroll Deduction {i+1}')}:").grid(row=i, column=0, pady=5, padx=5, sticky=tk.W)
            entry = ttk.Entry(payroll_frame)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.W)
            # Handle different types of deductions
            if ded.get('type') in ['fixed', 'per-day']:
                amount = ded.get('amount', 0)
            elif ded.get('type') == 'percentage':
                amount = ded.get('rate', 0) * 100
            else:
                amount = ded.get('amount', 0)
            entry.insert(0, str(amount))
            self.payroll_deductions.append(entry)

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=current_row, column=0, pady=20)

        ttk.Button(button_frame, text="Save", command=self._on_save, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def _on_save(self):
        """Handle save button click"""
        try:
            # Get existing data
            employee_data = self.employee_ops.get_employee_data()

            # Get original deductions to preserve names
            orig_special_deds = employee_data.get('special_deductions', [])
            orig_payroll_deds = employee_data.get('payroll_deductions', [])

            # Update special deductions
            special_deds = []
            for i, entry in enumerate(self.special_deductions):
                if i < len(orig_special_deds):  # Use original name if available
                    name = orig_special_deds[i].get('name')
                    category = orig_special_deds[i].get('category', 'pre-tax')
                    ded_type = orig_special_deds[i].get('type', 'fixed')
                else:
                    name = f"Special Deduction {i+1}"
                    category = "pre-tax"
                    ded_type = 'fixed'
                
                value = entry.get().strip()
                if value:
                    try:
                        amount = float(value)
                        deduction = {
                            'name': name,
                            'category': category,
                            'type': ded_type
                        }
                        
                        # Set amount or rate based on type
                        if ded_type in ['fixed', 'per-day']:
                            deduction['amount'] = amount
                        elif ded_type == 'percentage':
                            deduction['rate'] = amount/100
                            deduction['amount'] = 0.0
                        
                        special_deds.append(deduction)
                    except ValueError:
                        pass

            # Update payroll deductions
            payroll_deds = []
            for i, entry in enumerate(self.payroll_deductions):
                if i < len(orig_payroll_deds):  # Use original name if available
                    name = orig_payroll_deds[i].get('name')
                    category = orig_payroll_deds[i].get('category', 'post-tax')
                    ded_type = orig_payroll_deds[i].get('type', 'fixed')
                else:
                    name = f"Payroll Deduction {i+1}"
                    category = "post-tax"
                    ded_type = 'fixed'
                
                value = entry.get().strip()
                if value:
                    try:
                        amount = float(value)
                        deduction = {
                            'name': name,
                            'category': category,
                            'type': ded_type
                        }
                        
                        # Set amount or rate based on type
                        if ded_type in ['fixed', 'per-day']:
                            deduction['amount'] = amount
                        elif ded_type == 'percentage':
                            deduction['rate'] = amount/100
                            deduction['amount'] = 0.0
                        
                        payroll_deds.append(deduction)
                    except ValueError:
                        pass

            # Update the deductions sections
            employee_data['special_deductions'] = special_deds
            employee_data['payroll_deductions'] = payroll_deds

            # Save employee
            success, errors = self.employee_ops.save_employee_data(employee_data)
            if success:
                messagebox.showinfo("Success", "Deductions saved successfully!")
                self._on_close()
            else:
                messagebox.showerror("Error", "\n".join(errors))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}") 