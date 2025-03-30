from datetime import datetime

class TimesheetOperations:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def validate_timesheet_data(self, timesheet_data):
        """Validate timesheet data"""
        if not timesheet_data.get('week_end'):
            raise ValueError("Week start date is required")
            
        try:
            datetime.strptime(timesheet_data['week_end'], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if not timesheet_data.get('entries'):
            raise ValueError("Daily entries are required")

        for day, entry in timesheet_data['entries'].items():
            if not all(key in entry for key in ['time_in', 'time_out']):
                raise ValueError(f"Missing required fields for {day}")
            
            if not isinstance(entry.get('is_holiday', False), bool):
                raise ValueError(f"Invalid holiday format for {day}")
            
            if not isinstance(entry.get('vacation_hours', 0), (int, float, str)):
                raise ValueError(f"Invalid vacation hours format for {day}")
            
            if not isinstance(entry.get('sick_hours', 0), (int, float, str)):
                raise ValueError(f"Invalid sick hours format for {day}")

    def add_timesheet(self, timesheet_data):
        """Add a new timesheet"""
        try:
            self.validate_timesheet_data(timesheet_data)
            self.data_manager.add_timesheet(timesheet_data)
            return True, "Timesheet added successfully!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def get_timesheet(self, week_end):
        """Get timesheet by week start date"""
        try:
            timesheet = self.data_manager.get_timesheet(week_end)
            if not timesheet:
                return None
            return timesheet
        except Exception as e:
            return None

    def delete_timesheet(self, week_end):
        """Delete a timesheet"""
        try:
            if self.data_manager.delete_timesheet(week_end):
                return True, "Timesheet deleted successfully!"
            return False, "Timesheet not found."
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def get_timesheets(self):
        """Get all timesheets"""
        try:
            timesheets = self.data_manager.get_timesheets()
            return True, timesheets
        except Exception as e:
            return False, f"An error occurred: {str(e)}"