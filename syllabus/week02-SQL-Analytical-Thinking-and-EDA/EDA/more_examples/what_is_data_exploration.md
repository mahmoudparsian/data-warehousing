# What is Data Exploration?

**Data exploration**, also called **exploratory data analysis (EDA)**, is the
process of examining and understanding a dataset *before* formal modeling or
hypothesis testing. It helps you uncover patterns, spot anomalies, test
assumptions, and assess data quality.

---

## Key Goals

1. **Understand the structure** — data types, dimensions, column names.
2. **Summarize features** — mean, median, mode, standard deviation.
3. **Identify missing or unusual values.**
4. **Visualize distributions** and relationships between variables.
5. **Spot outliers and data-quality issues.**

---

## Common Techniques

### With SQL (DuckDB)

```sql
-- schema & types
DESCRIBE my_table;

-- summary statistics
SELECT
    COUNT(*)          AS total_rows,
    AVG(price)        AS avg_price,
    MEDIAN(price)     AS median_price,
    MIN(price)        AS min_price,
    MAX(price)        AS max_price
FROM my_table;

-- missing-value audit
SELECT
    SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END) AS null_count
FROM my_table;

-- categorical patterns
SELECT category, COUNT(*) AS cnt
FROM my_table
GROUP BY category
ORDER BY cnt DESC;
```

### With Python (Pandas)

```python
df.info()                  # schema & non-null counts
df.describe()              # summary statistics
df.isnull().sum()          # missing values
df.duplicated().sum()      # duplicate rows
df.value_counts()          # frequency counts
df.groupby("col").mean()   # categorical patterns
```

### Visualization

| Chart Type   | Purpose                |
|--------------|------------------------|
| Histogram    | Distribution of a variable |
| Boxplot      | Spread and outliers    |
| Scatter plot | Relationship between two variables |
| Pair plot    | All pairwise relationships |
| Heatmap      | Correlation matrix     |

### Tools

DuckDB, Pandas, Seaborn, Matplotlib, Plotly

---

## Hands-on Example: Iris Dataset

A step-by-step EDA using the classic Iris dataset in Python.

### Step 1 — Load libraries

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
```

### Step 2 — Load the dataset

```python
iris = sns.load_dataset("iris")
```

### Step 3 — Inspect the first few rows

```python
iris.head()
```

---

### Step 4 — Basic information and summary

```python
iris.info()

iris.describe()

print("Missing values:\n", iris.isnull().sum())
```

---

### Step 5 — Univariate analysis

```python
# distribution of each numerical column
iris.hist(bins=15, figsize=(10, 6), color="skyblue")
plt.tight_layout()
plt.show()

# count of each species
sns.countplot(data=iris, x="species")
plt.title("Count of Each Species")
plt.show()
```

---

### Step 6 — Bivariate analysis

```python
# scatter plot: sepal length vs. sepal width
sns.scatterplot(data=iris, x="sepal_length", y="sepal_width", hue="species")
plt.title("Sepal Length vs. Width")
plt.show()

# pair plot across all features
sns.pairplot(iris, hue="species")
plt.show()
```

---

### Step 7 — Correlation analysis

```python
plt.figure(figsize=(8, 6))
sns.heatmap(iris.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
```

---

### Insights

- Species differ most clearly in **petal dimensions**.
- **Petal length and petal width** are strongly correlated.
- **Sepal width** has the weakest correlation with other features.

---

*Data Warehousing — Week 3: Classic Data Warehousing*
