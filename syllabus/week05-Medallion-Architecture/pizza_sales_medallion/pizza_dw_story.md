---

title: Building a Data Warehouse – Pizza Shop Case Study
author: Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead

---

# 🍕 Pizza Shop Data Warehouse

	•	🍕 Business story
	•	🧱 Data warehouse motivation
	•	📋 Detailed business requirements (refined)
	•	🎯 Ready for classroom use

⸻




## From Raw Data to Business Insights

- Real-world dataset (2015–2016)
- Messy + evolving data
- Goal: Build a **modern data warehouse**

---

# 📖 Business Story

We operate a **pizza shop** with:

- Daily customer orders
- Multiple pizza types & sizes
- New products introduced in 2016

We want to answer:

- 📊 What are our best-selling pizzas?
- ⏰ When are peak hours?
- 💰 How is revenue evolving?

---

# 🧩 Data Sources

We receive raw data from:

- `orders_2015.csv`, 
- `orders_2016.csv`
- `order_details_2015.csv`, 
- `order_details_2016.csv`
- `pizzas.csv`
- `pizza_types.csv`

⚠️ Data is **messy and inconsistent**

---

# 🚨 Real-World Challenges

Our raw data contains:

- Multiple date formats
- Missing values
- Duplicate records
- Invalid references
- Schema inconsistencies

👉 We must **clean and standardize** before analysis

---

# 🧱 Why Data Warehouse?

We need:

- ✔ Clean, reliable data
- ✔ Consistent schema
- ✔ Fast analytical queries
- ✔ Business-ready datasets

👉 Solution: **Medallion Architecture**

- 🟫 Bronze (raw)
- ⚪ Silver (clean)
- 🟡 Gold (business-ready)

---

# 📘 Business Requirements (Orders)

## 1. Date Standardization

- Formats may include:
  - YYYY-MM-DD
  - MM/DD/YYYY

👉 Must convert to:

- `YYYY-MM-DD`

❗ If parsing fails → **DROP record**

---

# 📘 Orders (continued)

## 2. Missing order_id

- If `order_id` is NULL → **DROP**

## 3. Uniqueness

- `order_id` must be **unique**

## 4. Duplicate Records

- If all fields identical → **REMOVE**

---

# 📘 Business Requirements <br> (Order Details)

## 1. Schema Validation

Each record must have exactly:

- `order_details_id`
- `order_id`
- `pizza_id`
- `quantity`

❗ Otherwise → **DROP**

---

# 📘 Order Details (continued)

## 2. NULL Handling

- Any NULL field → **DROP**

## 3. Referential Integrity

- `order_id` must exist in `orders`
- `pizza_id` must exist in `pizzas`

❗ Otherwise → **DROP**

---

# 📘 Order Details (continued)

## 4. Quantity Rules

- Must be **integer > 0**

## 5. Primary Key

- `order_details_id` must be **unique**

---

# 🚀 What Comes Next?

We will build:

1. 🟫 Bronze Layer (raw ingestion)
2. ⚪ Silver Layer (clean + validated)
3. 🟡 Gold Layer (star schema)
4. 📊 BI Layer (OLAP queries)

👉 Final goal: **Answer real business questions**

---

# 🎯 Key Learning Outcomes

Students will learn:

- Data cleaning & validation
- Schema design (fact & dimension)
- SQL for analytics
- Real-world DW thinking

---

# 🍕 Let’s Build It!

Next step:

👉 Implement in **Jupyter Notebook (DuckDB)**

- Raw → Bronze → Silver → Gold → BI


⸻

🎯 Why this is strong for your class

	•	Clean narrative (not just rules)
	•	Real-world framing
	•	Progressive build-up
	•	Sets up your next notebook perfectly

⸻

🚀 Next Step

we move to:

👉 Jupyter Notebook (full pipeline)
with:

	•	Bronze ingestion
	•	Silver cleaning (based on these rules)
	•	Gold star schema
	•	OLAP queries + visualization

