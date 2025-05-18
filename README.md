# Datox - No-Code Data Science Platform

A desktop application for data analysis and visualization without coding.

## Features

- Data import from CSV, Excel, and other formats
- Data cleaning and transformation
- Statistical analysis
- Data visualization
- Project saving and loading

## Installation

1. Make sure you have Python 3.9+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   or
   ```
   pip install numpy pandas pandastable matplotlib scipy
   ```

3. Run the application:
   ```
   python main.py
   ```

## Usage Guide

### Loading Data
Click "Open Dataset" to load your data from CSV, Excel, or other supported formats.

### Data Cleaning
Navigate to the "Data Cleaning" tab to handle missing values and outliers.

### Visualization
Use the "Visualization" tab to create charts and plots.

### Statistics
The "Statistics" tab provides descriptive statistics and hypothesis testing.

## Troubleshooting

If you encounter "cannot use geometry manager pack inside . which already has slaves managed by grid" errors:
- This is a Tkinter layout conflict. Make sure all widgets in the same container use the same geometry manager.

If panels don't appear properly:
- Try resizing the window or reopening the application.

## Development Status

Current working components:
- Data loading and viewing
- Basic UI structure

In progress:
- Data cleaning functionality
- Visualization features
- Statistical analysis
