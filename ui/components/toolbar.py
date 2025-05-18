"""
Toolbar - Application toolbar with common actions
"""

import tkinter as tk
from tkinter import ttk


class Toolbar(ttk.Frame):
    """Application toolbar with common actions"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._create_widgets()

    def _create_widgets(self):
        """Create toolbar widgets"""
        # Open dataset button
        open_btn = ttk.Button(self, text="Open Dataset", command=self.app.open_dataset)
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.Y)

        # Data cleaning button
        clean_btn = ttk.Button(
            self, text="Clean Data", command=self.app.show_data_cleaning
        )
        clean_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Visualization button
        viz_btn = ttk.Button(
            self, text="Visualize", command=self.app.show_visualization
        )
        viz_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Statistics button
        stats_btn = ttk.Button(
            self, text="Statistics", command=self.app.show_statistics
        )
        stats_btn.pack(side=tk.LEFT, padx=2, pady=2)
