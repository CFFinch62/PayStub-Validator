from datetime import datetime
from calculate_wages import calculate_wages
from calculate_deductions import calculate_deductions

class PaystubOperations:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def validate_paystub_data(self, paystub_data):
        """Validate paystub data"""
        if not paystub_data.get('week_end'):
            raise ValueError("Week start date is required")
            
        try:
            datetime.strptime(paystub_data['week_end'], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if not paystub_data.get('hours'):
            raise ValueError("Hours data is required")

        if not paystub_data.get('wages'):
            raise ValueError("Wages data is required")

        if not paystub_data.get('pre_tax_deductions'):
            raise ValueError("Pre-tax deductions data is required")

        if not paystub_data.get('post_tax_deductions'):
            raise ValueError("Post-tax deductions data is required")

        if not paystub_data.get('pay'):
            raise ValueError("Pay data is required")

    def calculate_hours(self, timesheet):
        """Calculate hours from timesheet data"""
        hours = {
            'Regular': 0.0,
            'Regular OT': 0.0,
            'Holiday': 0.0,
            'Holiday OT': 0.0,
            'Vacation': 0.0,
            'Sick': 0.0,
            'Differential': 0.0
        }

        for entry in timesheet['entries'].values():
            # Skip if no time in/out
            if not entry['time_in'] or not entry['time_out']:
                continue

            # Calculate daily hours from time in/out
            time_in = datetime.strptime(entry['time_in'], "%H:%M")
            time_out = datetime.strptime(entry['time_out'], "%H:%M")
            daily_hours = (time_out - time_in).total_seconds() / 3600
            
            # Add vacation and sick hours
            hours['Vacation'] += float(entry['vacation_hours'])
            hours['Sick'] += float(entry['sick_hours'])
            
            # Calculate regular vs OT hours
            if entry['is_holiday']:
                if daily_hours <= 7:
                    hours['Holiday'] += daily_hours
                else:
                    hours['Holiday'] += 7
                    hours['Holiday OT'] += daily_hours - 7
            else:
                current_regular = hours['Regular']
                if current_regular < 37.5:
                    if current_regular + daily_hours <= 37.5:
                        hours['Regular'] += daily_hours
                    else:
                        hours['Regular'] += (37.5 - current_regular)
                        hours['Regular OT'] += (current_regular + daily_hours - 37.5)
                else:
                    hours['Regular OT'] += daily_hours

            # Calculate differential (night hours)
            if time_in.hour >= 17 or time_out.hour < 7:
                hours['Differential'] += daily_hours

        return hours

    def generate_paystub(self, timesheet):
        """Generate a new paystub"""
        try:
            employee = self.data_manager.employee
            if not employee:
                return False, "Employee not found."

            # Calculate hours
            hours = self.calculate_hours(timesheet)
            
            # Calculate days worked
            days_worked = len([entry for entry in timesheet['entries'].values() 
                             if entry['time_in'] and entry['time_out']])

            # Calculate wages
            wages = calculate_wages(hours, float(employee['pay_rate']))
            
            # Calculate gross pay
            gross_pay = sum(wages.values())
            
            # Calculate deductions
            deductions = calculate_deductions(gross_pay, employee, days_worked)
            
            # Organize deductions into pre-tax and post-tax, and separate additions
            pre_tax_deductions = {}
            post_tax_deductions = {}
            additions = {}
            
            for deduction_id, amount in deductions.items():
                if deduction_id in ['401K% T', 'UNION N', 'UN INST', 'AFLCNTT', 'WILTONN']:
                    pre_tax_deductions[deduction_id] = amount
                elif deduction_id in ['LONGEVT', 'MEALS N', 'TRAVELN']:
                    additions[deduction_id] = amount
                else:
                    post_tax_deductions[deduction_id] = amount

            # Add DIS-SUI deduction
            post_tax_deductions['DIS-SUI'] = 0.60

            # Calculate total pre-tax deductions
            total_pre_tax = sum(pre_tax_deductions.values())
            
            # Calculate adjusted gross (gross - pre-tax deductions)
            adjusted_gross = gross_pay - total_pre_tax
            
            # Calculate total post-tax deductions
            total_post_tax = sum(post_tax_deductions.values())
            
            # Calculate total additions
            total_additions = sum(additions.values())
            
            # Calculate net pay (adjusted gross - post-tax deductions + additions)
            net_pay = adjusted_gross - total_post_tax + total_additions
            
            # Create paystub data
            paystub_data = {
                'week_end': timesheet['week_end'],
                'hours': hours,
                'wages': wages,
                'pay': {
                    'gross': gross_pay,
                    'adjusted_gross': adjusted_gross,
                    'net': net_pay
                },
                'pre_tax_deductions': pre_tax_deductions,
                'post_tax_deductions': post_tax_deductions,
                'additions': additions
            }

            self.validate_paystub_data(paystub_data)
            self.data_manager.add_paystub(paystub_data)
            return True, "Paystub generated successfully!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def get_paystub_details(self, week_end):
        """Get paystub details"""
        try:
            paystub = self.data_manager.get_paystub(week_end)
            if not paystub:
                return False, "Paystub not found."
            return True, paystub
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def get_employee_paystubs(self):
        """Get all paystubs for the employee"""
        try:
            paystubs = self.data_manager.get_paystubs()
            return True, paystubs
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def delete_paystub(self, week_end):
        """Delete a paystub by week start date"""
        try:
            # Check if paystub exists
            paystub = self.data_manager.get_paystub(week_end)
            if not paystub:
                return False, "Paystub not found."
                
            # Delete the paystub
            success = self.data_manager.delete_paystub(week_end)
            if success:
                return True, "Paystub deleted successfully!"
            else:
                return False, "Failed to delete paystub."
        except Exception as e:
            return False, f"An error occurred: {str(e)}"