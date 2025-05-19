"""
Sidebar - Navigation panel for the application
"""


import tkinter as tk
from tkinter import ttk


class Sidebar(ttk.Frame):
    """Sidebar navigation panel"""

    def __init__(self, parent, app):
        super().__init__(parent, width=200, style="Sidebar.TFrame")
        self.app = app
        
        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="#f0f0f0")

        self.pack_propagate(False)

        self._create_widgets()

    def _create_widgets(self):
        """Create sidebar widgets"""
        title_label = ttk.Label(self, text="Datox Tools", font=("Arial", 12, "bold"))
        title_label.pack(pady=10)

        section_frame = ttk.LabelFrame(self, text="Data Operations")
        section_frame.pack(fill=tk.X, padx=5, pady=5)

        info_btn = ttk.Button(
            section_frame,
            text="Dataset Info",
            command=lambda: self.app.data_view.show_dataset_info(),
        )
        info_btn.pack(fill=tk.X, padx=5, pady=3)

        clean_btn = ttk.Button(
            section_frame,
            text="Data Cleaning",
            command=lambda: self.app.show_data_cleaning(),
        )
        clean_btn.pack(fill=tk.X, padx=5, pady=3)

        viz_frame = ttk.LabelFrame(self, text="Visualization")
        viz_frame.pack(fill=tk.X, padx=5, pady=5)

        charts_btn = ttk.Button(
            viz_frame, text="Charts", command=lambda: self.app.show_visualization()
        )
        charts_btn.pack(fill=tk.X, padx=5, pady=3)

        analytics_frame = ttk.LabelFrame(self, text="Analytics")
        analytics_frame.pack(fill=tk.X, padx=5, pady=5)

        stats_btn = ttk.Button(
            analytics_frame,
            text="Statistics",
            command=lambda: self.app.show_statistics(),
        )
        stats_btn.pack(fill=tk.X, padx=5, pady=3)
