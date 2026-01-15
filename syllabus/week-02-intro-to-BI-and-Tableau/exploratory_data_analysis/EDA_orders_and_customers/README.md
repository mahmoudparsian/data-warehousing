# EDA for Customers and Orders

	Let's have 2 data sets (customers and orders) 
	and say that they are linked by a single common 
	column (customer_id).
	
	Provide a complete working EDA using puython 
	for these two datasets: provide a descent size 
	of these data sets. 


⸻

# 📦 Datasets Overview

## 1️⃣ `customers.csv` (5,000 rows)

Grain: one row per customer

Columns

	•	customer_id (PK)
	•	country (USA, Canada, UK, Germany, France)
	•	age
	•	gender
	•	signup_year

## 2️⃣ `orders.csv` (20,000 rows)

Grain: one row per order

Columns

	•	order_id (PK)
	•	customer_id (FK → customers)
	•	order_amount
	•	order_year
	•	channel (Online / In-Store)
	

## 🔗 Single join key: `customer_id`

⸻

## 📊 What the EDA Notebook Covers

The Jupyter notebook (`EDA_orders_and_customers.ipynb`) includes:

### ✔ Data Loading

	•	Reads both CSVs
	•	Quick inspection with head()

### ✔ Structural EDA

	•	.info() for schema and null checks
	•	Row counts and data types

### ✔ Statistical EDA

	•	Descriptive statistics
	•	Categorical summaries

### ✔ Univariate Analysis

	•	Customer age distribution
	•	Orders by channel

### ✔ Relational EDA

	•	Inner join on customer_id
	•	Joined dataset exploration

### ✔ Aggregations

	•	Average order amount by country

### ✔ Bivariate Analysis

	•	Order amount vs. customer age (scatter plot)

### ✔ Business-style Insights

	•	Country-level revenue patterns
	•	Channel balance
	•	Demographic effects

⸻

