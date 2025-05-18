"""
DataTable - Panel for displaying tabular data
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandastable import Table


class DataTable(ttk.Frame):
    """Panel for displaying tabular data"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Info bar
        self.info_var = tk.StringVar()
        self.info_var.set("No dataset loaded")
        info_bar = ttk.Label(self, textvariable=self.info_var, anchor=tk.W)
        info_bar.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

        # Table frame
        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(row=1, column=0, sticky="nsew")

        # Create empty table initially
        self.create_empty_table()

    def create_empty_table(self):
        """Create an empty table"""
        empty_df = pd.DataFrame()
        self.table = Table(
            self.table_frame, dataframe=empty_df, showtoolbar=True, showstatusbar=True
        )
        self.table.show()

    def refresh(self):
        """Refresh the data table with current data"""
        if (
            hasattr(self.app.data_manager, "dataframe")
            and self.app.data_manager.dataframe is not None
        ):
            # Update the table with the new dataframe
            self.table.model.df = self.app.data_manager.dataframe
            self.table.redraw()

            # Update info
            rows, cols = self.app.data_manager.dataframe.shape
            self.info_var.set(f"Dataset: {rows} rows, {cols} columns")
        else:
            self.info_var.set("No dataset loaded")

    def show_info(self):
        """Show detailed information about the dataset"""
        if (
            hasattr(self.app.data_manager, "dataframe")
            and self.app.data_manager.dataframe is not None
        ):
            # Create a top-level window for dataset info
            info_window = tk.Toplevel(self)
            info_window.title("Dataset Information")
            info_window.geometry("600x400")

            # Text widget to display the info
            text = tk.Text(info_window, wrap=tk.WORD)
            text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

            # Add dataset info
            df = self.app.data_manager.dataframe
            text.insert(
                tk.END, f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns\n\n"
            )
            text.insert(tk.END, "Column information:\n")

            for col in df.columns:
                text.insert(tk.END, f"\n- {col}\n")
                text.insert(tk.END, f"  Type: {df[col].dtype}\n")
                text.insert(tk.END, f"  Missing values: {df[col].isna().sum()}\n")
                if pd.api.types.is_numeric_dtype(df[col]):
                    text.insert(tk.END, f"  Min: {df[col].min()}\n")
                    text.insert(tk.END, f"  Max: {df[col].max()}\n")
                    text.insert(tk.END, f"  Mean: {df[col].mean()}\n")
                elif pd.api.types.is_string_dtype(df[col]):
                    text.insert(tk.END, f"  Unique values: {df[col].nunique()}\n")

            # Make it read-only
            text.configure(state="disabled")
        else:
            self.info_var.set("No dataset loaded")
