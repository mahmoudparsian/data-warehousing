# 📊 Basic Data Exploration Report

## 1. Introduction
- Source of the dataset
- Brief description of the dataset
- Purpose of this exploration

## 2. Loading the Data
- Import necessary libraries
- Load dataset using Python `pandas`

## 3. Data Summary
- Display first few rows (`df.head()`)
- Show data shape and types (`df.shape`, `df.dtypes`)
- Basic statistics (`df.describe()`)

## 4. Missing Values
- Check for missing values (`df.isnull().sum()`)
- Decide how to handle them (drop or fill)

## 5. Univariate Analysis
- Visualize and describe individual columns
  - Histograms for numerical features
  - Bar plots for categorical features

## 6. Bivariate Analysis
- Explore relationships between two variables
  - Scatter plots (e.g., `age` vs `charges`)
  - Box plots (e.g., `smoker` vs `charges`)

## 7. Observations
- Summarize key insights
- Note patterns or anomalies for further investigation
