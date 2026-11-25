import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🍕 Pizza Shop: Bronze → Silver → Gold → Answers

    The whole week 6 pipeline in one notebook (Labs 6.1 and 6.2 do the same steps, one question at a time).
    Story and rules: [`pizza_dw_story.md`](pizza_dw_story.md) · [`README.md`](README.md). Words as in
    [Medallion in a nutshell](../../week05-Medallion-Architecture-Introduction/Medallion_Architecture_in_a_Nutshell.md).

    | Layer | Tables |
    |---|---|
    | 🟫 Bronze | `bronze.orders`, `bronze.order_details`, `bronze.pizzas`, `bronze.pizza_types` (all text, `_source_file`, `_batch_id`, `_ingested_at`) |
    | ⚪ Silver | `silver.orders`, `silver.order_details`, `silver.pizzas`, `silver.pizza_types`, reject tables `silver.rejected_orders`, `silver.rejected_order_details`, and the enriched `silver.order_lines` |
    | 🟡 Gold | `gold.dim_date`, `gold.dim_pizza`, `gold.fact_sales` |
    """)
    return


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt

    con = duckdb.connect()   # in memory: nothing is written to disk
    for _schema in ("bronze", "silver", "gold"):
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {_schema}")
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟫 Bronze
    ## 1. What arrived?
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT regexp_extract(filename, '[^/]+$') AS file, size AS bytes
    FROM read_blob('data/*.csv')
    ORDER BY file
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Transactions arrive **one file per year** (a batch); the menu is reference data; `delivery_app_2016.csv` is a second source for week 7.
    `pizza_types_fixed.csv` is the menu the shop **re-sent** after the first one failed to load (step 3).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Land the two batches, with lineage

    All text, nothing fixed. `_batch_id` comes from the file name.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE bronze.orders AS
    SELECT * EXCLUDE (filename),
           regexp_extract(filename, '[^/]+$')              AS _source_file,
           regexp_extract(filename, '([0-9]{4})', 1)::INTEGER AS _batch_id,
           current_timestamp                               AS _ingested_at
    FROM read_csv('data/orders_201*.csv', all_varchar = true, filename = true, union_by_name = true);
    
    CREATE OR REPLACE TABLE bronze.order_details AS
    SELECT * EXCLUDE (filename),
           regexp_extract(filename, '[^/]+$')              AS _source_file,
           regexp_extract(filename, '([0-9]{4})', 1)::INTEGER AS _batch_id,
           current_timestamp                               AS _ingested_at
    FROM read_csv('data/order_details_201*.csv', all_varchar = true, filename = true, union_by_name = true);
    
    SELECT 'orders' AS table_name, _batch_id, COUNT(*) AS n_rows FROM bronze.orders GROUP BY ALL
    UNION ALL
    SELECT 'order_details', _batch_id, COUNT(*) FROM bronze.order_details GROUP BY ALL
    ORDER BY table_name, _batch_id
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. The menu: a file that won't load

    `pizza_types.csv` is not UTF-8: a plain load **fails**. `store_rejects = true` loads the good rows and **records** the bad one
    (never `ignore_errors`, which would drop it silently). Then the shop's corrected file is **appended** as a new file: Bronze keeps both.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE bronze.pizzas AS
    SELECT * EXCLUDE (filename), regexp_extract(filename, '[^/]+$') AS _source_file, current_timestamp AS _ingested_at
    FROM read_csv('data/pizzas.csv', all_varchar = true, filename = true);
    
    CREATE OR REPLACE TABLE bronze.pizza_types AS
    SELECT * EXCLUDE (filename), regexp_extract(filename, '[^/]+$') AS _source_file, current_timestamp AS _ingested_at
    FROM read_csv('data/pizza_types.csv', all_varchar = true, filename = true, header = true, store_rejects = true);
    
    SELECT line, column_name, error_type, left(trim(csv_line, chr(10) || chr(13)), 60) AS csv_line_start
    FROM reject_errors
    """).df()
    _df
    return


@app.cell
def _(con):
    _df = con.execute("""
    INSERT INTO bronze.pizza_types
    SELECT * EXCLUDE (filename), regexp_extract(filename, '[^/]+$'), current_timestamp
    FROM read_csv('data/pizza_types_fixed.csv', all_varchar = true, filename = true);
    
    SELECT _source_file, COUNT(*) AS n_rows FROM bronze.pizza_types GROUP BY ALL ORDER BY 1
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Profile Bronze → the Silver to-do list
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT _batch_id,
           COUNT(*)                                                     AS order_rows,
           COUNT(*) - COUNT(order_id)                                   AS null_order_id,
           COUNT(order_id)
             - COUNT(DISTINCT (order_id, date, time)) FILTER (WHERE order_id IS NOT NULL) AS duplicate_orders,
           COUNT(*) FILTER (WHERE date LIKE '____-__-__')               AS dates_yyyy_mm_dd,
           COUNT(*) FILTER (WHERE date LIKE '__/__/____')               AS dates_mm_dd_yyyy
    FROM bronze.orders
    GROUP BY _batch_id
    ORDER BY _batch_id
    """).df()
    _df
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT (SELECT COUNT(*) FROM bronze.order_details
            WHERE order_details_id IS NULL OR order_id IS NULL OR pizza_id IS NULL OR quantity IS NULL) AS lines_with_null_field,
           (SELECT COUNT(*) FROM (SELECT order_details_id FROM bronze.order_details
                                  GROUP BY 1 HAVING COUNT(DISTINCT _batch_id) > 1))                    AS line_ids_in_both_batches,
           (SELECT COUNT(*) FROM (SELECT order_id FROM bronze.orders WHERE order_id IS NOT NULL
                                  GROUP BY 1 HAVING COUNT(DISTINCT _batch_id) > 1))                    AS order_ids_in_both_batches
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The to-do list:** two date formats; NULL order ids; duplicate orders; order lines with NULL fields; and `order_details_id` restarts in 2016,
    so an order line is identified by (`_batch_id`, `order_details_id`), never by the id alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ⚪ Silver

    | # | Rule | Fate |
    |---|---|---|
    | 1 | `orders.date`: `YYYY-MM-DD` or `MM/DD/YYYY` → one `DATE` | fixed |
    | 2 | NULL `order_id` | **rejected** → `silver.rejected_orders` |
    | 3 | exact duplicate orders | **duplicate** (removed, counted) |
    | 4 | order line with any NULL field | **rejected** → `silver.rejected_order_details` |

    ## 5. Orders (rules 1–3)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.rejected_orders AS
    SELECT *, 'R2 missing order_id' AS reject_reason
    FROM bronze.orders
    WHERE order_id IS NULL;
    
    CREATE OR REPLACE TABLE silver.orders AS
    SELECT DISTINCT                                                       -- rule 3 (after parsing: rule 1)
           order_id::INTEGER AS order_id,
           CASE WHEN date LIKE '____-__-__' THEN try_strptime(date, '%Y-%m-%d')
                WHEN date LIKE '__/__/____' THEN try_strptime(date, '%m/%d/%Y')
           END::DATE          AS order_date,                              -- rule 1
           time::TIME         AS order_time,
           _batch_id
    FROM bronze.orders
    WHERE order_id IS NOT NULL;                                           -- rule 2 rows are in silver.rejected_orders
    
    SELECT _batch_id, COUNT(*) AS orders, COUNT(DISTINCT order_id) AS distinct_ids,
           COUNT(*) FILTER (WHERE order_date IS NULL) AS unparsed_dates,
           MIN(order_date) AS first_day, MAX(order_date) AS last_day
    FROM silver.orders GROUP BY ALL ORDER BY 1
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Order lines (rule 4)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.rejected_order_details AS
    SELECT *, 'R4 missing field' AS reject_reason
    FROM bronze.order_details
    WHERE order_details_id IS NULL OR order_id IS NULL OR pizza_id IS NULL OR quantity IS NULL;
    
    CREATE OR REPLACE TABLE silver.order_details AS
    SELECT DISTINCT
           order_details_id::INTEGER AS order_details_id,
           order_id::INTEGER         AS order_id,
           pizza_id,
           quantity::INTEGER         AS quantity,
           _batch_id                                                      -- part of the key: ids restart every year
    FROM bronze.order_details
    WHERE NOT (order_details_id IS NULL OR order_id IS NULL OR pizza_id IS NULL OR quantity IS NULL);
    
    SELECT _batch_id, COUNT(*) AS order_lines FROM silver.order_details GROUP BY ALL ORDER BY 1
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. The menu: Silver decides which version is true

    Bronze holds **both** menu files (34 + 35 rows). Silver takes the corrected one: with both, every type would appear twice and every join would
    **double** the order lines (Lab 6.2, Q3).
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.pizzas AS
    SELECT pizza_id, pizza_type_id, size, price::DECIMAL(6, 2) AS price
    FROM bronze.pizzas;
    
    CREATE OR REPLACE TABLE silver.pizza_types AS
    SELECT pizza_type_id, name, category, ingredients
    FROM bronze.pizza_types
    WHERE _source_file = 'pizza_types_fixed.csv';
    
    SELECT (SELECT COUNT(*) FROM silver.pizzas) AS pizzas, (SELECT COUNT(*) FROM silver.pizza_types) AS pizza_types,
           (SELECT COUNT(DISTINCT pizza_type_id) FROM silver.pizza_types) AS distinct_types
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Checks before any join: integrity (all must be 0)
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    SELECT (SELECT COUNT(*) FROM silver.order_details WHERE order_id NOT IN (SELECT order_id FROM silver.orders))           AS lines_without_order,
           (SELECT COUNT(*) FROM silver.order_details WHERE pizza_id NOT IN (SELECT pizza_id FROM silver.pizzas))            AS lines_without_pizza,
           (SELECT COUNT(*) FROM silver.orders WHERE order_id NOT IN (SELECT order_id FROM silver.order_details))            AS orders_without_lines,
           (SELECT COUNT(*) FROM silver.pizzas WHERE pizza_type_id NOT IN (SELECT pizza_type_id FROM silver.pizza_types))     AS pizzas_without_type
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An inner `JOIN` silently **drops** orphans, so this check comes **before** every join that feeds a report. All 0: the joins below lose nothing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Reconcile Bronze → Silver
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    WITH n AS (
      SELECT 'orders' AS table_name, _batch_id, COUNT(*) AS n, 'bronze' AS what FROM bronze.orders GROUP BY ALL
      UNION ALL SELECT 'orders', _batch_id, COUNT(*), 'valid'    FROM silver.orders GROUP BY ALL
      UNION ALL SELECT 'orders', _batch_id, COUNT(*), 'rejected' FROM silver.rejected_orders GROUP BY ALL
      UNION ALL SELECT 'order_details', _batch_id, COUNT(*), 'bronze'   FROM bronze.order_details GROUP BY ALL
      UNION ALL SELECT 'order_details', _batch_id, COUNT(*), 'valid'    FROM silver.order_details GROUP BY ALL
      UNION ALL SELECT 'order_details', _batch_id, COUNT(*), 'rejected' FROM silver.rejected_order_details GROUP BY ALL
    )
    SELECT table_name, _batch_id,
           SUM(n) FILTER (WHERE what = 'bronze')   AS bronze_rows,
           SUM(n) FILTER (WHERE what = 'valid')    AS valid,
           SUM(n) FILTER (WHERE what = 'rejected') AS rejected,
           SUM(n) FILTER (WHERE what = 'bronze') - SUM(n) FILTER (WHERE what = 'valid')
             - SUM(n) FILTER (WHERE what = 'rejected') AS duplicates
    FROM n
    GROUP BY ALL
    ORDER BY table_name DESC, _batch_id
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. The enriched table and the control total
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE silver.order_lines AS
    SELECT d._batch_id, d.order_details_id, d.order_id, o.order_date, o.order_time,
           d.pizza_id, p.size, t.name AS pizza_name, t.category,
           d.quantity, p.price, d.quantity * p.price AS line_revenue
    FROM silver.order_details AS d
    JOIN silver.orders        AS o USING (order_id)
    JOIN silver.pizzas        AS p USING (pizza_id)
    JOIN silver.pizza_types   AS t USING (pizza_type_id);
    
    SELECT _batch_id, COUNT(*) AS order_lines, SUM(line_revenue) AS revenue
    FROM silver.order_lines GROUP BY ALL ORDER BY 1
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Control total:** the publisher of the 2015 data reports **$817,860.05**. Silver matches it **to the cent**: the strongest check there is,
    because the number comes from **outside** the pipeline.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🟡 Gold: a Star Schema

    Grain of `gold.fact_sales`: **one order line** (one pizza in one size in one order). Built only from Silver.
    """)
    return


@app.cell
def _(con):
    _df = con.execute("""
    CREATE OR REPLACE TABLE gold.dim_date AS
    SELECT DISTINCT
           strftime(order_date, '%Y%m%d')::INTEGER AS date_key,
           order_date                              AS full_date,
           year(order_date)                        AS year,
           month(order_date)                       AS month,
           monthname(order_date)                   AS month_name,
           dayname(order_date)                     AS day_name,
           quarter(order_date)                     AS quarter
    FROM silver.orders;
    
    CREATE OR REPLACE TABLE gold.dim_pizza AS
    SELECT p.pizza_id, p.pizza_type_id, t.name AS pizza_name, t.category, p.size, p.price
    FROM silver.pizzas AS p
    JOIN silver.pizza_types AS t USING (pizza_type_id);
    
    CREATE OR REPLACE TABLE gold.fact_sales AS
    SELECT d._batch_id, d.order_details_id, d.order_id,
           strftime(o.order_date, '%Y%m%d')::INTEGER AS date_key,
           o.order_time,
           d.pizza_id,
           d.quantity,
           p.price                                   AS unit_price,
           d.quantity * p.price                      AS sales_amount
    FROM silver.order_details AS d
    JOIN silver.orders        AS o USING (order_id)
    JOIN gold.dim_pizza       AS p USING (pizza_id);
    
    SELECT (SELECT COUNT(*) FROM gold.dim_date)            AS dates,
           (SELECT COUNT(*) FROM gold.dim_pizza)           AS pizzas,
           (SELECT COUNT(*) FROM gold.fact_sales)          AS fact_rows,
           (SELECT SUM(sales_amount) FROM gold.fact_sales) AS fact_revenue,
           (SELECT SUM(line_revenue) FROM silver.order_lines) AS silver_revenue
    """).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📊 Answers for the Owner
    ## Q1. The year in numbers
    """)
    return


@app.cell
def _(con):
    kpis = con.execute("""
    SELECT f._batch_id                         AS year,
           COUNT(DISTINCT f.order_id)          AS orders,
           SUM(f.quantity)                     AS pizzas_sold,
           SUM(f.sales_amount)                 AS revenue,
           ROUND(SUM(f.sales_amount) / COUNT(DISTINCT f.order_id), 2) AS avg_order_value
    FROM gold.fact_sales AS f
    GROUP BY ALL ORDER BY 1
    """).df()
    kpis
    return (kpis,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** 2016 revenue is **$1,417,513.75**, **+73.3%** on 2015 ($817,860.05). Orders grew only **+15.9%** (21,350 → 24,750),
    pizzas sold **+72.8%** (49,574 → 85,679): the growth comes from **bigger orders** (average $38.31 → $57.27), not from many more customers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q2. Revenue by month
    """)
    return


@app.cell
def _(con):
    monthly = con.execute("""
    SELECT d.year, d.month, SUM(f.sales_amount) AS revenue
    FROM gold.fact_sales AS f
    JOIN gold.dim_date   AS d USING (date_key)
    GROUP BY ALL ORDER BY 1, 2
    """).df()
    monthly
    return (monthly,)


@app.cell
def _(monthly, plt):
    plt.figure(figsize=(10, 4))
    for _year in sorted(monthly["year"].unique()):
        _m = monthly[monthly["year"] == _year]
        plt.plot(_m["month"], _m["revenue"], marker="o", label=str(_year))
    plt.xticks(range(1, 13))
    plt.xlabel("Month")
    plt.ylabel("Revenue (US $)")
    plt.title("Revenue by Month")
    plt.legend()
    plt.grid()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** no strong season. 2015 stays between $64,028 (October) and $72,558 (July); 2016 between $105,874 (October) and
    $124,691 (May). The big change is the **level**: every 2016 month is far above every 2015 month.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q3. Peak hours
    """)
    return


@app.cell
def _(con):
    hourly = con.execute("""
    SELECT hour(order_time) AS hour, COUNT(DISTINCT (_batch_id, order_id)) AS orders
    FROM gold.fact_sales
    GROUP BY ALL ORDER BY 1
    """).df()
    hourly
    return (hourly,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** two peaks, **lunch** (12:00–13:59: 10,793 orders) and **dinner** (17:00–18:59: 10,032); almost nothing before 11:00 or after 22:00.
    Staff and ovens should follow these two peaks.
    """)
    return


@app.cell
def _(hourly, plt):
    plt.figure(figsize=(9, 4))
    plt.bar(hourly["hour"], hourly["orders"])
    plt.xlabel("Hour of the day")
    plt.ylabel("Orders (2015 + 2016)")
    plt.title("Orders by Hour")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q4. Best sellers (both years)
    """)
    return


@app.cell
def _(con):
    top10 = con.execute("""
    SELECT p.pizza_name, p.category, SUM(f.quantity) AS pizzas_sold, SUM(f.sales_amount) AS revenue
    FROM gold.fact_sales AS f
    JOIN gold.dim_pizza  AS p USING (pizza_id)
    GROUP BY ALL ORDER BY revenue DESC LIMIT 10
    """).df()
    top10
    return (top10,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** **4 of the top 5** are chicken pizzas (The Barbecue Chicken Pizza first, $110,272.25), although the Chicken category is the
    smallest by revenue overall (Q5): a few chicken pizzas carry the category.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q5. Category mix
    """)
    return


@app.cell
def _(con):
    categories = con.execute("""
    SELECT p.category,
           SUM(f.sales_amount) AS revenue,
           ROUND(100 * SUM(f.sales_amount) / SUM(SUM(f.sales_amount)) OVER (), 1) AS pct_of_revenue
    FROM gold.fact_sales AS f
    JOIN gold.dim_pizza  AS p USING (pizza_id)
    GROUP BY ALL ORDER BY revenue DESC
    """).df()
    categories
    return (categories,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** the four categories are close: Classic 26.7%, Supreme 25.7%, Veggie 24.5%, Chicken 23.1%. No category to drop.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q6. Did the three new 2016 pizzas work?
    """)
    return


@app.cell
def _(con):
    new_pizzas = con.execute("""
    SELECT p.pizza_name, SUM(f.quantity) AS pizzas_sold, SUM(f.sales_amount) AS revenue,
           ROUND(100 * SUM(f.sales_amount) / (SELECT SUM(sales_amount) FROM gold.fact_sales WHERE _batch_id = 2016), 1) AS pct_of_2016_revenue
    FROM gold.fact_sales AS f
    JOIN gold.dim_pizza  AS p USING (pizza_id)
    WHERE f._batch_id = 2016
      AND p.pizza_type_id NOT IN (SELECT DISTINCT p2.pizza_type_id
                                  FROM gold.fact_sales f2 JOIN gold.dim_pizza p2 USING (pizza_id)
                                  WHERE f2._batch_id = 2015)
    GROUP BY ALL ORDER BY revenue DESC
    """).df()
    new_pizzas
    return (new_pizzas,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** together the three new pizzas brought **1.3%** of 2016 revenue (Margherita 0.5%, Deep Dish 0.4%, Detroit Style 0.4%):
    a weak launch. Candidates to promote, or to drop.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✅ Summary
    | Step | Result |
|---|---|
| Bronze | orders 21,389 + 24,991 · order lines 48,662 + 58,859 · menu 34 + 35 rows, 1 line recorded in `reject_errors` |
| Silver | orders 21,350 + 24,750 (rejected 15 + 75, duplicates 24 + 166) · order lines 48,632 + 58,820 (rejected 30 + 39) · 0 orphans |
| Proof | every table reconciles per batch · 2015 revenue = **$817,860.05**, the published control total |
| Gold | `fact_sales` 107,452 rows (one order line each), revenue = Silver's to the cent; `dim_date` 724 days (7 days without orders) |
| Answers | 2016: +73% revenue from bigger orders; lunch and dinner peaks; chicken pizzas lead; categories balanced; new pizzas 1.3% |

Every row of Bronze is accounted for, every rule is one SQL step, and every answer comes from Gold.
    """)
    return


if __name__ == "__main__":
    app.run()
