---
marp: true
theme: default
paginate: true
title: Week 8 — Session 2 — KPIs That Add Up, and Data Marts
---

# Week 8 — Session 2
## KPIs That Add Up (and Those That Don't) · Data Marts

Examples use the online-sales star from week 4 (`week04…/OLAP/OLAP_by_DuckDB/csv/`, 1M sales lines); every query runs.
Lab 8.2 applies the same ideas to the pizza shop.

```sql
CREATE OR REPLACE VIEW sales    AS SELECT * FROM read_csv('../week04-Star-Schema-and-OLAP/OLAP/OLAP_by_DuckDB/csv/sales.csv');
CREATE OR REPLACE VIEW dates    AS SELECT * FROM read_csv('../week04-Star-Schema-and-OLAP/OLAP/OLAP_by_DuckDB/csv/dates.csv');
CREATE OR REPLACE VIEW products AS SELECT * FROM read_csv('../week04-Star-Schema-and-OLAP/OLAP/OLAP_by_DuckDB/csv/products.csv');
SELECT COUNT(*) AS sales_lines, MIN(date_key) AS first_day, MAX(date_key) AS last_day FROM sales;
```

<!-- RESULT -->

| sales_lines | first_day | last_day |
|------------:|----------:|---------:|
|     1000000 |  20230101 | 20251230 |

*(1 row)*

<!-- /RESULT -->

---

# ➕ Three Kinds of Measures

| Kind | Can you SUM it… | Examples |
|---|---|---|
| **Additive** | across **all** dimensions | revenue, quantity, discount amount |
| **Semi-additive** | across some, **not over time** | account balance, inventory on hand |
| **Non-additive** | never: recompute from parts | prices, ratios, averages, percentages, **distinct counts** |

👉 Store additive **parts** in the fact table; compute ratios **at query time** from summed parts

---

# ⏳ Semi-Additive: Don't Sum Over Time

```sql
CREATE OR REPLACE TABLE balances AS SELECT * FROM (VALUES
    ('A', DATE '2024-01-31', 100.00), ('A', DATE '2024-02-29', 120.00), ('A', DATE '2024-03-31', 90.00),
    ('B', DATE '2024-01-31',  50.00), ('B', DATE '2024-02-29',  50.00), ('B', DATE '2024-03-31', 70.00)
) t(account, month_end, balance);

SELECT 'SUM over accounts, one month (Mar)' AS question, SUM(balance) AS answer FROM balances WHERE month_end = DATE '2024-03-31'
UNION ALL
SELECT 'SUM over the quarter (wrong)',  SUM(balance) FROM balances
UNION ALL
SELECT 'quarter-end balance (right)',   SUM(balance) FROM balances WHERE month_end = (SELECT MAX(month_end) FROM balances)
UNION ALL
SELECT 'average monthly total balance', SUM(balance) / COUNT(DISTINCT month_end) FROM balances;
```

<!-- RESULT -->

| question                           | answer |
|------------------------------------|-------:|
| SUM over accounts, one month (Mar) |  160.0 |
| SUM over the quarter (wrong)       |  480.0 |
| quarter-end balance (right)        |  160.0 |
| average monthly total balance      |  160.0 |

*(4 rows)*

<!-- /RESULT -->

The bank never held $480: summing balances over time counts the same money three times. Over time, take the **last** value or the **average**.

---

# ❌ Distinct Counts Don't Add Up

```sql
WITH m AS (SELECT d.month_of_year, COUNT(DISTINCT s.customer_key) AS n      -- customers per month, 2024
           FROM sales s JOIN dates d USING (date_key)
           WHERE d.year = 2024 GROUP BY 1)
SELECT (SELECT SUM(n) FROM m) AS monthly_customers_summed,
       (SELECT COUNT(DISTINCT s.customer_key)
        FROM sales s JOIN dates d USING (date_key) WHERE d.year = 2024) AS customers_in_2024;
```

<!-- RESULT -->

| monthly_customers_summed | customers_in_2024 |
|-------------------------:|------------------:|
|                    50876 |              5000 |

*(1 row)*

<!-- /RESULT -->

👉 50,876 vs 5,000: most customers buy in many months, so "monthly customers, summed" counts each of them about **10×**.

---

# ❌ Average of What?

| Question | Wrong (looks fine) | Right |
|---|---|---|
| average order value | `AVG(line_amount)` (= average **line**) | `SUM(revenue) / COUNT(DISTINCT order_id)` |
| average price paid | `AVG(unit_price)` (every line counts once) | `SUM(revenue) / SUM(quantity)` (weighted by units) |
| average across stores | `AVG(store_average)` | `SUM(revenue) / SUM(lines)` over all stores |
| revenue per customer | `AVG(total_amount)` (= average **line**) | `SUM(total_amount) / COUNT(DISTINCT customer_key)` |

```sql
SELECT ROUND(AVG(s.total_amount), 2)                                      AS avg_line_amount,
       ROUND(SUM(s.total_amount) / COUNT(DISTINCT s.customer_key), 2)     AS revenue_per_customer,
       ROUND(AVG(s.unit_price), 2)                                        AS avg_unit_price_per_line,
       ROUND(SUM(s.total_amount) / SUM(s.quantity), 2)                    AS avg_price_per_unit
FROM sales s JOIN dates d USING (date_key) WHERE d.year = 2024;
```

<!-- RESULT -->

| avg_line_amount | revenue_per_customer | avg_unit_price_per_line | avg_price_per_unit |
|----------------:|---------------------:|------------------------:|-------------------:|
|          235.49 |             23553.13 |                  164.34 |              164.2 |

*(1 row)*

<!-- /RESULT -->

Same 2024 sales, two "averages": **$235.49** per line vs **$23,553.13** per customer (100× apart). The price averages differ less ($164.34 vs $164.20)
because quantities are small, but only the unit-weighted one is right.
👉 Always ask: **average per what?** (per line, per order, per unit, per customer, per day)

---

# 🧮 The Safe Pattern

```sql no-run
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

```sql no-run
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
SELECT d.year, p.product_name, ROUND(SUM(s.total_amount), 2) AS revenue,
       ROUND(100.0 * SUM(s.total_amount)
             / SUM(SUM(s.total_amount)) OVER (PARTITION BY d.year), 2) AS pct_of_year,
       RANK() OVER (PARTITION BY d.year ORDER BY SUM(s.total_amount) DESC) AS revenue_rank
FROM sales s JOIN dates d USING (date_key) JOIN products p USING (product_key)
GROUP BY d.year, p.product_name      -- explicit GROUP BY (not GROUP BY ALL) with windows over aggregates
QUALIFY revenue_rank <= 3
ORDER BY d.year, revenue_rank;
```

<!-- RESULT -->

| year | product_name |     revenue | pct_of_year | revenue_rank |
|-----:|--------------|------------:|------------:|-------------:|
| 2023 | Product_0001 | 14740346.51 |       20.73 |            1 |
| 2023 | Product_0011 |  8384346.89 |       11.79 |            2 |
| 2023 | Product_0002 |  8331109.65 |       11.72 |            3 |
| 2024 | Product_0001 | 24590028.58 |       20.88 |            1 |
| 2024 | Product_0002 | 13885472.99 |       11.79 |            2 |
| 2024 | Product_0011 | 13872015.53 |       11.78 |            3 |
| 2025 | Product_0001 |  9831644.45 |        20.9 |            1 |
| 2025 | Product_0002 |  5542341.61 |       11.78 |            2 |
| 2025 | Product_0011 |  5471665.12 |       11.63 |            3 |

*(9 rows)*

<!-- /RESULT -->

👉 `SUM(SUM(x)) OVER (…)`: the inner SUM is the GROUP BY aggregate, the outer is the window. Product_0001 alone is about 21% of every year.

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
