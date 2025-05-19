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

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.data_table = DataTable(self.notebook, self.app)
        self.notebook.add(self.data_table, text="Data Table")

        self.cleaning_panel = CleaningPanel(self.notebook, self.app)
        self.visualization_panel = VisualizationPanel(self.notebook, self.app)
        self.statistics_panel = StatisticsPanel(self.notebook, self.app)

    def refresh_data(self):
        """Refresh the data display"""
        self.data_table.refresh()

    def show_dataset_info(self):
        """Show dataset information"""
        if "Data Table" not in [
            self.notebook.tab(i, "text") for i in self.notebook.tabs()
        ]:
            self.notebook.add(self.data_table, text="Data Table")

        self.notebook.select(self.notebook.tabs()[0])  
        self.data_table.show_info()

    def show_cleaning_panel(self):
        """Show the data cleaning panel"""
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Data Cleaning":
                self.notebook.select(i)

                self.cleaning_panel.on_show()
                return

        self.notebook.add(self.cleaning_panel, text="Data Cleaning")
        self.notebook.select(self.notebook.index("end") - 1)
        self.cleaning_panel.on_show()

    def show_visualization_panel(self):
        """Show the visualization panel"""

        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Visualization":
                self.notebook.select(i)
               
                self.visualization_panel.on_show()
                return

        self.notebook.add(self.visualization_panel, text="Visualization")
        self.notebook.select(self.notebook.index("end") - 1)
        
        self.visualization_panel.on_show()

    def show_statistics_panel(self):
        """Show the statistics panel"""
        
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == "Statistics":
                self.notebook.select(i)
                self.statistics_panel.on_show()
                return

        self.notebook.add(self.statistics_panel, text="Statistics")
        self.notebook.select(self.notebook.index("end") - 1)
        self.statistics_panel.on_show()
