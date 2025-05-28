"""
VisualizationPanel - Panel for data visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter


class VisualizationPanel(ttk.Frame):
    """Panel for data visualization"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        sns.set_style("whitegrid")
        plt.rcParams["font.size"] = 10
        plt.rcParams["axes.titlesize"] = 12
        plt.rcParams["axes.labelsize"] = 10

        self.color_palette = sns.color_palette("tab10")

        self._create_options_panel()
        self._create_plot_panel()

    def _create_options_panel(self):
        options_frame = ttk.LabelFrame(self, text="Visualization Options")
        options_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(options_frame, text="Chart Type:").pack(anchor="w", padx=5, pady=5)
        self.chart_var = tk.StringVar(value="scatter")
        chart_types = ["scatter", "bar", "box", "histogram", "heatmap"]
        chart_combo = ttk.Combobox(
            options_frame, textvariable=self.chart_var, values=chart_types
        )
        chart_combo.pack(fill=tk.X, padx=5, pady=2)
        chart_combo.bind("<<ComboboxSelected>>", self._on_chart_type_changed)

        ttk.Label(options_frame, text="X-Axis Column:").pack(anchor="w", padx=5, pady=5)
        self.x_var = tk.StringVar()
        self.x_combo = ttk.Combobox(options_frame, textvariable=self.x_var)
        self.x_combo.pack(fill=tk.X, padx=5, pady=2)
        self.x_combo.bind("<<ComboboxSelected>>", self._on_axis_changed)

        self.y_label = ttk.Label(options_frame, text="Y-Axis Column:")
        self.y_label.pack(anchor="w", padx=5, pady=5)
        self.y_var = tk.StringVar()
        self.y_combo = ttk.Combobox(options_frame, textvariable=self.y_var)
        self.y_combo.pack(fill=tk.X, padx=5, pady=2)
        self.y_combo.bind("<<ComboboxSelected>>", self._on_axis_changed)

        self.options_container = ttk.Frame(options_frame)
        self.options_container.pack(fill=tk.X, padx=5, pady=5)

        self._create_scatter_options()
        self._create_histogram_options()
        self._create_heatmap_options()
        self._create_box_options()
        self._create_bar_options()

        ttk.Label(options_frame, text="Chart Title:").pack(anchor="w", padx=5, pady=5)
        self.title_var = tk.StringVar(value="Data Visualization")
        title_entry = ttk.Entry(options_frame, textvariable=self.title_var)
        title_entry.pack(fill=tk.X, padx=5, pady=2)

        ttk.Button(
            options_frame, text="Generate Plot", command=self._generate_plot
        ).pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(options_frame, text="Export Plot", command=self._export_plot).pack(
            fill=tk.X, padx=5, pady=5
        )

    def _create_scatter_options(self):
        """Create options specific to scatter plots"""
        self.scatter_frame = ttk.LabelFrame(
            self.options_container, text="Scatter Options"
        )

        self.regression_var = tk.BooleanVar(value=False)
        regression_check = ttk.Checkbutton(
            self.scatter_frame,
            text="Add regression line",
            variable=self.regression_var,
        )
        regression_check.pack(anchor="w", padx=5, pady=2)

        reg_type_frame = ttk.Frame(self.scatter_frame)
        reg_type_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(reg_type_frame, text="Regression Type:").pack(side=tk.LEFT)
        self.reg_type_var = tk.StringVar(value="linear")
        reg_types = ["linear", "polynomial"]
        reg_type_combo = ttk.Combobox(
            reg_type_frame, textvariable=self.reg_type_var, values=reg_types, width=10
        )
        reg_type_combo.pack(side=tk.LEFT, padx=5)
        
        poly_frame = ttk.Frame(self.scatter_frame)
        poly_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(poly_frame, text="Polynomial Degree:").pack(side=tk.LEFT)
        self.poly_degree_var = tk.StringVar(value="2")
        poly_degree_entry = ttk.Entry(
            poly_frame, textvariable=self.poly_degree_var, width=5
        )
        poly_degree_entry.pack(side=tk.LEFT, padx=5)

        size_frame = ttk.Frame(self.scatter_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(size_frame, text="Marker Size:").pack(side=tk.LEFT)
        self.marker_size_var = tk.StringVar(value="50")
        size_entry = ttk.Entry(size_frame, textvariable=self.marker_size_var, width=5)
        size_entry.pack(side=tk.LEFT, padx=5)

        self.show_stats_var = tk.BooleanVar(value=True)
        stats_check = ttk.Checkbutton(
            self.scatter_frame,
            text="Show correlation statistics",
            variable=self.show_stats_var,
        )
        stats_check.pack(anchor="w", padx=5, pady=2)

    def _create_histogram_options(self):
        """Create options specific to histograms"""
        self.histogram_frame = ttk.LabelFrame(
            self.options_container, text="Histogram Options"
        )

        bins_frame = ttk.Frame(self.histogram_frame)
        bins_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(bins_frame, text="Number of Bins:").pack(side=tk.LEFT)
        self.bins_var = tk.StringVar(value="20")
        bins_entry = ttk.Entry(bins_frame, textvariable=self.bins_var, width=5)
        bins_entry.pack(side=tk.LEFT, padx=5)

        self.kde_var = tk.BooleanVar(value=True)
        kde_check = ttk.Checkbutton(
            self.histogram_frame,
            text="Add density curve",
            variable=self.kde_var,
        )
        kde_check.pack(anchor="w", padx=5, pady=2)

        self.hist_stats_var = tk.BooleanVar(value=True)
        hist_stats_check = ttk.Checkbutton(
            self.histogram_frame,
            text="Show statistics",
            variable=self.hist_stats_var,
        )
        hist_stats_check.pack(anchor="w", padx=5, pady=2)

        color_frame = ttk.Frame(self.histogram_frame)
        color_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT)
        self.hist_color_var = tk.StringVar(value="blue")
        colors = ["blue", "green", "red", "purple", "orange", "teal"]
        color_combo = ttk.Combobox(
            color_frame, textvariable=self.hist_color_var, values=colors, width=10
        )
        color_combo.pack(side=tk.LEFT, padx=5)

    def _create_heatmap_options(self):
        """Create options specific to heatmaps"""
        self.heatmap_frame = ttk.LabelFrame(
            self.options_container, text="Heatmap Options"
        )

        cmap_frame = ttk.Frame(self.heatmap_frame)
        cmap_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(cmap_frame, text="Color Map:").pack(side=tk.LEFT)
        self.cmap_var = tk.StringVar(value="viridis")
        cmaps = [
            "viridis",
            "plasma",
            "Blues",
            "Reds",
            "Greens",
            "YlGnBu",
            "coolwarm",
            "RdBu_r",
        ]
        cmap_combo = ttk.Combobox(
            cmap_frame, textvariable=self.cmap_var, values=cmaps, width=10
        )
        cmap_combo.pack(side=tk.LEFT, padx=5)

        self.annot_var = tk.BooleanVar(value=True)
        annot_check = ttk.Checkbutton(
            self.heatmap_frame,
            text="Show values",
            variable=self.annot_var,
        )
        annot_check.pack(anchor="w", padx=5, pady=2)

        self.mask_var = tk.BooleanVar(value=False)
        mask_check = ttk.Checkbutton(
            self.heatmap_frame,
            text="Show only upper triangle",
            variable=self.mask_var,
        )
        mask_check.pack(anchor="w", padx=5, pady=2)

        self.cluster_var = tk.BooleanVar(value=False)
        cluster_check = ttk.Checkbutton(
            self.heatmap_frame,
            text="Cluster variables",
            variable=self.cluster_var,
        )
        cluster_check.pack(anchor="w", padx=5, pady=2)

    def _create_box_options(self):
        """Create options specific to box plots"""
        self.box_frame = ttk.LabelFrame(self.options_container, text="Box Plot Options")

        self.notch_var = tk.BooleanVar(value=False)
        notch_check = ttk.Checkbutton(
            self.box_frame,
            text="Show notches",
            variable=self.notch_var,
        )
        notch_check.pack(anchor="w", padx=5, pady=2)

        self.points_var = tk.BooleanVar(value=True)
        points_check = ttk.Checkbutton(
            self.box_frame,
            text="Show individual points",
            variable=self.points_var,
        )
        points_check.pack(anchor="w", padx=5, pady=2)

        self.mean_var = tk.BooleanVar(value=True)
        mean_check = ttk.Checkbutton(
            self.box_frame,
            text="Show mean marker",
            variable=self.mean_var,
        )
        mean_check.pack(anchor="w", padx=5, pady=2)

        palette_frame = ttk.Frame(self.box_frame)
        palette_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(palette_frame, text="Color Palette:").pack(side=tk.LEFT)
        self.box_palette_var = tk.StringVar(value="tab10")
        palettes = ["tab10", "Set1", "Set2", "Set3", "pastel", "husl", "colorblind"]
        palette_combo = ttk.Combobox(
            palette_frame, textvariable=self.box_palette_var, values=palettes, width=10
        )
        palette_combo.pack(side=tk.LEFT, padx=5)

    def _create_bar_options(self):
        """Create options specific to bar charts"""
        self.bar_frame = ttk.LabelFrame(
            self.options_container, text="Bar Chart Options"
        )

        self.bar_orient_var = tk.StringVar(value="vertical")
        ttk.Radiobutton(
            self.bar_frame,
            text="Vertical",
            variable=self.bar_orient_var,
            value="vertical",
        ).pack(anchor="w", padx=5, pady=2)
        ttk.Radiobutton(
            self.bar_frame,
            text="Horizontal",
            variable=self.bar_orient_var,
            value="horizontal",
        ).pack(anchor="w", padx=5, pady=2)

        self.bar_values_var = tk.BooleanVar(value=True)
        bar_values_check = ttk.Checkbutton(
            self.bar_frame,
            text="Show values on bars",
            variable=self.bar_values_var,
        )
        bar_values_check.pack(anchor="w", padx=5, pady=2)

        self.sort_bars_var = tk.BooleanVar(value=False)
        sort_bars_check = ttk.Checkbutton(
            self.bar_frame,
            text="Sort bars by height",
            variable=self.sort_bars_var,
        )
        sort_bars_check.pack(anchor="w", padx=5, pady=2)

        palette_frame = ttk.Frame(self.bar_frame)
        palette_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(palette_frame, text="Color Palette:").pack(side=tk.LEFT)
        self.bar_palette_var = tk.StringVar(value="tab10")
        palettes = ["tab10", "Set1", "Set2", "Set3", "pastel", "husl", "colorblind"]
        palette_combo = ttk.Combobox(
            palette_frame, textvariable=self.bar_palette_var, values=palettes, width=10
        )
        palette_combo.pack(side=tk.LEFT, padx=5)

    def _on_chart_type_changed(self, event):
        """Handle chart type selection change"""
        chart_type = self.chart_var.get()

        for frame in [
            self.scatter_frame,
            self.histogram_frame,
            self.heatmap_frame,
            self.box_frame,
            self.bar_frame,
        ]:
            frame.pack_forget()

        if chart_type == "histogram":
            self.y_label.pack_forget()
            self.y_combo.pack_forget()
            self.histogram_frame.pack(fill=tk.X, padx=0, pady=5)

        elif chart_type == "heatmap":
            self.y_label.pack_forget()
            self.y_combo.pack_forget()
            self.heatmap_frame.pack(fill=tk.X, padx=0, pady=5)

        elif chart_type == "scatter":
            self.y_label.pack(anchor="w", padx=5, pady=5)
            self.y_combo.pack(fill=tk.X, padx=5, pady=2)
            self.scatter_frame.pack(fill=tk.X, padx=0, pady=5)

        elif chart_type == "box":
            self.y_label.pack(anchor="w", padx=5, pady=5)
            self.y_combo.pack(fill=tk.X, padx=5, pady=2)
            self.box_frame.pack(fill=tk.X, padx=0, pady=5)

        else:
            self.y_label.pack(anchor="w", padx=5, pady=5)
            self.y_combo.pack(fill=tk.X, padx=5, pady=2)
            self.bar_frame.pack(fill=tk.X, padx=0, pady=5)

        self.title_var.set(f"{chart_type.capitalize()} Chart")

        self._update_column_suggestions()

    def _on_axis_changed(self, event):
        """Handle axis column selection change"""
        self._update_column_suggestions()

    def _update_column_suggestions(self):
        """Update the column dropdowns with appropriate columns based on the selected chart type"""
        if (
            not hasattr(self.app.data_manager, "dataframe")
            or self.app.data_manager.dataframe is None
        ):
            return

        df = self.app.data_manager.dataframe
        chart_type = self.chart_var.get()

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        current_x = self.x_var.get()
        current_y = self.y_var.get()

        if chart_type == "histogram":
            self.x_combo["values"] = numeric_cols
            if current_x not in numeric_cols and numeric_cols:
                self.x_var.set(numeric_cols[0])

        elif chart_type == "heatmap":
            self.x_combo["values"] = ["[Correlation Matrix]"]
            self.x_var.set("[Correlation Matrix]")

        elif chart_type == "scatter":
            self.x_combo["values"] = numeric_cols
            self.y_combo["values"] = numeric_cols

            if current_x not in numeric_cols and numeric_cols:
                self.x_var.set(numeric_cols[0])
            if current_y not in numeric_cols and len(numeric_cols) > 1:
                self.y_var.set(numeric_cols[1])
            elif current_y not in numeric_cols and numeric_cols:
                self.y_var.set(numeric_cols[0])

        elif chart_type == "box":
            self.x_combo["values"] = categorical_cols
            self.y_combo["values"] = numeric_cols

            if current_x not in categorical_cols and categorical_cols:
                self.x_var.set(categorical_cols[0])
            elif (
                not categorical_cols and numeric_cols
            ):  
                self.x_var.set(numeric_cols[0])

            if current_y not in numeric_cols and numeric_cols:
                self.y_var.set(numeric_cols[0])

        else: 
            self.x_combo["values"] = categorical_cols
            self.y_combo["values"] = numeric_cols

            if current_x not in categorical_cols and categorical_cols:
                self.x_var.set(categorical_cols[0])
            elif (
                not categorical_cols and numeric_cols
            ): 
                self.x_var.set(numeric_cols[0])

            if current_y not in numeric_cols and numeric_cols:
                self.y_var.set(numeric_cols[0])

    def _create_plot_panel(self):
        """Create the plot panel"""
        plot_frame = ttk.LabelFrame(self, text="Visualization")
        plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.grid(row=1, column=0, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

    def _update_column_list(self):
        """Update the column dropdowns with available columns"""
        if (
            hasattr(self.app.data_manager, "dataframe")
            and self.app.data_manager.dataframe is not None
        ):
            self._update_column_suggestions()

    def _generate_plot(self):
        """Generate the selected plot type"""
        if (
            not hasattr(self.app.data_manager, "dataframe")
            or self.app.data_manager.dataframe is None
        ):
            messagebox.showwarning("Warning", "Please load a dataset first")
            return

        chart_type = self.chart_var.get()
        title = self.title_var.get()
        df = self.app.data_manager.dataframe

        self.figure.clear()

        try:
            sns.set_style("whitegrid")

            if chart_type == "scatter":
                ax = self.figure.add_subplot(111)
                self._create_scatter_plot(df, ax)
            elif chart_type == "bar":
                ax = self.figure.add_subplot(111)
                self._create_bar_plot(df, ax)
            elif chart_type == "histogram":
                ax = self.figure.add_subplot(111)
                self._create_histogram_plot(df, ax)
            elif chart_type == "box":
                ax = self.figure.add_subplot(111)
                self._create_box_plot(df, ax)
            elif chart_type == "heatmap":
                ax = self.figure.add_subplot(111)
                self._create_heatmap_plot(df, ax)

            if "ax" in locals():
                ax.set_title(title, fontsize=14, fontweight="bold", pad=15)

            self.figure.tight_layout()

            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Plot Error", f"Error generating plot: {str(e)}")
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(
                0.5,
                0.5,
                f"Error generating plot:\n{str(e)}",
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax.transAxes,
                fontsize=12,
                color="red",
            )
            self.canvas.draw()

    def _create_scatter_plot(self, df, ax):
        """Create a scatter plot with enhanced visual insights"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()

        if not x_col or not y_col:
            messagebox.showwarning("Warning", "Please select X and Y columns")
            return

        try:
            marker_size = int(self.marker_size_var.get())
        except ValueError:
            marker_size = 50

        valid_data = df[[x_col, y_col]].dropna()

        if len(valid_data) < 2:
            messagebox.showwarning(
                "Warning", "Not enough valid data points to create scatter plot"
            )
            return

        scatter = ax.scatter(
            valid_data[x_col],
            valid_data[y_col],
            s=marker_size,
            alpha=0.7,
            edgecolor="w",
            linewidth=0.5,
            c=self.color_palette[0],
        )

        correlation = valid_data[x_col].corr(valid_data[y_col])

        if self.regression_var.get():
            x_data = valid_data[x_col]
            y_data = valid_data[y_col]

            regression_type = self.reg_type_var.get()

            if regression_type == "linear":
                z = np.polyfit(x_data, y_data, 1)
                p = np.poly1d(z)

                x_range = np.linspace(x_data.min(), x_data.max(), 100)
                ax.plot(
                    x_range,
                    p(x_range),
                    "r--",
                    linewidth=2,
                    label=f"y = {z[0]:.4f}x + {z[1]:.4f}",
                )


                if len(x_data) > 2:  
                    y_pred = p(x_data)
                    x_sorted = np.sort(x_data)
                    y_pred_sorted = p(x_sorted)

                    residual_std = np.std(y_data - y_pred)
                    ax.fill_between(
                        x_sorted,
                        y_pred_sorted - residual_std,
                        y_pred_sorted + residual_std,
                        alpha=0.2,
                        color="red",
                    )

            elif regression_type == "polynomial":
                try:
                    degree = int(self.poly_degree_var.get())
                    if degree < 1:
                        degree = 2
                except ValueError:
                    degree = 2

                z = np.polyfit(x_data, y_data, degree)
                p = np.poly1d(z)

                x_range = np.linspace(x_data.min(), x_data.max(), 100)
                ax.plot(
                    x_range,
                    p(x_range),
                    "r-",
                    linewidth=2,
                    label=f"Polynomial (degree {degree})",
                )

        if self.show_stats_var.get():
            stats_text = (
                f"Correlation: {correlation:.4f}\n"
                f"Number of points: {len(valid_data)}\n"
            )

            if self.regression_var.get() and "p" in locals():
                y_pred = p(x_data)
                ss_total = np.sum((y_data - np.mean(y_data)) ** 2)
                ss_residual = np.sum((y_data - y_pred) ** 2)
                r_squared = 1 - (ss_residual / ss_total)

                stats_text += f"R²: {r_squared:.4f}\n"

            props = dict(boxstyle="round", facecolor="white", alpha=0.8)
            ax.text(
                0.05,
                0.95,
                stats_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment="top",
                bbox=props,
            )

        if self.regression_var.get():
            ax.legend(loc="best", frameon=True, framealpha=0.8)

        ax.set_xlabel(f"{x_col}", fontsize=12)
        ax.set_ylabel(f"{y_col}", fontsize=12)

        ax.grid(True, linestyle="--", alpha=0.7)

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.2f}"))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:,.2f}"))

    def _create_bar_plot(self, df, ax):
        """Create an enhanced bar chart with insights"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()

        if not x_col or not y_col:
            messagebox.showwarning("Warning", "Please select X and Y columns")
            return
        # Only keep top 20 values to avoid overcrowded plots
        grouped_data = df.groupby(x_col)[y_col].mean().reset_index()

        if self.sort_bars_var.get():
            grouped_data = grouped_data.sort_values(by=y_col, ascending=False)

        if len(grouped_data) > 20:
            grouped_data = grouped_data.head(20)
            ax.set_title(ax.get_title() + " (Top 20)", fontsize=14)

        orientation = self.bar_orient_var.get()
        palette = self.bar_palette_var.get()

        if orientation == "horizontal":
            sns.barplot(
                x=y_col,
                y=x_col,
                data=grouped_data,
                palette=palette,
                ax=ax,
            )

            ax.set_xlabel(f"{y_col}", fontsize=12)
            ax.set_ylabel(f"{x_col}", fontsize=12)

            if self.bar_values_var.get():
                for i, v in enumerate(grouped_data[y_col]):
                    ax.text(
                        v + (0.01 * grouped_data[y_col].max()),
                        i,
                        f"{v:.2f}",
                        va="center",
                        fontweight="bold",
                    )
        else:
            sns.barplot(
                x=x_col,
                y=y_col,
                data=grouped_data,
                palette=palette,
                ax=ax,
            )

            ax.set_xlabel(f"{x_col}", fontsize=12)
            ax.set_ylabel(f"{y_col}", fontsize=12)

            if self.bar_values_var.get():
                for i, v in enumerate(grouped_data[y_col]):
                    ax.text(
                        i,
                        v + (0.01 * grouped_data[y_col].max()),
                        f"{v:.2f}",
                        ha="center",
                        va="bottom",
                        fontweight="bold",
                    )

        if orientation == "vertical" and len(grouped_data) > 5:
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        total = grouped_data[y_col].sum()
        mean = grouped_data[y_col].mean()
        ax.text(
            0.02,
            0.95,
            f"Total: {total:.2f}\nMean: {mean:.2f}",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:,.2f}"))

        self.figure.tight_layout()

    def _create_histogram_plot(self, df, ax):
        """Create an enhanced histogram with insights"""
        x_col = self.x_var.get()

        if not x_col:
            messagebox.showwarning("Warning", "Please select a column")
            return

        try:
            bins = int(self.bins_var.get())
        except ValueError:
            bins = 20

        color = self.hist_color_var.get()

        data = df[x_col].dropna()

        if len(data) == 0:
            messagebox.showwarning("Warning", "No valid data points for histogram")
            return

        sns.histplot(
            data,
            bins=bins,
            kde=self.kde_var.get(),
            ax=ax,
            color=color,
            edgecolor="white",
            line_kws={"linewidth": 2},
        )

        if self.hist_stats_var.get():

            mean = data.mean()
            median = data.median()
            std = data.std()
            min_val = data.min()
            max_val = data.max()

            stats_text = (
                f"Mean: {mean:.4f}\n"
                f"Median: {median:.4f}\n"
                f"Std Dev: {std:.4f}\n"
                f"Min: {min_val:.4f}\n"
                f"Max: {max_val:.4f}\n"
                f"Count: {len(data)}"
            )
            
            ax.text(
                0.95,
                0.95,
                stats_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment="top",
                horizontalalignment="right",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            )

            ax.axvline(mean, color="red", linestyle="--", alpha=0.7, label="Mean")
            ax.axvline(median, color="green", linestyle="-", alpha=0.7, label="Median")
            ax.legend()

        ax.set_xlabel(f"{x_col}", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.2f}"))

    def _create_box_plot(self, df, ax):
        """Create an enhanced box plot with insights"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()

        if not x_col or not y_col:
            messagebox.showwarning("Warning", "Please select X and Y columns")
            return

        valid_data = df[[x_col, y_col]].dropna()

        if len(valid_data) == 0:
            messagebox.showwarning("Warning", "No valid data points for box plot")
            return

        notch = self.notch_var.get()
        showmeans = self.mean_var.get()
        palette = self.box_palette_var.get()

        sns.boxplot(
            x=x_col,
            y=y_col,
            data=valid_data,
            notch=notch,
            showmeans=showmeans,
            meanprops={
                "marker": "o",
                "markerfacecolor": "white",
                "markeredgecolor": "black",
            },
            palette=palette,
            ax=ax,
        )
        if self.points_var.get():
            sns.swarmplot(
                x=x_col,
                y=y_col,
                data=valid_data,
                color="black",
                alpha=0.5,
                size=4,
                ax=ax,
            )

        categories = valid_data[x_col].unique()
        stats_text = ""

        if len(categories) <= 5:
            for cat in categories:
                cat_data = valid_data[valid_data[x_col] == cat][y_col]
                stats_text += f"{cat}:\n"
                stats_text += f"  Count: {len(cat_data)}\n"
                stats_text += f"  Mean: {cat_data.mean():.2f}\n"
                stats_text += f"  Median: {cat_data.median():.2f}\n"
                stats_text += f"  StdDev: {cat_data.std():.2f}\n\n"

            ax.text(
                1.02,
                0.95,
                stats_text,
                transform=ax.transAxes,
                fontsize=9,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            )
            self.figure.subplots_adjust(right=0.75)

        ax.set_xlabel(f"{x_col}", fontsize=12)
        ax.set_ylabel(f"{y_col}", fontsize=12)

        if len(categories) > 5:
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:,.2f}"))

    def _create_heatmap_plot(self, df, ax):
        """Create an enhanced heatmap for correlation analysis"""
        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty or numeric_df.shape[1] < 2:
            messagebox.showwarning(
                "Warning", "Need at least two numeric columns for correlation analysis"
            )
            return

        corr_matrix = numeric_df.corr()

        mask = None
        if self.mask_var.get():
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        if self.cluster_var.get():
            import scipy.cluster.hierarchy as sch

            linkage = sch.linkage(corr_matrix, method="ward")

            dendro = sch.dendrogram(linkage, no_plot=True)
            reordered_idx = dendro["leaves"]

            corr_matrix = corr_matrix.iloc[reordered_idx, reordered_idx]

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        hm = sns.heatmap(
            corr_matrix,
            annot=self.annot_var.get(),
            cmap=self.cmap_var.get(),
            mask=mask,
            linewidths=0.5,
            ax=ax,
            fmt=".2f",
            square=True,
            cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
        )

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        plt.setp(ax.get_yticklabels(), rotation=0)

        ax.set_title(self.title_var.get(), fontsize=14, pad=20)

        if len(corr_matrix) > 1:  
            strong_corrs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)): 
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        strong_corrs.append(
                            (
                                corr_matrix.columns[i],
                                corr_matrix.columns[j],
                                corr_matrix.iloc[i, j],
                            )
                        )

            if strong_corrs:
                text = "Strong correlations:\n\n"
                for var1, var2, corr in sorted(
                    strong_corrs, key=lambda x: abs(x[2]), reverse=True
                ):
                    text += f"{var1} ↔ {var2}: {corr:.2f}\n"

                ax_text = self.figure.add_axes([0.7, 0.1, 0.25, 0.2])
                ax_text.axis("off")
                ax_text.text(
                    0,
                    1,
                    text,
                    verticalalignment="top",
                    fontsize=10,
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
                )

        self.figure.tight_layout()

    def _export_plot(self):
        """Export the current plot as an image file"""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            self.figure.savefig(
                file_path, dpi=300, bbox_inches="tight", transparent=False
            )
            self.app.status_var.set(f"Plot exported to {file_path}")
            messagebox.showinfo("Export Successful", f"Plot saved to {file_path}")

    def on_show(self):
        """Called when the panel is shown"""
        self._update_column_list()
        self._on_chart_type_changed(None)
