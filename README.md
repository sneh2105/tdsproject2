# Autolysis: Automated Data Analysis and Storytelling

## Overview

`autolysis.py` is a Python script designed to automate data analysis and storytelling. It processes datasets, creates meaningful visualizations, and generates AI-driven narratives summarizing the insights.

---

## Features

1. **Dataset Analysis**:
   - Summarizes the dataset, including shape, data types, missing values, and sample rows.

2. **Visualizations**:
   - **Correlation Heatmap**: Displays relationships between numerical features.
   - **Clustering Visualization**: Groups data into clusters using K-Means and visualizes them with PCA.

3. **AI-Driven Narratives**:
   - Automatically generates a story summarizing the dataset and insights using GPT-4o-Mini.

4. **Compatibility**:
   - Works with any valid CSV file containing numerical data.

---

## Requirements

### Python Version
- Python >= 3.9

### Dependencies
The script requires the following Python libraries:
- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `openai`
- `tenacity`

Install them using:
```bash
pip install pandas matplotlib seaborn scikit-learn openai tenacity

