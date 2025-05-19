"""
DataManager - Core class for data management operations
"""

import pandas as pd
import numpy as np
import pickle
import os


class DataManager:
    """Handles data loading, processing, and management"""

    def __init__(self):
        """Initialize DataManager"""
        self.dataframe = None
        self.original_dataframe = None
        self.file_path = None
        self.file_name = None
        self.history = []

    def load_dataset(self, file_path):
        """Load dataset from file with encoding detection"""
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

        encodings = ["utf-8", "latin1", "iso-8859-1", "cp1252"]

        if file_path.endswith(".csv"):
            for encoding in encodings:
                try:
                    self.dataframe = pd.read_csv(
                        file_path,
                        encoding=encoding,
                        on_bad_lines="skip",
                        low_memory=True,
                    )
                    break  
                except UnicodeDecodeError:
                    continue  
                except Exception as e:
                    raise ValueError(f"Error reading CSV file: {str(e)}")
            else:  
                raise ValueError(
                    "Could not determine the file encoding. The file might be corrupted."
                )

        elif file_path.endswith((".xls", ".xlsx")):
            try:
                self.dataframe = pd.read_excel(file_path)
            except Exception as e:
                raise ValueError(f"Error reading Excel file: {str(e)}")
        else:
            raise ValueError(
                f"Unsupported file format. Only CSV and Excel files are supported."
            )

        if len(self.dataframe) > 100000: 
            self.original_dataframe = self.dataframe.sample(
                n=100000, random_state=42
            ).copy()
        else:
            self.original_dataframe = self.dataframe.copy()

        self.history = []

        return self.dataframe

    def save_project(self, file_path):
        """Save the current project state"""
        project_data = {
            "dataframe": self.dataframe,
            "original_dataframe": self.original_dataframe,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "history": self.history,
        }

        with open(file_path, "wb") as f:
            pickle.dump(project_data, f)

    def load_project(self, file_path):
        """Load a saved project"""
        with open(file_path, "rb") as f:
            project_data = pickle.load(f)

        self.dataframe = project_data["dataframe"]
        self.original_dataframe = project_data["original_dataframe"]
        self.file_path = project_data["file_path"]
        self.file_name = project_data["file_name"]
        self.history = project_data["history"]

        return self.dataframe

    def clean_missing_values(self, column, method, value=None):
        """Clean missing values in a column"""
        if self.dataframe is None or column not in self.dataframe.columns:
            return None

        self.history.append(
            {
                "operation": "clean_missing",
                "column": column,
                "method": method,
                "value": value,
            }
        )

        df = self.dataframe.copy()

        if method == "drop":
            self.dataframe = df.dropna(subset=[column])
        elif method == "mean" and pd.api.types.is_numeric_dtype(df[column]):
            self.dataframe[column] = df[column].fillna(df[column].mean())
        elif method == "median" and pd.api.types.is_numeric_dtype(df[column]):
            self.dataframe[column] = df[column].fillna(df[column].median())
        elif method == "mode":
            mode_value = df[column].mode()[0] if not df[column].mode().empty else None
            self.dataframe[column] = df[column].fillna(mode_value)
        elif method == "value":
            self.dataframe[column] = df[column].fillna(value)

        return self.dataframe

    def remove_duplicates(self):
        """Remove duplicate rows"""
        if self.dataframe is None:
            return 0

        self.history.append({"operation": "remove_duplicates"})

        original_rows = len(self.dataframe)
        self.dataframe = self.dataframe.drop_duplicates().reset_index(drop=True)

        return original_rows - len(self.dataframe)

    def handle_outliers(self, column, method):
        """Handle outliers in a numeric column"""
        if self.dataframe is None or column not in self.dataframe.columns:
            return None

        if not pd.api.types.is_numeric_dtype(self.dataframe[column]):
            return None

        self.history.append(
            {
                "operation": "handle_outliers",
                "column": column,
                "method": method,
            }
        )

        q1 = self.dataframe[column].quantile(0.25)
        q3 = self.dataframe[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        if method == "cap":
            self.dataframe[column] = self.dataframe[column].clip(
                lower=lower_bound, upper=upper_bound
            )
        elif method == "remove":
            self.dataframe = self.dataframe[
                (self.dataframe[column] >= lower_bound)
                & (self.dataframe[column] <= upper_bound)
            ]

        return self.dataframe

    def get_column_stats(self, column):
        """Get basic statistics for a column"""
        if self.dataframe is None or column not in self.dataframe.columns:
            return None

        stats = {}
        series = self.dataframe[column]
        stats["count"] = len(series)
        stats["missing"] = series.isna().sum()
        stats["unique"] = series.nunique()

        if pd.api.types.is_numeric_dtype(series):
            stats["mean"] = series.mean()
            stats["median"] = series.median()
            stats["std"] = series.std()
            stats["min"] = series.min()
            stats["max"] = series.max()
            stats["skew"] = series.skew()
            stats["kurtosis"] = series.kurtosis()

            stats["25%"] = series.quantile(0.25)
            stats["50%"] = series.quantile(0.50)
            stats["75%"] = series.quantile(0.75)

        stats["dtype"] = str(series.dtype)

        if pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(
            series
        ):
            value_counts = series.value_counts(normalize=True)
            stats["top_values"] = value_counts.head(5).to_dict()

        return stats

    def reset_to_original(self):
        """Reset the dataframe to the original state"""
        if self.original_dataframe is not None:
            self.dataframe = self.original_dataframe.copy()
            self.history = []

        return self.dataframe

    def get_numeric_columns(self):
        """Get list of numeric columns"""
        if self.dataframe is None:
            return []

        return list(self.dataframe.select_dtypes(include=["number"]).columns)

    def get_categorical_columns(self):
        """Get list of categorical columns"""
        if self.dataframe is None:
            return []

        return list(
            self.dataframe.select_dtypes(include=["object", "category"]).columns
        )
