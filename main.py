"""
Datox - No-Code Data Science Platform
Main application entry point
"""

import tkinter as tk
from tkinter import ttk
import os
import sys
import traceback
import pandas as pd

# Add project root to path to enable absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Attempting to import AppWindow...")
    from ui.app_window import AppWindow

    print("Successfully imported AppWindow")
except ImportError as e:
    print(f"Error importing AppWindow: {e}")
    print(f"Current sys.path: {sys.path}")
    print(
        f"Looking for: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui', 'app_window.py')}"
    )
    print(
        f"This file exists: {os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui', 'app_window.py'))}"
    )
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)


def main():
    """Main function to start the application"""
    try:
        print("Starting application...")
        root = tk.Tk()
        root.title("Datox - No-Code Data Science Platform")
        root.geometry("1200x800")

        # Set application style
        style = ttk.Style()
        style.theme_use("clam")  # Use a modern theme

        # Increase default font size for better readability
        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(size=10)

        # Configure pandas to display more readable output
        pd.set_option("display.max_rows", 500)
        pd.set_option("display.max_columns", 50)
        pd.set_option("display.width", 1000)

        print("Creating AppWindow instance...")
        app = AppWindow(root)
        print("AppWindow created successfully")

        print("Entering main loop...")
        root.mainloop()
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
