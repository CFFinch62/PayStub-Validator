DIFF_RATE = 1.4186

def calculate_wages(hours, reg_rate):
    """ Calculate gross wages based upon hours worked
        Consumes: dict (hours), float (reg_rate)
        Returns: dict (wages)
    """
    wages = {
        'Regular': 0.00,
        'Regular OT': 0.00,
        'Holiday': 0.00,
        'Holiday OT': 0.00,
        'Vacation': 0.00,
        'Sick': 0.00,
        'Differential': 0.00
    }

    ot_rate = reg_rate * 1.5  # Calculate OT rate based on regular rate

    wages['Regular'] = reg_rate * hours['Regular']
    wages['Regular OT'] = ot_rate * hours['Regular OT']
    
    wages['Holiday'] = reg_rate * hours['Holiday']
    wages['Holiday OT'] = ot_rate * hours['Holiday OT']
   
    wages['Vacation'] = reg_rate * hours['Vacation']
    wages['Sick'] = reg_rate * hours['Sick']
    
    wages['Differential'] = DIFF_RATE * hours['Differential']
    
    return wages
