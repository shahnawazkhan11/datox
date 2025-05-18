"""
AppWindow - Main application window for Datox
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ui.components.sidebar import Sidebar
from ui.components.data_view import DataView
from ui.components.toolbar import Toolbar
from core.data_manager import DataManager


class AppWindow:
    """Main application window class that organizes the UI components"""

    def __init__(self, root):
        self.root = root
        self.data_manager = DataManager()

        # Configure root window grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Create main UI components
        self.toolbar = Toolbar(self.root, self)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self.root, self)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        self.data_view = DataView(self.root, self)
        self.data_view.grid(row=1, column=1, sticky="nsew")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Add tab change listener to update panels when tabs are changed
        self.data_view.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        self._create_menu()

    def _create_menu(self):
        """Create the application menu"""
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Dataset", command=self.open_dataset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Data menu
        data_menu = tk.Menu(menu_bar, tearoff=0)
        data_menu.add_command(label="Clean Data", command=self.show_data_cleaning)
        data_menu.add_command(label="Visualize", command=self.show_visualization)
        data_menu.add_command(label="Statistics", command=self.show_statistics)
        menu_bar.add_cascade(label="Data", menu=data_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def open_dataset(self):
        """Open a dataset file dialog"""
        file_path = filedialog.askopenfilename(
            title="Open Dataset",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            try:
                # Show loading indicator
                self.status_var.set(f"Loading dataset from {file_path}...")
                self.root.update_idletasks()  # Force UI update

                # Create progress window
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Loading Dataset")
                progress_window.geometry("300x100")
                progress_window.transient(self.root)
                progress_window.grab_set()

                ttk.Label(progress_window, text="Loading dataset, please wait...").pack(
                    pady=10
                )
                progress = ttk.Progressbar(progress_window, mode="indeterminate")
                progress.pack(fill=tk.X, padx=20, pady=10)
                progress.start()
                progress_window.update_idletasks()

                # Load the dataset
                self.data_manager.load_dataset(file_path)

                # Close progress window
                progress_window.destroy()

                # Update the UI
                self.data_view.refresh_data()
                self.status_var.set(f"Dataset loaded: {file_path}")

            except ValueError as e:
                messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def show_data_cleaning(self):
        """Show data cleaning panel"""
        self.data_view.show_cleaning_panel()

    def show_visualization(self):
        """Show visualization panel"""
        self.data_view.show_visualization_panel()

    def show_statistics(self):
        """Show statistics panel"""
        self.data_view.show_statistics_panel()

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About", "Datox - No-Code Data Science Platform\nVersion 1.0"
        )

    def _on_tab_changed(self, event):
        """Handle tab change events to ensure panels are updated"""
        current_tab = self.data_view.notebook.select()
        tab_text = self.data_view.notebook.tab(current_tab, "text")

        # Call the appropriate on_show method based on the selected tab
        if tab_text == "Data Cleaning":
            self.data_view.cleaning_panel.on_show()
        elif tab_text == "Visualization":
            self.data_view.visualization_panel.on_show()
        elif tab_text == "Statistics":
            self.data_view.statistics_panel.on_show()
