import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .base_form import BaseForm
from ..gui_utils import center_elements

class EnterTimesheetForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.timesheet_ops = main_app.timesheet_ops

    def create_form(self):
        """Create the enter timesheet form"""
        self.form_window.title("Enter Timesheet")
        self.form_window.geometry("500x500")  # Larger size to show all content
        self.form_window.resizable(False, False)  # Prevent resizing

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
            text="ENTER TIMESHEET",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Week end date frame
        date_frame = ttk.LabelFrame(scrollable_frame, text="Week End Date", padding="10")
        date_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        ttk.Label(date_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        week_end_entry = ttk.Entry(date_frame)
        week_end_entry.grid(row=0, column=1, padx=5)

        # Timesheet frame
        timesheet_frame = ttk.LabelFrame(scrollable_frame, text="Daily Entries", padding="10")
        timesheet_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        # Days of the week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_entries = {}

        # Create headers
        ttk.Label(timesheet_frame, text="Day").grid(row=0, column=0, padx=5)
        ttk.Label(timesheet_frame, text="Time In").grid(row=0, column=1, padx=5)
        ttk.Label(timesheet_frame, text="Time Out").grid(row=0, column=2, padx=5)
        ttk.Label(timesheet_frame, text="Holiday").grid(row=0, column=3, padx=5)
        ttk.Label(timesheet_frame, text="Vacation").grid(row=0, column=4, padx=5)
        ttk.Label(timesheet_frame, text="Sick").grid(row=0, column=5, padx=5)

        # Create daily entry fields
        for idx, day in enumerate(days):
            ttk.Label(timesheet_frame, text=day).grid(row=idx+1, column=0, padx=5)
            time_in = ttk.Entry(timesheet_frame, width=10)
            time_in.grid(row=idx+1, column=1, padx=5)
            time_out = ttk.Entry(timesheet_frame, width=10)
            time_out.grid(row=idx+1, column=2, padx=5)
            is_holiday = tk.BooleanVar()
            ttk.Checkbutton(timesheet_frame, text="", variable=is_holiday).grid(row=idx+1, column=3, padx=5)
            vacation = ttk.Entry(timesheet_frame, width=5)
            vacation.grid(row=idx+1, column=4, padx=5)
            sick = ttk.Entry(timesheet_frame, width=5)
            sick.grid(row=idx+1, column=5, padx=5)
            
            daily_entries[day] = {
                'time_in': time_in,
                'time_out': time_out,
                'is_holiday': is_holiday,
                'vacation': vacation,
                'sick': sick
            }

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=3, column=0, pady=20)

        def save_timesheet():
            try:
                week_end = week_end_entry.get().strip()
                if not week_end:
                    messagebox.showerror("Error", "Please enter a week end date")
                    return

                # Validate date format
                try:
                    datetime.strptime(week_end, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                    return

                # Collect daily entries
                entries = {}
                for day, fields in daily_entries.items():
                    entries[day] = {
                        'time_in': fields['time_in'].get().strip(),
                        'time_out': fields['time_out'].get().strip(),
                        'is_holiday': fields['is_holiday'].get(),
                        'vacation_hours': fields['vacation'].get().strip() or '0',
                        'sick_hours': fields['sick'].get().strip() or '0'
                    }

                # Save timesheet
                success, message = self.timesheet_ops.add_timesheet({
                    'week_end': week_end,
                    'entries': entries
                })
                if success:
                    messagebox.showinfo("Success", message)
                    self._on_close()
                else:
                    messagebox.showerror("Error", message)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        ttk.Button(button_frame, text="Save", command=save_timesheet, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')

class EditTimesheetForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.timesheet_ops = main_app.timesheet_ops

    def create_form(self):
        """Create the edit timesheet form"""
        self.form_window.title("Edit Timesheet")
        self.form_window.geometry("500x350")  # Larger size to show all content
        self.form_window.resizable(False, False)  # Prevent resizing

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
            text="EDIT TIMESHEET",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Timesheet selection frame
        select_frame = ttk.LabelFrame(scrollable_frame, text="Select Timesheet", padding="10")
        select_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        timesheet_listbox = tk.Listbox(select_frame, width=50, height=5)
        timesheet_listbox.grid(row=0, column=0, padx=5, pady=5)

        # Load timesheets
        timesheets = self.data_manager.get_timesheets()
        for timesheet in timesheets:
            timesheet_listbox.insert(tk.END, timesheet['week_end'])

        # Timesheet frame (initially hidden)
        timesheet_frame = ttk.LabelFrame(scrollable_frame, text="Daily Entries", padding="10")
        daily_entries = {}

        # Days of the week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create headers
        ttk.Label(timesheet_frame, text="Day").grid(row=0, column=0, padx=5)
        ttk.Label(timesheet_frame, text="Time In").grid(row=0, column=1, padx=5)
        ttk.Label(timesheet_frame, text="Time Out").grid(row=0, column=2, padx=5)
        ttk.Label(timesheet_frame, text="Holiday").grid(row=0, column=3, padx=5)
        ttk.Label(timesheet_frame, text="Vacation").grid(row=0, column=4, padx=5)
        ttk.Label(timesheet_frame, text="Sick").grid(row=0, column=5, padx=5)

        # Create daily entry fields
        for idx, day in enumerate(days):
            ttk.Label(timesheet_frame, text=day).grid(row=idx+1, column=0, padx=5)
            time_in = ttk.Entry(timesheet_frame, width=10)
            time_in.grid(row=idx+1, column=1, padx=5)
            time_out = ttk.Entry(timesheet_frame, width=10)
            time_out.grid(row=idx+1, column=2, padx=5)
            is_holiday = tk.BooleanVar()
            ttk.Checkbutton(timesheet_frame, text="", variable=is_holiday).grid(row=idx+1, column=3, padx=5)
            vacation = ttk.Entry(timesheet_frame, width=5)
            vacation.grid(row=idx+1, column=4, padx=5)
            sick = ttk.Entry(timesheet_frame, width=5)
            sick.grid(row=idx+1, column=5, padx=5)
            
            daily_entries[day] = {
                'time_in': time_in,
                'time_out': time_out,
                'is_holiday': is_holiday,
                'vacation': vacation,
                'sick': sick
            }

        def load_timesheet():
            selection = timesheet_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a timesheet to edit")
                return

            week_end = timesheet_listbox.get(selection[0])
            success, result = self.timesheet_ops.get_timesheet_details(week_end)
            
            if not success:
                messagebox.showerror("Error", result)
                return

            timesheet = result

            for day, entries in timesheet['entries'].items():
                if day in daily_entries:
                    daily_entries[day]['time_in'].delete(0, tk.END)
                    daily_entries[day]['time_in'].insert(0, entries.get('time_in', ''))
                    daily_entries[day]['time_out'].delete(0, tk.END)
                    daily_entries[day]['time_out'].insert(0, entries.get('time_out', ''))
                    daily_entries[day]['is_holiday'].set(entries.get('is_holiday', False))
                    daily_entries[day]['vacation'].delete(0, tk.END)
                    daily_entries[day]['vacation'].insert(0, entries.get('vacation_hours', '0'))
                    daily_entries[day]['sick'].delete(0, tk.END)
                    daily_entries[day]['sick'].insert(0, entries.get('sick_hours', '0'))

            # Show the timesheet frame
            timesheet_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        def save_timesheet():
            selection = timesheet_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a timesheet to edit")
                return

            week_end = timesheet_listbox.get(selection[0])
            
            try:
                # Collect daily entries
                entries = {}
                for day, fields in daily_entries.items():
                    entries[day] = {
                        'time_in': fields['time_in'].get().strip(),
                        'time_out': fields['time_out'].get().strip(),
                        'is_holiday': fields['is_holiday'].get(),
                        'vacation_hours': fields['vacation'].get().strip() or '0',
                        'sick_hours': fields['sick'].get().strip() or '0'
                    }

                # Save timesheet
                success, message = self.timesheet_ops.add_timesheet({
                    'week_end': week_end,
                    'entries': entries
                })
                if success:
                    messagebox.showinfo("Success", message)
                    self._on_close()
                else:
                    messagebox.showerror("Error", message)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=3, column=0, pady=20)

        ttk.Button(button_frame, text="Load", command=load_timesheet, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save", command=save_timesheet, width=15).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=2, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')

class DeleteTimesheetForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.timesheet_ops = main_app.timesheet_ops

    def create_form(self):
        """Create the delete timesheet form"""
        self.form_window.title("Delete Timesheet")
        self.form_window.geometry("500x350")  # Smaller size since it's just a list and buttons
        self.form_window.resizable(False, False)  # Prevent resizing

        # Create main container
        container = ttk.Frame(self.form_window, padding="20")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(
            container,
            text="DELETE TIMESHEET",
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

        def delete_timesheet():
            selection = timesheet_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a timesheet to delete")
                return

            week_end = timesheet_listbox.get(selection[0])
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the timesheet for week ending {week_end}?"):
                success, message = self.timesheet_ops.delete_timesheet(week_end)
                if success:
                    messagebox.showinfo("Success", message)
                    self._on_close()
                else:
                    messagebox.showerror("Error", message)

        # Buttons
        button_frame = ttk.Frame(container)
        button_frame.grid(row=2, column=0, pady=20)

        ttk.Button(button_frame, text="Delete", command=delete_timesheet, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')

class DisplayTimesheetForm(BaseForm):
    def __init__(self, main_app):
        super().__init__(main_app)
        self.data_manager = main_app.data_manager
        self.timesheet_ops = main_app.timesheet_ops

    def create_form(self):
        """Create the display timesheet form"""
        self.form_window.title("Display Timesheet")
        self.form_window.geometry("500x600")  # Increased width from 370 to 800

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
            text="TIMESHEETS",
            font=('Helvetica', 16, 'bold')
        )
        title.grid(row=0, column=0, pady=20)

        # Timesheet list
        timesheet_frame = ttk.LabelFrame(scrollable_frame, text="Select Timesheet", padding="10")
        timesheet_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)

        # Configure grid weights for timesheet frame
        timesheet_frame.grid_columnconfigure(0, weight=1)
        timesheet_frame.grid_rowconfigure(0, weight=1)

        # Create listbox for timesheets
        timesheet_listbox = tk.Listbox(timesheet_frame, height=5)
        timesheet_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Add scrollbar to listbox
        listbox_scrollbar = ttk.Scrollbar(timesheet_frame, orient="vertical", command=timesheet_listbox.yview)
        listbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        timesheet_listbox.configure(yscrollcommand=listbox_scrollbar.set)

        # Populate timesheet list
        timesheets = self.data_manager.get_timesheets()
        for timesheet in timesheets:
            timesheet_listbox.insert(tk.END, timesheet['week_end'])

        # Display frame for timesheet details
        display_frame = ttk.Frame(scrollable_frame)
        display_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        def display_timesheet():
            selection = timesheet_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a timesheet to display")
                return

            week_end = timesheet_listbox.get(selection[0])
            
            try:
                timesheet = self.timesheet_ops.get_timesheet(week_end)
                if not timesheet:
                    messagebox.showerror("Error", "Timesheet not found")
                    return

                # Clear previous display
                for widget in display_frame.winfo_children():
                    widget.destroy()

                # Display timesheet details
                row = 0
                ttk.Label(display_frame, text="Week Ending:", font=('Helvetica', 12, 'bold')).grid(row=row, column=0, pady=5)
                ttk.Label(display_frame, text=timesheet['week_end']).grid(row=row, column=1, pady=5)
                row += 1

                # Create entries frame
                entries_frame = ttk.LabelFrame(display_frame, text="Daily Entries", padding="10")
                entries_frame.grid(row=row, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
                row += 1

                # Configure column widths
                for i in range(6):  # 6 columns for Date, Time In, Time Out, Vacation, Sick, Holiday
                    entries_frame.grid_columnconfigure(i, weight=1)

                # Headers
                ttk.Label(entries_frame, text="Date", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=5, padx=10)
                ttk.Label(entries_frame, text="Time In", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, pady=5, padx=10)
                ttk.Label(entries_frame, text="Time Out", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, pady=5, padx=10)
                ttk.Label(entries_frame, text="Vacation", font=('Helvetica', 10, 'bold')).grid(row=0, column=3, pady=5, padx=10)
                ttk.Label(entries_frame, text="Sick", font=('Helvetica', 10, 'bold')).grid(row=0, column=4, pady=5, padx=10)
                ttk.Label(entries_frame, text="Holiday", font=('Helvetica', 10, 'bold')).grid(row=0, column=5, pady=5, padx=10)

                # Display entries
                for i, (date, entry) in enumerate(timesheet['entries'].items(), start=1):
                    ttk.Label(entries_frame, text=date).grid(row=i, column=0, pady=2, padx=10)
                    ttk.Label(entries_frame, text=entry['time_in'] or '').grid(row=i, column=1, pady=2, padx=10)
                    ttk.Label(entries_frame, text=entry['time_out'] or '').grid(row=i, column=2, pady=2, padx=10)
                    ttk.Label(entries_frame, text=entry['vacation_hours']).grid(row=i, column=3, pady=2, padx=10)
                    ttk.Label(entries_frame, text=entry['sick_hours']).grid(row=i, column=4, pady=2, padx=10)
                    ttk.Label(entries_frame, text="Yes" if entry['is_holiday'] else "No").grid(row=i, column=5, pady=2, padx=10)

                # Show the display frame
                display_frame.grid()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=3, column=0, pady=20)

        ttk.Button(button_frame, text="Display", command=display_timesheet, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Close", command=self._on_close, width=15).grid(row=0, column=1, padx=5)

        # Center the window on the screen
        self.form_window.update_idletasks()
        width = self.form_window.winfo_width()
        height = self.form_window.winfo_height()
        x = (self.form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.form_window.winfo_screenheight() // 2) - (height // 2)
        self.form_window.geometry(f'+{x}+{y}')

class PrintTimesheetForm(DisplayTimesheetForm):
    def create_form(self):
        """Create the print timesheet form"""
        super().create_form()
        # Add print button
        ttk.Button(self.button_frame, text="Print", command=self.print_timesheet, width=15).grid(row=0, column=2, padx=5)

    def print_timesheet(self):
        """Print the selected timesheet"""
        # TODO: Implement printing functionality
        messagebox.showinfo("Print", "Printing functionality to be implemented")