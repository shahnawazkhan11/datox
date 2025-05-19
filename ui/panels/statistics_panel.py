"""
StatisticsPanel - Panel for displaying data statistics
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from scipy import stats


class StatisticsPanel(ttk.Frame):
    """Panel for displaying data statistics"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self._create_options_panel()
        self._create_stats_panel()

    def _create_options_panel(self):
        """Create the options panel"""
        options_frame = ttk.LabelFrame(self, text="Statistics Options")
        options_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(options_frame, text="Statistics Type:").pack(
            anchor="w", padx=5, pady=5
        )
        self.stats_var = tk.StringVar(value="descriptive")
        stats_types = ["descriptive", "correlation", "hypothesis"]
        stats_combo = ttk.Combobox(
            options_frame, textvariable=self.stats_var, values=stats_types
        )
        stats_combo.pack(fill=tk.X, padx=5, pady=2)
        stats_combo.bind("<<ComboboxSelected>>", self._on_stats_type_changed)

        self.column_frame = ttk.LabelFrame(options_frame, text="Column Selection")
        self.column_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.column_frame, text="Column:").pack(anchor="w", padx=5, pady=5)
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(
            self.column_frame, textvariable=self.column_var
        )
        self.column_combo.pack(fill=tk.X, padx=5, pady=2)

        self.hypo_frame = ttk.LabelFrame(options_frame, text="Hypothesis Test")

        ttk.Label(self.hypo_frame, text="Test Type:").pack(anchor="w", padx=5, pady=5)
        self.test_var = tk.StringVar(value="ttest")
        test_types = ["ttest", "anova", "chi2"]
        test_combo = ttk.Combobox(
            self.hypo_frame, textvariable=self.test_var, values=test_types
        )
        test_combo.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.hypo_frame, text="Secondary Column:").pack(
            anchor="w", padx=5, pady=5
        )
        self.column2_var = tk.StringVar()
        self.column2_combo = ttk.Combobox(
            self.hypo_frame, textvariable=self.column2_var
        )
        self.column2_combo.pack(fill=tk.X, padx=5, pady=2)

        ttk.Button(
            options_frame,
            text="Calculate Statistics",
            command=self._calculate_statistics,
        ).pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(
            options_frame, text="Export Statistics", command=self._export_statistics
        ).pack(fill=tk.X, padx=5, pady=5)

    def _create_stats_panel(self):
        """Create the statistics display panel"""
        stats_frame = ttk.LabelFrame(self, text="Statistics Results")
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)

        self.stats_text = tk.Text(stats_frame, wrap=tk.WORD, font=("Courier", 10))
        self.stats_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(
            stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.stats_text.configure(yscrollcommand=scrollbar.set)

    def _on_stats_type_changed(self, event):
        """Handle statistics type change"""
        stats_type = self.stats_var.get()

        if stats_type == "hypothesis":
            self.column_frame.pack_forget()
            self.hypo_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.hypo_frame.pack_forget()
            self.column_frame.pack(fill=tk.X, padx=5, pady=5)

    def _update_column_list(self):
        """Update the column dropdowns with available columns"""
        if (
            hasattr(self.app.data_manager, "dataframe")
            and self.app.data_manager.dataframe is not None
        ):
            df = self.app.data_manager.dataframe
            columns = list(df.columns)

            self.column_combo["values"] = columns
            self.column2_combo["values"] = columns

            if columns:
                self.column_combo.current(0)
                if len(columns) > 1:
                    self.column2_combo.current(1)
                else:
                    self.column2_combo.current(0)

    def _calculate_statistics(self):
        """Calculate and display the selected statistics"""
        if (
            not hasattr(self.app.data_manager, "dataframe")
            or self.app.data_manager.dataframe is None
        ):
            return

        self.stats_text.delete(1.0, tk.END)

        stats_type = self.stats_var.get()
        df = self.app.data_manager.dataframe

        try:
            if stats_type == "descriptive":
                column = self.column_var.get()
                if not column:
                    self._append_text("Please select a column.")
                    return

                self._append_text(f"Descriptive Statistics for '{column}':\n\n")

                if pd.api.types.is_numeric_dtype(df[column]):
                    stats_data = df[column].describe()
                    self._append_text(f"Count: {stats_data['count']}\n")
                    self._append_text(f"Mean: {stats_data['mean']:.4f}\n")
                    self._append_text(f"Std Dev: {stats_data['std']:.4f}\n")
                    self._append_text(f"Min: {stats_data['min']:.4f}\n")
                    self._append_text(f"25%: {stats_data['25%']:.4f}\n")
                    self._append_text(f"Median: {stats_data['50%']:.4f}\n")
                    self._append_text(f"75%: {stats_data['75%']:.4f}\n")
                    self._append_text(f"Max: {stats_data['max']:.4f}\n")

                    self._append_text(f"\nSkewness: {df[column].skew():.4f}\n")
                    self._append_text(f"Kurtosis: {df[column].kurtosis():.4f}\n")
                    self._append_text(f"Missing values: {df[column].isna().sum()}\n")
                else:
                    value_counts = df[column].value_counts()
                    self._append_text(f"Total count: {len(df[column])}\n")
                    self._append_text(f"Unique values: {df[column].nunique()}\n")
                    self._append_text(f"Missing values: {df[column].isna().sum()}\n\n")
                    self._append_text("Value Counts:\n")

                    for val, count in value_counts.items():
                        percent = 100 * count / value_counts.sum()
                        self._append_text(f"{val}: {count} ({percent:.2f}%)\n")

            elif stats_type == "correlation":
                numeric_df = df.select_dtypes(include=["number"])
                if numeric_df.empty:
                    self._append_text(
                        "No numeric columns found for correlation analysis."
                    )
                    return

                corr_matrix = numeric_df.corr()

                self._append_text("Correlation Matrix:\n\n")
                header = "           "
                for col in corr_matrix.columns:
                    header += f"{col[:10]:>10} "
                self._append_text(header + "\n")

                for i, row in enumerate(corr_matrix.index):
                    line = f"{row[:10]:<10} "
                    for j, col in enumerate(corr_matrix.columns):
                        line += f"{corr_matrix.iloc[i, j]:>10.4f} "
                    self._append_text(line + "\n")

            elif stats_type == "hypothesis":
                col1 = self.column_var.get()
                col2 = self.column2_var.get()
                test_type = self.test_var.get()

                if not col1 or not col2:
                    self._append_text("Please select columns for hypothesis testing.")
                    return

                self._append_text(f"Hypothesis Test: {test_type}\n")
                self._append_text(f"Between '{col1}' and '{col2}'\n\n")

                if test_type == "ttest":
                    if not pd.api.types.is_numeric_dtype(
                        df[col1]
                    ) or not pd.api.types.is_numeric_dtype(df[col2]):
                        self._append_text(
                            "T-test requires numeric data for both columns."
                        )
                        return

                    data1 = df[col1].dropna()
                    data2 = df[col2].dropna()

                    result = stats.ttest_ind(data1, data2, nan_policy="omit")

                    self._append_text(f"t-statistic: {result.statistic:.4f}\n")
                    self._append_text(f"p-value: {result.pvalue:.4f}\n\n")

                    alpha = 0.05
                    self._append_text(f"At significance level {alpha}:\n")
                    if result.pvalue < alpha:
                        self._append_text(
                            "Reject null hypothesis. There is a significant difference between the means.\n"
                        )
                    else:
                        self._append_text(
                            "Fail to reject null hypothesis. There is not a significant difference between the means.\n"
                        )

                elif test_type == "chi2":
                    contingency = pd.crosstab(df[col1], df[col2])

                    chi2, p, dof, expected = stats.chi2_contingency(contingency)

                    self._append_text(f"Chi-square statistic: {chi2:.4f}\n")
                    self._append_text(f"p-value: {p:.4f}\n")
                    self._append_text(f"Degrees of freedom: {dof}\n\n")

                    alpha = 0.05
                    self._append_text(f"At significance level {alpha}:\n")
                    if p < alpha:
                        self._append_text(
                            "Reject null hypothesis. There is a significant relationship between the variables.\n"
                        )
                    else:
                        self._append_text(
                            "Fail to reject null hypothesis. There is not a significant relationship between the variables.\n"
                        )

                elif test_type == "anova":
                    if not pd.api.types.is_numeric_dtype(df[col1]):
                        self._append_text(
                            "ANOVA requires a numeric column for the first selection."
                        )
                        return

                    groups = df.groupby(col2)[col1].apply(list).values

                    result = stats.f_oneway(*groups)

                    self._append_text(f"F-statistic: {result.statistic:.4f}\n")
                    self._append_text(f"p-value: {result.pvalue:.4f}\n\n")

                    alpha = 0.05
                    self._append_text(f"At significance level {alpha}:\n")
                    if result.pvalue < alpha:
                        self._append_text(
                            "Reject null hypothesis. There are significant differences between group means.\n"
                        )
                    else:
                        self._append_text(
                            "Fail to reject null hypothesis. There are not significant differences between group means.\n"
                        )

        except Exception as e:
            self._append_text(f"Error calculating statistics: {str(e)}")

    def _append_text(self, text):
        """Append text to the statistics text widget"""
        self.stats_text.insert(tk.END, text)

    def _export_statistics(self):
        """Export the current statistics as a text file"""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if file_path:
            with open(file_path, "w") as f:
                f.write(self.stats_text.get(1.0, tk.END))
            self.app.status_var.set(f"Statistics exported to {file_path}")

    def on_show(self):
        """Called when the panel is shown"""
        self._update_column_list()
