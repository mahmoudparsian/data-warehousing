---
marp: true
paginate: true
size: 16:9
---

# Vehicles Lakehouse SQL Exercises (Student)
### DuckDB • Bronze → Silver → Gold

![bg right:45% w:520](vehicles_lakehouse_etl_diagram.png)

---

## Assumptions

You created:
- `bronze_vehicles` (view)
- `silver_vehicles` (table)
- `gold_kpi_month` (view)

---

## Q1 — Schema & missingness (Bronze)

Write SQL to show:
- inferred schema (names + types)
- missing counts for: price, year, odometer, manufacturer, model, posting_date

---

## Q2 — Price trend (Gold)

Using `gold_kpi_month`, return:
- month, median_price, p90_price

Then describe 2–3 bullet observations.

---

## Q3 — Manufacturer market share (Silver)

Return top 15 manufacturers by listing count, including:
- manufacturer, listings
- percent share of total listings

---

## Q4 — Depreciation curve (Silver)

Compute median price by `vehicle_age` (0–30).
Only include ages with at least 500 listings.

---

## Q5 — State comparison (Silver)

Find the 10 states with the **highest median price**,
only for states with at least 3000 listings.

---

## Q6 — Outliers by month (Silver)

For each month, find the top 3 most expensive listings.
Return: month, state, manufacturer, model, price, rank_in_month.

(Hint: window functions.)

---
