# Exploratory Data Analysis (EDA)

This document contains **two parts in one downloadable Markdown file**:

1. **10 lecture slides** (Markdown slide format)
2. **A complete, end-to-end EDA example** using **Python (Jupyter Notebook style)** on a realistic dataset

You can:

- Use Part 1 directly as slides

- Copy Part 2 into a Jupyter notebook (`.ipynb`) or run it cell-by-cell

---

# Part 1 — EDA Lecture Slides (10 Slides)

---

## Slide 1 — What Is Exploratory Data Analysis (EDA)?

**Exploratory Data Analysis (EDA)** is the process of:

- Understanding a dataset
- Discovering patterns and anomalies
- Checking assumptions
- Preparing data for modeling or analytics

EDA is **not about modeling** — it is about **understanding the data first**.

---

## Slide 2 — Why EDA Is Important

Without EDA:

- Models may be incorrect or misleading
- Data quality issues remain hidden
- Business conclusions may be wrong

EDA helps answer:

- Is the data complete?
- Is it consistent?
- Does it make sense?

---

## Slide 3 — Typical EDA Questions

- How big is the dataset?
- What columns exist and what do they mean?
- Are there missing values?
- Are there outliers?
- How are variables distributed?
- How do variables relate to each other?

---

## Slide 4 — EDA Process Overview

Typical EDA steps:

1. Understand the dataset
2. Inspect schema and data types
3. Check missing values
4. Study distributions
5. Detect outliers
6. Analyze relationships
7. Summarize findings

EDA is **iterative**, not linear.

---

## Slide 5 — Step 1: Understand the Dataset

- Source of the data
- Business meaning
- Time span
- Unit of measurement

Always ask:
> “What does one row represent?”

---

## Slide 6 — Step 2: Data Types & Structure

- Numerical vs categorical columns
- Date/time fields
- Identifiers vs measures

Correct data types are **critical** for analysis.

---

## Slide 7 — Step 3: Missing Values

Questions:

- Which columns have missing values?
- How many?
- Random or systematic?

Strategies:

- Drop
- Impute
- Flag

---

## Slide 8 — Step 4: Distributions & Outliers

- Histograms
- Box plots
- Summary statistics

Outliers may indicate:
- Errors
- Rare events
- Important business signals

---

## Slide 9 — Step 5: Relationships Between Variables

- Correlation analysis
- Group-by aggregations
- Trend analysis over time

EDA often reveals **unexpected relationships**.

---

## Slide 10 — EDA Deliverables

A good EDA produces:

- Clean summary statistics
- Visual insights
- Data quality findings
- Actionable recommendations

EDA is the **foundation** of analytics and data science.

---

# Part 2 — Complete EDA Example (Python + Jupyter)

## Dataset Description

We use a **retail sales dataset** with the following columns:

- `order_id`
- `order_date`
- `customer_id`
- `country`
- `category`
- `quantity`
- `unit_price`
- `revenue`

Each row represents **one product sale in one order**.

---

## Cell 1 — Import Libraries

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

---

## Cell 2 — Load Dataset

```python
df = pd.read_csv("retail_sales.csv")
df.head()
```

---

## Cell 3 — Basic Dataset Overview

```python
df.shape
```

```python
df.info()
```

---

## Cell 4 — Summary Statistics

```python
df.describe()
```

---

## Cell 5 — Missing Value Analysis

```python
df.isnull().sum()
```

Percentage of missing values:

```python
(df.isnull().mean() * 100).round(2)
```

---

## Cell 6 — Date Handling

```python
df['order_date'] = pd.to_datetime(df['order_date'])
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
```

---

## Cell 7 — Distribution of Revenue

```python
plt.hist(df['revenue'], bins=30)
plt.xlabel("Revenue")
plt.ylabel("Frequency")
plt.title("Revenue Distribution")
plt.show()
```

---

## Cell 8 — Detecting Outliers (Box Plot)

```python
plt.boxplot(df['revenue'])
plt.ylabel("Revenue")
plt.title("Revenue Outliers")
plt.show()
```

---

## Cell 9 — Revenue by Country

```python
revenue_by_country = df.groupby('country')['revenue'].sum().sort_values(ascending=False)
revenue_by_country
```

---

## Cell 10 — Revenue Trend Over Time

```python
revenue_by_year = df.groupby('year')['revenue'].sum()
revenue_by_year.plot(kind='line')
plt.xlabel("Year")
plt.ylabel("Total Revenue")
plt.title("Yearly Revenue Trend")
plt.show()
```

---

## Cell 11 — Category-Level Analysis

```python
df.groupby('category')['revenue'].agg(['count', 'mean', 'sum'])
```

---

## Cell 12 — Key EDA Findings (Example)

- Revenue is right-skewed
- A small number of orders generate very high revenue
- Strong growth observed in recent years
- Certain categories dominate total revenue

---

## Final Notes

This EDA:
- Identifies data quality issues
- Reveals distributions and trends
- Provides insights before modeling

EDA should **always precede** machine learning, OLAP analysis, or dashboarding.

---

## End of Document

