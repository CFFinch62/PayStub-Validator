from datetime import datetime

class EmployeeOperations:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def validate_employee_data(self, employee_data):
        """Validate employee data before saving"""
        errors = []
        
        # Required fields
        if not employee_data.get('first_name'):
            errors.append("First name is required")
        if not employee_data.get('last_name'):
            errors.append("Last name is required")
        if not employee_data.get('hire_date'):
            errors.append("Hire date is required")
        if not employee_data.get('filing_status'):
            errors.append("Filing status is required")
        if not employee_data.get('pay_rate'):
            errors.append("Pay rate is required")

        # Validate filing status
        if employee_data.get('filing_status') not in ['S', 'M']:
            errors.append("Filing status must be 'S' or 'M'")

        # Validate hire date format
        try:
            datetime.strptime(employee_data.get('hire_date', ''), "%Y-%m-%d")
        except ValueError:
            errors.append("Hire date must be in YYYY-MM-DD format")

        # Validate pay rate
        try:
            float(employee_data.get('pay_rate', 0))
        except ValueError:
            errors.append("Pay rate must be a valid number")

        # Validate filing dependents
        try:
            int(employee_data.get('filing_dependents', 0))
        except ValueError:
            errors.append("Filing dependents must be a valid number")

        # Validate union data structure
        if 'union' not in employee_data:
            errors.append("Union data structure is required")
        else:
            # Validate union additions
            for addition in employee_data['union'].get('additions', []):
                if not addition.get('name'):
                    errors.append("Union addition name is required")
                if not addition.get('category'):
                    errors.append("Union addition category is required")
                if not addition.get('type'):
                    errors.append("Union addition type is required")
                if addition.get('type') in ['fixed', 'per-day']:
                    try:
                        float(addition.get('amount', 0))
                    except ValueError:
                        errors.append(f"Invalid amount for union addition {addition.get('name', 'Unknown')}")
                elif addition.get('type') == 'percentage':
                    try:
                        float(addition.get('rate', 0))
                    except ValueError:
                        errors.append(f"Invalid rate for union addition {addition.get('name', 'Unknown')}")

            # Validate union deductions
            for deduction in employee_data['union'].get('deductions', []):
                if not deduction.get('name'):
                    errors.append("Union deduction name is required")
                if not deduction.get('category'):
                    errors.append("Union deduction category is required")
                if not deduction.get('type'):
                    errors.append("Union deduction type is required")
                if deduction.get('type') in ['fixed', 'per-day']:
                    try:
                        float(deduction.get('amount', 0))
                    except ValueError:
                        errors.append(f"Invalid amount for union deduction {deduction.get('name', 'Unknown')}")
                elif deduction.get('type') == 'percentage':
                    try:
                        float(deduction.get('rate', 0))
                    except ValueError:
                        errors.append(f"Invalid rate for union deduction {deduction.get('name', 'Unknown')}")

        # Validate special deductions
        for deduction in employee_data.get('special_deductions', []):
            if not deduction.get('name'):
                errors.append("Special deduction name is required")
            if not deduction.get('category'):
                errors.append("Special deduction category is required")
            if not deduction.get('type'):
                errors.append("Special deduction type is required")
            if deduction.get('type') in ['fixed', 'per-day']:
                try:
                    float(deduction.get('amount', 0))
                except ValueError:
                    errors.append(f"Invalid amount for special deduction {deduction.get('name', 'Unknown')}")
            elif deduction.get('type') == 'percentage':
                try:
                    float(deduction.get('rate', 0))
                except ValueError:
                    errors.append(f"Invalid rate for special deduction {deduction.get('name', 'Unknown')}")

        # Validate payroll deductions
        for deduction in employee_data.get('payroll_deductions', []):
            if not deduction.get('name'):
                errors.append("Payroll deduction name is required")
            if not deduction.get('category'):
                errors.append("Payroll deduction category is required")
            if not deduction.get('type'):
                errors.append("Payroll deduction type is required")
            if deduction.get('type') in ['fixed', 'per-day']:
                try:
                    float(deduction.get('amount', 0))
                except ValueError:
                    errors.append(f"Invalid amount for payroll deduction {deduction.get('name', 'Unknown')}")
            elif deduction.get('type') == 'percentage':
                try:
                    float(deduction.get('rate', 0))
                except ValueError:
                    errors.append(f"Invalid rate for payroll deduction {deduction.get('name', 'Unknown')}")

        return errors

    def get_employee_data(self):
        """Get the current employee data or return default values if none exists"""
        # Get default structure
        default_data = {
            'first_name': '',
            'last_name': '',
            'hire_date': '',
            'filing_status': '',
            'filing_dependents': '0',
            'pay_rate': '',
            'union': {
                'additions': [
                    {
                        'name': "Union Pension",
                        'category': "pre-tax",
                        'type': "percentage",
                        'rate': 0.05,
                        'amount': 0.0
                    },
                    {
                        'name': "Union Vacation",
                        'category': "pre-tax",
                        'type': "percentage",
                        'rate': 0.04,
                        'amount': 0.0
                    }
                ],
                'deductions': [
                    {
                        'name': "Union Dues",
                        'category': "pre-tax",
                        'type': "percentage",
                        'rate': 0.01779,
                        'amount': 0.0
                    },
                    {
                        'name': "Union Health Insurance",
                        'category': "pre-tax",
                        'type': "fixed",
                        'amount': 25.00
                    }
                ]
            },
            'special_deductions': [
                {
                    'name': "401(k) Contribution",
                    'category': "pre-tax",
                    'type': "percentage",
                    'rate': 0.06,
                    'amount': 0.0
                },
                {
                    'name': "Health Savings Account",
                    'category': "pre-tax",
                    'type': "fixed",
                    'amount': 50.00
                }
            ],
            'payroll_deductions': [
                {
                    'name': "Federal Tax",
                    'category': "post-tax",
                    'type': "percentage",
                    'rate': 0.22,
                    'amount': 0.0
                },
                {
                    'name': "State Tax",
                    'category': "post-tax",
                    'type': "percentage",
                    'rate': 0.05,
                    'amount': 0.0
                },
                {
                    'name': "Social Security",
                    'category': "post-tax",
                    'type': "percentage",
                    'rate': 0.062,
                    'amount': 0.0
                },
                {
                    'name': "Medicare",
                    'category': "post-tax",
                    'type': "percentage",
                    'rate': 0.0145,
                    'amount': 0.0
                }
            ]
        }

        # If we have existing data, merge it with defaults
        if self.data_manager.employee:
            # Deep merge the data
            merged_data = default_data.copy()
            for key, value in self.data_manager.employee.items():
                if isinstance(value, dict) and key in merged_data and isinstance(merged_data[key], dict):
                    # For nested dictionaries (like union, deductions), merge their contents
                    merged_data[key].update(value)
                else:
                    merged_data[key] = value
            return merged_data

        return default_data

    def save_employee_data(self, employee_data):
        """Save employee data"""
        errors = self.validate_employee_data(employee_data)
        if errors:
            return False, errors
        
        # Get existing data to preserve other sections
        existing_data = self.get_employee_data()
        if existing_data:
            # Create a deep copy of the existing data
            merged_data = existing_data.copy()
            
            # Update only the sections that were changed
            for key, value in employee_data.items():
                # Special handling for nested structures
                if isinstance(value, dict) and key in merged_data and isinstance(merged_data[key], dict):
                    # For nested dictionaries (like union), merge their contents
                    for sub_key, sub_value in value.items():
                        merged_data[key][sub_key] = sub_value
                else:
                    merged_data[key] = value
            
            employee_data = merged_data
        
        # Save the employee data
        self.data_manager.employee = employee_data
        self.data_manager._save_data()
        return True, []

    def add_deduction(self, employee_data, deduction_type, deduction_data):
        """Add a new deduction to the specified category"""
        if deduction_type == 'union':
            employee_data['union']['deductions'].append(deduction_data)
        elif deduction_type == 'special':
            employee_data['special_deductions'].append(deduction_data)
        elif deduction_type == 'payroll':
            employee_data['payroll_deductions'].append(deduction_data)
        return employee_data

    def remove_deduction(self, employee_data, deduction_type, deduction_id):
        """Remove a deduction by its ID"""
        if deduction_type == 'union':
            employee_data['union']['deductions'] = [
                d for d in employee_data['union']['deductions']
                if d.get('id') != deduction_id
            ]
        elif deduction_type == 'special':
            employee_data['special_deductions'] = [
                d for d in employee_data['special_deductions']
                if d.get('id') != deduction_id
            ]
        elif deduction_type == 'payroll':
            employee_data['payroll_deductions'] = [
                d for d in employee_data['payroll_deductions']
                if d.get('id') != deduction_id
            ]
        return employee_data

    def add_union_addition(self, employee_data, addition_data):
        """Add a new union addition"""
        employee_data['union']['additions'].append(addition_data)
        return employee_data

    def remove_union_addition(self, employee_data, addition_id):
        """Remove a union addition by its ID"""
        employee_data['union']['additions'] = [
            a for a in employee_data['union']['additions']
            if a.get('id') != addition_id
        ]
        return employee_data 