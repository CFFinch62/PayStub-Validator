# IMPORTS
from datetime import datetime

def calculate_hours(time_in, time_out):
    """
    Calculate hours worked from time in and time out.
    Returns a dictionary with the formatted times and total hours.
    """
    # Convert time strings to datetime objects
    time_in_dt = datetime.strptime(time_in, "%H:%M:%S")
    time_out_dt = datetime.strptime(time_out, "%H:%M:%S")

    # Calculate hours worked
    hours = (time_out_dt - time_in_dt).total_seconds() / 3600

    return {
        'in': time_in,
        'out': time_out,
        'hours': hours
    }

def round_minutes_to_quarter_hour(minute):
    
    adjust_hour = False
    
    if minute <= 5:
        adjusted_minute = 0
    elif minute > 5 and minute <= 20:
        adjusted_minute = 15
    elif minute > 20 and minute <= 35:
        adjusted_minute = 30    
    elif minute > 35 and minute <= 55:
        adjusted_minute = 45
    else:
        adjusted_minute = 0
        adjust_hour = True
        
    return [adjusted_minute, adjust_hour] 

# TEST CODE
#if __name__ == "__main__":
#    print(calculate_hours('08:00:00', '17:00:00'))
#    print(calculate_hours('08:30:00', '17:00:00'))
#    print(calculate_hours('08:53:00', '17:00:00'))