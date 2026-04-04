---
marp: true
theme: default
paginate: true
title: Assignment 2 — WHERE vs HAVING + Top-N
---

# Assignment 2 — SQL (DuckDB)

## Objective
- Understand difference between **WHERE** and **HAVING**
- Practice **GROUP BY**
- Practice **Top-N queries**

Dataset columns:
transaction_id, transaction_date, sale_type, product_name, price, quantity, gender, discount, country, age, sales_amount

---

# Question 1 — WHERE

### Task
Find all transactions where:
- country = 'USA'
- sales_amount > 1000

### Requirement
- Use **WHERE**
- Do NOT use GROUP BY

---

# Question 2 — GROUP BY + WHERE

### Task
Find total sales per product for:
- country = 'USA'

### Requirement
- Use **WHERE**
- Use GROUP BY product_name

---

# Question 3 — HAVING

### Task
Find products where:
- total sales > 1,000,000

### Requirement
- Use GROUP BY
- Use **HAVING**

---

# Question 4 — WHERE vs HAVING

### Task
Find countries where:
- transactions are only from 2025
- total sales > 5,000,000

### Requirement
- Use BOTH:
  - WHERE (for filtering rows)
  - HAVING (for filtering groups)

---

# Question 5 — Top-N (Important)

### Task
Find **Top 3 products by total sales per country**

### Requirement
- Use window function
- Use ROW_NUMBER()
- Use PARTITION BY country
- Do NOT use LIMIT alone

---

# Submission

For each question:
- Write SQL
- Add 2 bullet points explaining business insight
