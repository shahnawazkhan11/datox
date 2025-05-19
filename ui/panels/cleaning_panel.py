"""
CleaningPanel - Panel for data cleaning operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class CleaningPanel(ttk.Frame):
    """Panel for data cleaning operations"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self._create_options_panel()
        self._create_preview_panel()

    def _create_options_panel(self):
        """Create the options panel"""
        options_frame = ttk.LabelFrame(self, text="Cleaning Options")
        options_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(options_frame, text="Select Column:").pack(anchor="w", padx=5, pady=5)
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(options_frame, textvariable=self.column_var)
        self.column_combo.pack(fill=tk.X, padx=5, pady=2)
        self.column_combo.bind("<<ComboboxSelected>>", self._on_column_selected)

        duplicates_frame = ttk.LabelFrame(options_frame, text="Remove Duplicates")
        duplicates_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            duplicates_frame,
            text="Remove Duplicate Rows",
            command=self._remove_duplicates,
        ).pack(fill=tk.X, padx=5, pady=5)

        missing_frame = ttk.LabelFrame(options_frame, text="Handle Missing Values")
        missing_frame.pack(fill=tk.X, padx=5, pady=5)

        self.missing_var = tk.StringVar(value="drop")
        ttk.Radiobutton(
            missing_frame, text="Drop rows", variable=self.missing_var, value="drop"
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Radiobutton(
            missing_frame,
            text="Fill with mean",
            variable=self.missing_var,
            value="mean",
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Radiobutton(
            missing_frame,
            text="Fill with median",
            variable=self.missing_var,
            value="median",
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Radiobutton(
            missing_frame,
            text="Fill with mode",
            variable=self.missing_var,
            value="mode",
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Radiobutton(
            missing_frame,
            text="Fill with value:",
            variable=self.missing_var,
            value="value",
        ).pack(anchor="w", padx=5, pady=2)

        self.custom_value = ttk.Entry(missing_frame)
        self.custom_value.pack(fill=tk.X, padx=5, pady=2)

        outliers_frame = ttk.LabelFrame(options_frame, text="Handle Outliers")
        outliers_frame.pack(fill=tk.X, padx=5, pady=5)

        self.outlier_var = tk.StringVar(value="none")
        ttk.Radiobutton(
            outliers_frame, text="None", variable=self.outlier_var, value="none"
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Radiobutton(
            outliers_frame,
            text="Cap at percentiles (1.5 IQR)",
            variable=self.outlier_var,
            value="cap",
        ).pack(anchor="w", padx=5, pady=2)

        ttk.Radiobutton(
            outliers_frame,
            text="Remove outliers",
            variable=self.outlier_var,
            value="remove",
        ).pack(anchor="w", padx=5, pady=2)

        # Buttons
        ttk.Button(
            options_frame, text="Apply Cleaning", command=self._apply_cleaning
        ).pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(options_frame, text="Preview", command=self._preview_cleaning).pack(
            fill=tk.X, padx=5, pady=5
        )

        # Reset button
        ttk.Button(
            options_frame, text="Reset to Original Data", command=self._reset_data
        ).pack(fill=tk.X, padx=5, pady=10)

    def _create_preview_panel(self):
        """Create the preview panel"""
        preview_frame = ttk.LabelFrame(self, text="Data Preview")
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        self.preview_info = ttk.Label(
            preview_frame, text="Select a column and cleaning options to preview"
        )
        self.preview_info.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.preview_tree = ttk.Treeview(preview_frame)
        self.preview_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        y_scrollbar = ttk.Scrollbar(
            preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview
        )
        y_scrollbar.grid(row=1, column=1, sticky="ns")

        x_scrollbar = ttk.Scrollbar(
            preview_frame, orient=tk.HORIZONTAL, command=self.preview_tree.xview
        )
        x_scrollbar.grid(row=2, column=0, sticky="ew")

        self.preview_tree.configure(
            yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set
        )

    def _update_column_list(self):
        """Update the column dropdown with available columns"""
        if (
            hasattr(self.app.data_manager, "dataframe")
            and self.app.data_manager.dataframe is not None
        ):
            columns = list(self.app.data_manager.dataframe.columns)
            self.column_combo["values"] = columns
            if columns:
                self.column_combo.current(0)

    def _on_column_selected(self, event):
        """Handle column selection change"""

        self._preview_cleaning()

    def _preview_cleaning(self):
        """Preview the selected cleaning operations"""
        if (
            not hasattr(self.app.data_manager, "dataframe")
            or self.app.data_manager.dataframe is None
        ):
            return

        column = self.column_var.get()
        if not column:
            return

        df = self.app.data_manager.dataframe.copy()
        sample_size = min(10, len(df))
        sample_df = df.sample(sample_size) if sample_size > 0 else df

        self.preview_tree.delete(*self.preview_tree.get_children())

        self.preview_tree["columns"] = ["index", "original", "cleaned"]
        self.preview_tree.column("#0", width=0, stretch=tk.NO)
        self.preview_tree.column("index", width=80, anchor=tk.W)
        self.preview_tree.column("original", width=150, anchor=tk.W)
        self.preview_tree.column("cleaned", width=150, anchor=tk.W)

        self.preview_tree.heading("#0", text="")
        self.preview_tree.heading("index", text="Index")
        self.preview_tree.heading("original", text="Original Value")
        self.preview_tree.heading("cleaned", text="Cleaned Value")

        cleaned_series = self._apply_cleaning_options(sample_df[column])

        for idx, (orig_val, clean_val) in enumerate(
            zip(sample_df[column], cleaned_series)
        ):
            row_idx = sample_df.index[idx]
            self.preview_tree.insert("", tk.END, values=(row_idx, orig_val, clean_val))

        missing_count = df[column].isna().sum()
        self.preview_info.config(
            text=f"Column: {column} | Missing values: {missing_count} | Total rows: {len(df)}"
        )

    def _apply_cleaning_options(self, series):
        """Apply selected cleaning options to a series"""
        result = series.copy()

        missing_option = self.missing_var.get()
        if pd.api.types.is_numeric_dtype(series):
            if missing_option == "mean":
                result = result.fillna(series.mean())
            elif missing_option == "median":
                result = result.fillna(series.median())
            elif missing_option == "mode":
                result = result.fillna(
                    series.mode()[0] if not series.mode().empty else None
                )
            elif missing_option == "value":
                try:
                    fill_value = float(self.custom_value.get())
                    result = result.fillna(fill_value)
                except (ValueError, TypeError):
                    pass 
        else:
            if missing_option == "mode":
                result = result.fillna(
                    series.mode()[0] if not series.mode().empty else ""
                )
            elif missing_option == "value":
                result = result.fillna(self.custom_value.get())

        if pd.api.types.is_numeric_dtype(series):
            if self.outlier_var.get() == "cap":
                q1 = result.quantile(0.25)
                q3 = result.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                result = result.clip(lower=lower_bound, upper=upper_bound)
            elif self.outlier_var.get() == "remove":
                q1 = result.quantile(0.25)
                q3 = result.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                result = result.mask((result < lower_bound) | (result > upper_bound))

        return result

    def _apply_cleaning(self):
        """Apply the cleaning operations to the actual dataset"""
        if (
            not hasattr(self.app.data_manager, "dataframe")
            or self.app.data_manager.dataframe is None
        ):
            return

        column = self.column_var.get()
        if not column:
            messagebox.showwarning("Warning", "Please select a column first")
            return

        try:
            missing_option = self.missing_var.get()
            outlier_option = self.outlier_var.get()

            if missing_option == "drop":
                self.app.data_manager.clean_missing_values(column, "drop")
            elif missing_option == "mean":
                self.app.data_manager.clean_missing_values(column, "mean")
            elif missing_option == "median":
                self.app.data_manager.clean_missing_values(column, "median")
            elif missing_option == "mode":
                self.app.data_manager.clean_missing_values(column, "mode")
            elif missing_option == "value":
                value = self.custom_value.get()
                if not value:
                    messagebox.showwarning(
                        "Warning", "Please enter a value to fill with"
                    )
                    return

                if pd.api.types.is_numeric_dtype(
                    self.app.data_manager.dataframe[column]
                ):
                    try:
                        value = float(value)
                    except ValueError:
                        messagebox.showwarning("Warning", "Please enter a valid number")
                        return

                self.app.data_manager.clean_missing_values(column, "value", value)

            if outlier_option != "none":
                self.app.data_manager.handle_outliers(column, outlier_option)

            self.app.data_view.refresh_data()

            self.preview_info.config(text=f"Cleaning applied to column: {column}")
            messagebox.showinfo(
                "Success", f"Cleaning operations applied to column: {column}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply cleaning: {str(e)}")

    def _remove_duplicates(self):
        """Remove duplicate rows from the dataset"""
        if (
            not hasattr(self.app.data_manager, "dataframe")
            or self.app.data_manager.dataframe is None
        ):
            return

        try:
            removed_count = self.app.data_manager.remove_duplicates()

            self.app.data_view.refresh_data()

            messagebox.showinfo(
                "Remove Duplicates", f"Removed {removed_count} duplicate rows"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove duplicates: {str(e)}")

    def _reset_data(self):
        """Reset the data to its original state"""
        if (
            not hasattr(self.app.data_manager, "original_dataframe")
            or self.app.data_manager.original_dataframe is None
        ):
            return

        if messagebox.askyesno(
            "Reset Data", "Reset data to original state? All changes will be lost."
        ):
            try:
                self.app.data_manager.reset_to_original()

                self.app.data_view.refresh_data()

                self.preview_info.config(text="Data reset to original state")
                messagebox.showinfo(
                    "Reset Data", "Data has been reset to its original state"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset data: {str(e)}")

    def on_show(self):
        """Called when the panel is shown"""
        if (
            hasattr(self.app.data_manager, "dataframe")
            and self.app.data_manager.dataframe is not None
        ):
            columns = list(self.app.data_manager.dataframe.columns)

            self.column_combo["values"] = columns

            if columns:
                self.column_combo.set(columns[0])  

                self._preview_cleaning()
        else:
            self.column_combo["values"] = []
            self.preview_info.config(
                text="No dataset loaded. Please load a dataset first."
            )
