---
title: Pizza Shop Data Warehouse — the Story
author: Mahmoud Parsian
marp: true
theme: default
paginate: true
class: lead
---

# 🍕 Pizza Shop Data Warehouse
## From two years of raw files to business answers

The running case of weeks 6–10: Bronze and Silver (weeks 6–7), Gold (week 8), incremental loads (week 9), the story (week 10).

---

# 📖 The Business

A pizza shop with daily orders, many pizza types in up to five sizes, and **new pizzas in 2016**. The owner asks:

- 📊 Which pizzas sell best, and which should leave the menu?
- ⏰ When are the peak days and hours?
- 💰 How is revenue changing from 2015 to 2016, and did the new pizzas work?

Nobody can answer these from the raw files: they arrive in pieces, in different years, with problems.

---

# 🧩 What Arrives

| File | One row = | Kind |
|---|---|---|
| `orders_2015.csv`, `orders_2016.csv` | one order: `order_id, date, time` | transactions, one file per year (a **batch**) |
| `order_details_2015.csv`, `order_details_2016.csv` | one pizza line in an order: `order_details_id, order_id, pizza_id, quantity` | transactions |
| `pizzas.csv` | one pizza in one size, with its price | menu (reference data) |
| `pizza_types.csv` → re-sent as `pizza_types_fixed.csv` | one pizza type: name, category, ingredients | menu |
| `delivery_app_2016.csv` | one order from a delivery app, in its own format | a second source (week 7) |

```
pizza_types ──< pizzas ──< order_details >── orders
```

---

# 🚨 What Goes Wrong (Real-World Problems)

- the menu file **won't load** the first time (the shop re-sends it)
- ids **restart** in every yearly file: `order_details_id = 1` exists in 2015 **and** in 2016
- two **date formats** in the same column
- orders with **no id**, order lines with **missing fields**
- the same order sent **twice**

👉 Bronze must keep all of it, traceably. Silver must fix, reject or deduplicate every problem, and **prove** it lost nothing.

---

# 🥉🥈🥇 The Plan: Medallion

| Layer | Pizza shop | Week |
|---|---|---|
| 🟫 Bronze | every file as received (all text), with `_source_file`, `_batch_id`, `_ingested_at`; load errors recorded | 6 (Lab 6.1) |
| ⚪ Silver | typed, cleaned, deduplicated tables + reject tables; one enriched `silver.order_lines` | 6 (Lab 6.2), 7 |
| 🟡 Gold | star schema: `fact_sales` + dimensions; business tables | 8 |

Dashboards and the week 10 story **read** Gold: they are consumers, not a layer. Words as in [Medallion in a nutshell](../../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md).

---

# 📋 The Shop's Business Rules (Silver)

| # | Table | Rule | Fate of the row |
|---|---|---|---|
| 1 | orders | `date` comes as `YYYY-MM-DD` or `MM/DD/YYYY` → one real `DATE` | fixed |
| 2 | orders | NULL `order_id`: cannot match any order line | **rejected** → `silver.rejected_orders` |
| 3 | orders | exact duplicate orders (all fields identical) | **duplicate**: keep one, count the others |
| 4 | order_details | a line with **any** NULL field | **rejected** → `silver.rejected_order_details` |

Plus two checks that **must pass** before Gold (they change no row; a failure stops the pipeline):

- **keys:** an id is unique **within its batch** (`_batch_id` + id), not across batches
- **referential integrity:** every order line's `order_id` is in `orders`, every `pizza_id` is in `pizzas`, every pizza's type is in `pizza_types`

---

# ⚖️ How We Know Silver Is Right

1. **Reconcile** each table: Bronze rows = valid + rejected + duplicates (per batch).
2. **Integrity:** 0 orphans between orders, order lines and the menu.
3. **Control total:** the publisher of the 2015 data reports **$817,860.05** revenue. Silver must match it **to the cent**.

A number from **outside** the pipeline is the strongest test there is: "close" is not "correct".

---

# 🎯 What You Will Be Able to Do

- land messy files so nothing is lost and every row is traceable (Lab 6.1)
- turn business rules into Silver SQL, with reject tables and a reconciliation (Lab 6.2)
- check keys and integrity before any join that feeds a report
- validate against a control total

👉 Demo of the whole pipeline (Bronze → Silver → Gold → analysis): [`pizza_shop_dw.py`](pizza_shop_dw.py) (Marimo).
