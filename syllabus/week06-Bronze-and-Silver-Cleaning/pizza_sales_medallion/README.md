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

1. `orders.date` comes in two formats, `2015-01-01` (YYYY-MM-DD) and `12/25/2015` (MM/DD/YYYY); convert both to one valid date.
2. An order with a missing (NULL) `order_id` is dropped: it can't match any order line.
3. Exact duplicate orders (all fields identical) are dropped.
4. In `order_details`: every record must have exactly 4 fields, and a record with **any** NULL field is dropped.

## 💡 Business questions (Gold)

- How many orders per day? Are there peak hours?
- How many pizzas are in a typical order? Which pizzas are bestsellers?
- How much revenue per year, and is there seasonality?
- Which pizzas should leave the menu, and did the 2016 additions work?
