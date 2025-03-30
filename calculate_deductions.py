from datetime import datetime

def calculate_deductions(gross_pay, employee, days_worked):
    """Calculate all deductions for an employee's paycheck"""
    deductions = {}
    pre_tax_total = 0.0
    
    # Calculate pre-tax deductions first
    # Union additions
    for addition in employee['union']['additions']:
        name = addition['name']
        if addition['type'] == 'fixed':
            amount = addition['amount']
        elif addition['type'] == 'per-day':
            amount = addition['amount'] * days_worked
        elif addition['type'] == 'percentage':
            amount = gross_pay * addition['rate']
        else:
            # Default to fixed amount if type is unknown
            amount = addition.get('amount', 0)
        deductions[name] = amount
        
    # Union deductions
    for deduction in employee['union']['deductions']:
        name = deduction['name']
        if deduction['type'] == 'fixed':
            amount = deduction['amount']
        elif deduction['type'] == 'per-day':
            amount = deduction['amount'] * days_worked
        elif deduction['type'] == 'percentage':
            amount = gross_pay * deduction['rate']
        else:
            # Default to fixed amount if type is unknown
            amount = deduction.get('amount', 0)
        deductions[name] = amount
        pre_tax_total += amount

    # Special deductions
    for deduction in employee['special_deductions']:
        name = deduction['name']
        if deduction['type'] == 'fixed':
            amount = deduction['amount']
        elif deduction['type'] == 'per-day':
            amount = deduction['amount'] * days_worked
        elif deduction['type'] == 'percentage':
            amount = gross_pay * deduction['rate']
        else:
            # Default to fixed amount if type is unknown
            amount = deduction.get('amount', 0)
        deductions[name] = amount
        pre_tax_total += amount

    # Calculate adjusted gross pay
    adj_gross = gross_pay - pre_tax_total

    # Calculate post-tax deductions
    for deduction in employee['payroll_deductions']:
        name = deduction['name']
        if deduction['type'] == 'fixed':
            amount = deduction['amount']
        elif deduction['type'] == 'per-day':
            amount = deduction['amount'] * days_worked
        elif deduction['type'] == 'percentage':
            amount = adj_gross * deduction['rate']
        else:
            # Default to fixed amount if type is unknown
            amount = deduction.get('amount', 0)
        deductions[name] = amount

    return deductions 