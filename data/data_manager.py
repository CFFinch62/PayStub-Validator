import json
import os
from datetime import datetime
from pathlib import Path

class DataManager:
    def __init__(self):
        # Create data directory if it doesn't exist
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
        # Define file paths
        self.employee_file = self.data_dir / 'employees.json'
        self.timesheet_file = self.data_dir / 'timesheets.json'
        self.paystub_file = self.data_dir / 'paystubs.json'
        
        # Initialize data stores
        self.employee = None
        self.timesheets = {}
        self.paystubs = {}
        self._load_data()

    def _load_data(self):
        """Load all data from JSON files."""
        try:
            # Load employee data
            if self.employee_file.exists():
                with open(self.employee_file, 'r') as f:
                    data = json.load(f)
                    self.employee = data.get('Employee', None)

            # Load timesheets
            if self.timesheet_file.exists():
                with open(self.timesheet_file, 'r') as f:
                    self.timesheets = json.load(f)

            # Load paystubs
            if self.paystub_file.exists():
                with open(self.paystub_file, 'r') as f:
                    self.paystubs = json.load(f)
        except Exception as e:
            print(f"Error loading data: {str(e)}")

    def _save_data(self):
        """Save all data to JSON files."""
        try:
            # Save employee data
            with open(self.employee_file, 'w') as f:
                json.dump({'Employee': self.employee}, f, indent=4)

            # Save timesheets
            with open(self.timesheet_file, 'w') as f:
                json.dump(self.timesheets, f, indent=4)

            # Save paystubs
            with open(self.paystub_file, 'w') as f:
                json.dump(self.paystubs, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    # Timesheet operations
    def add_timesheet(self, timesheet_data):
        """Add or update timesheet"""
        key = f"Employee_{timesheet_data['week_end']}"
        self.timesheets[key] = timesheet_data
        self._save_data()

    def get_timesheet(self, week_end):
        """Get timesheet by week start date"""
        key = f"Employee_{week_end}"
        return self.timesheets.get(key)

    def delete_timesheet(self, week_end):
        """Delete timesheet"""
        key = f"Employee_{week_end}"
        if key in self.timesheets:
            del self.timesheets[key]
            self._save_data()
            return True
        return False

    def get_timesheets(self):
        """Get all timesheets"""
        # Filter out the "timesheets" key and return only the actual timesheet data
        return [timesheet for key, timesheet in self.timesheets.items() 
                if key != "timesheets" and isinstance(timesheet, dict)]

    # Paystub operations
    def add_paystub(self, paystub_data):
        """Add or update paystub"""
        key = f"Employee_{paystub_data['week_end']}"
        self.paystubs[key] = paystub_data
        self._save_data()

    def get_paystub(self, week_end):
        """Get paystub by week start date"""
        key = f"Employee_{week_end}"
        return self.paystubs.get(key)

    def delete_paystub(self, week_end):
        """Delete paystub"""
        key = f"Employee_{week_end}"
        if key in self.paystubs:
            del self.paystubs[key]
            self._save_data()
            return True
        return False

    def get_paystubs(self):
        """Get all paystubs"""
        return list(self.paystubs.values())

