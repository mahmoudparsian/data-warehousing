---
marp: true
theme: default
paginate: true
title: Week 8 — Session 2 — KPIs That Add Up, and Data Marts
---

# Week 8 — Session 2
## KPIs That Add Up (and Those That Don't) · Data Marts

Examples use the online-sales star from week 4 (`week04…/OLAP/OLAP_by_DuckDB/`, 1M sales lines).
Lab 8.2 applies the same ideas to the pizza shop.

---

# ➕ Three Kinds of Measures

| Kind | Can you SUM it… | Examples |
|---|---|---|
| **Additive** | across **all** dimensions | revenue, quantity, discount amount |
| **Semi-additive** | across some, **not over time** | account balance, inventory on hand |
| **Non-additive** | never: recompute from parts | prices, ratios, averages, percentages, **distinct counts** |

👉 Store additive **parts** in the fact table; compute ratios **at query time** from summed parts

---

# ❌ Distinct Counts Don't Add Up

```sql
-- customers per month in 2024, summed over the 12 months
WITH m AS (SELECT d.month_of_year, COUNT(DISTINCT s.customer_key) AS n
           FROM sales s JOIN dates d USING (date_key)
           WHERE d.year = 2024 GROUP BY 1)
SELECT SUM(n) FROM m;                                   -- 50,876

SELECT COUNT(DISTINCT s.customer_key)
FROM sales s JOIN dates d USING (date_key) WHERE d.year = 2024;   -- 5,000
```

👉 Most customers buy in many months. "Monthly customers, summed" counts them **10×**

---

# ❌ Average of What?

| Question | Wrong (looks fine) | Right |
|---|---|---|
| average order value | `AVG(line_amount)` (= average **line**) | `SUM(revenue) / COUNT(DISTINCT order_id)` |
| average price paid | `AVG(unit_price)` (every line counts once) | `SUM(revenue) / SUM(quantity)` (weighted by units) |
| average across stores | `AVG(store_average)` | `SUM(revenue) / SUM(lines)` over all stores |
| revenue per customer | `AVG(total_amount)` = 235.49 | `SUM(total_amount) / COUNT(DISTINCT customer_key)` = **23,553** (2024) |

👉 Always ask: **average per what?** (per line, per order, per unit, per customer, per day)

---

# 🧮 The Safe Pattern

```sql
SELECT channel,
       SUM(revenue)                              AS revenue,        -- additive
       COUNT(DISTINCT order_id)                  AS orders,         -- non-additive: recount
       SUM(revenue) / COUNT(DISTINCT order_id)   AS avg_order_value -- ratio of sums
FROM fact_sales
GROUP BY channel;
```

- Sum the **parts**, divide **last**
- Never average a column that is already an average
- Never sum a distinct count from a coarser table

---

# 🏪 Data Marts

A **data mart** = a small Gold table (or view) shaped for **one** group of users

| Mart | Grain | For |
|---|---|---|
| `mart_daily_channel` | day × channel | operations: staffing, daily targets |
| `mart_menu_performance` | year × product | menu / marketing: what to keep, promote, drop |
| `mart_store_month` | store × month | regional managers |

- Built **from the star schema** (never from Silver directly), so every mart agrees with the others
- Pre-aggregated: fast dashboards, simple for BI tools
- Each mart **declares its grain**, like a fact table

---

# ✅ Check Every Mart Against the Fact

```sql
SELECT (SELECT SUM(revenue) FROM gold.mart_daily_channel) AS mart_revenue,
       (SELECT SUM(revenue) FROM gold.fact_sales)          AS fact_revenue,
       (SELECT SUM(orders)  FROM gold.mart_daily_channel)  AS mart_orders,
       (SELECT COUNT(DISTINCT channel || '|' || order_key) FROM gold.fact_sales) AS fact_orders;
```

- Revenue must match exactly (additive)
- Orders match **only** if an order never spans two rows of the mart (one order = one day + one channel ✓)
- If they don't match, the dashboard must not ship

---

# 🪟 Ranking Inside a Mart

```sql
SELECT d.year, p.product_name, SUM(s.total_amount) AS revenue,
       ROUND(100.0 * SUM(s.total_amount)
             / SUM(SUM(s.total_amount)) OVER (PARTITION BY d.year), 2) AS pct_of_year,
       RANK() OVER (PARTITION BY d.year ORDER BY SUM(s.total_amount) DESC) AS revenue_rank
FROM sales s JOIN dates d USING (date_key) JOIN products p USING (product_key)
GROUP BY d.year, p.product_name;      -- explicit GROUP BY (not GROUP BY ALL) with windows over aggregates
```

👉 `SUM(SUM(x)) OVER (…)`: the inner SUM is the GROUP BY aggregate, the outer is the window

---

# 📊 From Mart to Tableau

1. `COPY (SELECT * FROM gold.mart_… ) TO 'mart.csv' (HEADER);` (or Parquet)
2. Tableau: Connect → Text file → the CSV
3. Build each chart on the **mart's grain**; let Tableau **sum additive** columns only
4. For ratios (AOV), create a **calculated field**: `SUM([revenue]) / SUM([orders])`, not `AVG([aov])`

👉 Same rule as SQL: sum the parts, divide last

---

# ✅ Summary

- Know each measure's type: additive, semi-additive, non-additive
- Ratios and distinct counts are **recomputed**, never summed or averaged
- Marts = small, declared-grain Gold tables for one audience, built from the star
- Reconcile marts against the fact before anyone sees a dashboard

👉 Now: **Lab 8.2**
