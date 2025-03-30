import tkinter as tk
from tkinter import ttk

def center_window(window):
    """Center any tkinter window on the screen
    
    Args:
        window: A tkinter window/toplevel widget
    """
    window.update_idletasks()
    
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position coordinates
    x = (screen_width - window.winfo_width()) // 2
    y = (screen_height - window.winfo_height()) // 2
    
    # Set the position
    window.geometry(f'+{x}+{y}') 

def center_frame(frame, parent):
    """
    Center a frame within its parent container.
    """
    # Configure parent container to expand
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    
    # Place frame in center of parent
    frame.grid(row=0, column=0, sticky='nsew')
    
    # Configure frame's grid to center its contents
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # Create a centered inner frame for content
    inner_frame = ttk.Frame(frame, padding="20")
    inner_frame.grid(row=0, column=0)
    
    return inner_frame

def center_elements(container):
    """Center elements within their container frame"""
    # Configure column to center elements horizontally
    container.grid_columnconfigure(0, weight=1)
    
    # Center each element
    for child in container.winfo_children():
        child.grid_configure(sticky='n')  # Align to top, prevent vertical stretching 