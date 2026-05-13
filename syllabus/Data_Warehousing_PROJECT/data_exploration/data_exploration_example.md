### 🗂 Basic Table of Contents for a Data Exploration Report

1. **Introduction**
2. **Loading the Data**
3. **Data Overview**

   * Shape and Data Types
   * Sample Rows
4. **Missing Values**
5. **Descriptive Statistics**
6. **Univariate Analysis**
7. **Bivariate Analysis**
8. **Observations & Insights**

---

### 🐍 Complete Python Example

We’ll use a small sample dataset similar to an "insurance.csv" file.

#### 1. Setup and Load Data

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data
data = {
    'age': [19, 18, 28, 45, 34],
    'gender': ['female', 'male', 'male', 'female', 'male'],
    'bmi': [27.9, 33.77, 33.0, 28.5, 31.0],
    'children': [0, 1, 3, 2, 1],
    'smoker': ['yes', 'no', 'no', 'yes', 'no'],
    'region': ['west', 'south-east', 'south-west', 'north', 'east'],
    'charges': [16884.92, 1725.55, 4449.46, 21984.5, 12365.0]
}

df = pd.DataFrame(data)
```

#### 2. Data Overview

```python
# Shape and data types
print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)

# First few rows
df.head()
```

#### 3. Missing Values

```python
# Check for missing values
df.isnull().sum()
```

#### 4. Descriptive Statistics

```python
df.describe()
```

#### 5. Univariate Analysis

```python
# Histogram for 'charges'
sns.histplot(df['charges'], kde=True)
plt.title("Distribution of Charges")
plt.show()

# Countplot for 'smoker'
sns.countplot(x='smoker', data=df)
plt.title("Smoker Count")
plt.show()
```

#### 6. Bivariate Analysis

```python
# Scatter plot: age vs charges
sns.scatterplot(x='age', y='charges', hue='smoker', data=df)
plt.title("Age vs Charges by Smoker")
plt.show()

# Box plot: smoker vs charges
sns.boxplot(x='smoker', y='charges', data=df)
plt.title("Charges by Smoking Status")
plt.show()
```

#### 7. Observations & Insights

```markdown
- Smokers tend to have higher charges.
- Age and number of children seem to affect insurance charges.
- No missing data detected.
- BMI and charges show some variation but no clear linear trend in this small dataset.
```

---

