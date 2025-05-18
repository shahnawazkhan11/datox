"""
DataView - Main data display area
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from ui.panels.data_table import DataTable
from ui.panels.cleaning_panel import CleaningPanel
from ui.panels.visualization_panel import VisualizationPanel
from ui.panels.statistics_panel import StatisticsPanel


class DataView(ttk.Frame):
    """Main data display area"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Configure the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create a notebook for multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Create the main data table panel
        self.data_table = DataTable(self.notebook, self.app)
        self.notebook.add(self.data_table, text="Data Table")

        # Create specialized panels but don't add them yet
        self.cleaning_panel = CleaningPanel(self.notebook, self.app)
        self.visualization_panel = VisualizationPanel(self.notebook, self.app)
        self.statistics_panel = StatisticsPanel(self.notebook, self.app)

    def refresh_data(self):
        """Refresh the data display"""
        self.data_table.refresh()

    def show_dataset_info(self):
        """Show dataset information"""
        # Ensure we have a data tab
        if "Data Table" not in [
            self.notebook.tab(i, "text") for i in self.notebook.tabs()
        ]:
            self.notebook.add(self.data_table, text="Data Table")

        self.notebook.select(self.notebook.tabs()[0])  # Select the data table tab
        self.data_table.show_info()

    def show_cleaning_panel(self):
        """Show the data cleaning panel"""
        # Check if cleaning panel is already in the notebook
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Data Cleaning":
                self.notebook.select(i)
                # Make sure to call on_show when switching to this tab
                self.cleaning_panel.on_show()
                return

        # If not, add it and call on_show
        self.notebook.add(self.cleaning_panel, text="Data Cleaning")
        self.notebook.select(self.notebook.index("end") - 1)
        self.cleaning_panel.on_show()

    def show_visualization_panel(self):
        """Show the visualization panel"""
        # Check if visualization panel is already in the notebook
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Visualization":
                self.notebook.select(i)
                # Make sure to call on_show when switching to this tab
                self.visualization_panel.on_show()
                return

        # If not, add it and call on_show
        self.notebook.add(self.visualization_panel, text="Visualization")
        self.notebook.select(self.notebook.index("end") - 1)
        # Make sure to set the focus on the visualization tab
        self.visualization_panel.on_show()

    def show_statistics_panel(self):
        """Show the statistics panel"""
        # Check if statistics panel is already in the notebook
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Statistics":
                self.notebook.select(i)
                # Make sure to call on_show when switching to this tab
                self.statistics_panel.on_show()
                return

        # If not, add it and call on_show
        self.notebook.add(self.statistics_panel, text="Statistics")
        self.notebook.select(self.notebook.index("end") - 1)
        self.statistics_panel.on_show()
