# What is a Data Exploration

* **Data exploration**, also called **exploratory data analysis (EDA)**, is the process of examining and understanding a dataset before formal modeling or hypothesis testing. 

* **Data exploration** helps uncover patterns, spot anomalies, test assumptions, and check the quality of the data.

---

### 🔍 Key Goals of Data Exploration:

1. **Understand the structure** of the data (types, dimensions, columns).
2. **Summarize** features using statistics (mean, median, mode, std).
3. **Identify missing or unusual values.**
4. **Visualize distributions** and relationships between variables.
5. **Spot potential outliers or data quality issues.**

---

### 🧰 Common Techniques:

Let `df` (as a DataFrame) represents your data set:


* `df.info()`
* `df.describe()` for basic summary
* `value_counts()`, 
* `groupby()` for categorical patterns
* Plots:

  * Histograms, Boxplots (distribution)
  * Scatter plots, Pair plots (relationships)
  * Heatmaps (correlations)
* Handling nulls: `df.isnull().sum()`
* Checking duplicates: `df.duplicated().sum()`

### 📈 Example Tools in Python:

* DuckDB
* Pandas
* Seaborn
* Matplotlib
* Plotly

-------

# Hands-on data exploration (EDA) example using the Iris dataset with Python.

---

## 🏷️ **Step-by-Step Iris Data Exploration**

### Step 1: Load necessary libraries

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
```

### Step 2: Load the Iris dataset from Seaborn

```python
iris = sns.load_dataset("iris")
```

### Step 3: View the first few rows

```python
print(iris.head())
```

---

### 🧾 **Step 4: Basic Information and Summary**

```python
# Dataset info
iris.info()

# Summary statistics
iris.describe()

# Check for nulls
print("Missing values:\n", iris.isnull().sum())
```

---

### 🧮 **Step 5: Univariate Analysis**

```python
# Distribution of each numerical column
iris.hist(bins=15, figsize=(10, 6), color='skyblue')
plt.tight_layout()
plt.show()

# Count plot for the target class
sns.countplot(data=iris, x='species')
plt.title('Count of Each Species')
plt.show()
```

---

### 🔁 **Step 6: Bivariate Analysis**

```python
# Scatter plot: sepal_length vs sepal_width
sns.scatterplot(data=iris, x='sepal_length', y='sepal_width', hue='species')
plt.title('Sepal Length vs Width')
plt.show()

# Pair plot to explore all relationships
sns.pairplot(iris, hue="species")
plt.show()
```

---

### 🔗 **Step 7: Correlation Analysis**

```python
# Correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(iris.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()
```

---

### ✅ **Conclusion / Insights**

You might summarize:

* Species differ clearly in petal dimensions.
* Strong correlation between petal length & petal width.
* Sepal width has the weakest correlation with other features.

---
