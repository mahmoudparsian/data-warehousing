# Week 3 Lab — Student Version
## Bike Store Data Warehouse + OLAP Queries

## Lab Goal
This lab helps you practice:
- identifying fact and dimension tables
- querying a star schema
- answering business questions with warehouse SQL
- using OLAP-style analysis

---

## Part A — Understand the Warehouse

### Task 1
Explain the difference between:
- fact table
- dimension table
- grain

### Task 2
For the Bike Store warehouse:
- identify the fact table
- identify all dimension tables
- state the grain of the fact table

---

## Part B — Core Analytical Queries

### Task 3 — Total Revenue
Write a query to calculate total revenue from the fact table.

### Task 4 — Revenue by Store
Write a query to show revenue by store.

### Task 5 — Revenue by Category
Write a query to show revenue by product category.

### Task 6 — Revenue by Brand
Write a query to show revenue by brand.

### Task 7 — Revenue by Year
Write a query to show revenue by year.

### Task 8 — Revenue by Year and Month
Write a query to show revenue by year and month.

---

## Part C — OLAP Thinking

### Task 9 — Roll-Up
Show revenue by year only.

### Task 10 — Drill-Down
Show revenue by year and month.

### Task 11 — Slice
Show revenue for stores in California.

### Task 12 — Dice
Show 2023 revenue for Accessories only.

---

## Part D — Business Analysis

### Task 13 — Top Customers
Show the top 5 customers by total revenue.

### Task 14 — Top Products per Store
Use a window function to return the top 2 products in each store by revenue.

### Task 15 — Staff Performance
Show revenue by staff member.

### Task 16 — Category Profitability View
Show average order-line revenue by category.

---

## Part E — Reflection

Answer in plain English:

1. Why is a star schema easier for analytics than a normalized OLTP schema?
2. Why is the grain of the fact table so important?
3. Which query in this lab was most useful from a business perspective, and why?
4. How does Week 3 connect to Week 2 window functions?
