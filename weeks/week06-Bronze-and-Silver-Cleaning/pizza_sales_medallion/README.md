# 🍕 Pizza Shop: Bronze → Silver → Gold

Two years of orders from a (fictitious) pizza place: the 2015 data is the public
[Maven Analytics "Pizza Place Sales"](https://mavenanalytics.io/data-playground/pizza-place-sales) dataset (original in `original_data/`);
2016 is a second batch generated for this course, with a bigger menu and **messier data**.
Used in [Lab 6.1](../labs/week_06_lab_01_student.md) (Bronze) and [Lab 6.2](../labs/week_06_lab_02_student.md) (Silver).

## 📂 Files

| File | What it is |
|---|---|
| `data/orders_2015.csv`, `data/orders_2016.csv` | One row per order: `order_id, date, time` |
| `data/order_details_2015.csv`, `data/order_details_2016.csv` | One row per pizza type + size in an order: `order_details_id, order_id, pizza_id, quantity` |
| `data/pizzas.csv` | Menu: `pizza_id, pizza_type_id, size, price` |
| `data/pizza_types.csv` | Menu: `pizza_type_id, name, category, ingredients`, **as received from the shop** |
| `data/pizza_types_fixed.csv` | The same file, re-sent by the shop after a loading problem (see Lab 6.1) |
| `data/delivery_app_2016.csv` | 2016 orders from a **delivery app**: a second source with its own format (week 7) |
| [`data/data_dictionary.md`](data/data_dictionary.md) | What every column means |
| `pizza_shop_dw.py` | Demo: the full pipeline Bronze → Silver → Gold (star schema) → analysis, with charts |
| [`pizza_dw_story.md`](pizza_dw_story.md) | The business story as slides (Marp) |
| `original_data/Pizza_Sales.zip` | The original Maven dataset (2015 only) |

```
pizza_types ──< pizzas ──< order_details >── orders
  (menu)        (menu)      (transactions)    (transactions)
```

## 📋 The shop's business rules (for Silver)

Every row ends up **valid**, **rejected** (kept in a reject table with a reason) or a **duplicate** (removed, counted):
the words of [Medallion in a nutshell](../../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md).

| # | Table | Rule | Fate |
|---|---|---|---|
| 1 | orders | `date` comes as `2015-01-01` (YYYY-MM-DD) or `12/25/2015` (MM/DD/YYYY) → one valid `DATE` | fixed |
| 2 | orders | a missing (NULL) `order_id`: it can't match any order line | **rejected** → `silver.rejected_orders` |
| 3 | orders | exact duplicate orders (all fields identical) | **duplicate** |
| 4 | order_details | every record has the 4 fields; a record with **any** NULL field | **rejected** → `silver.rejected_order_details` |

Checks before Gold: ids are unique **within a batch** (they restart every year), and there are 0 orphans between orders, order lines and the menu.
Control total: 2015 revenue = **$817,860.05** (published with the original dataset).

## 💡 Business questions (Gold)

- How many orders per day? Are there peak hours?
- How many pizzas are in a typical order? Which pizzas are bestsellers?
- How much revenue per year, and is there seasonality?
- Which pizzas should leave the menu, and did the 2016 additions work?
