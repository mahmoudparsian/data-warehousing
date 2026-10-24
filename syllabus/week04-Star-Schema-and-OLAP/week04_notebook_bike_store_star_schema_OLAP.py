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
    # Week 3 — Classic Data Warehousing with Bike Store
    ## Star Schema + OLAP Queries

    ### Notebook Overview
    This notebook turns the **Bike Store** dataset into a simple classic data warehouse lesson.

    What this notebook does:
    - explains the business problem
    - creates a **star schema**
    - loads a small Bike Store warehouse into DuckDB
    - runs **OLAP-style queries**
    - connects SQL results to business insight

    ### Business Context
    Assume we are analysts for a bike retailer. The business wants to answer questions such as:
    - Which products sell best?
    - Which stores generate the most revenue?
    - How does sales performance change over time?
    - Which brands and categories drive the business?

    ### DW Concepts in this Notebook
    - **Fact table**: sales facts at the order-line grain
    - **Dimension tables**: date, customer, store, product, staff
    - **OLAP queries**: roll-up, drill-down, slice, dice, ranking
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Setup
    We use DuckDB as the analytical engine.

    Why DuckDB here?
    - lightweight and local
    - perfect for teaching
    - fast enough for warehouse-style queries
    """)
    return


@app.cell
def _():
    import duckdb as _duckdb
    _duckdb.execute("ATTACH IF NOT EXISTS 'week04_bikestore_dw.duckdb' AS week04_bikestore_dw; USE week04_bikestore_dw").fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Create a Small Bike Store Star Schema

    ### Grain
    The fact table grain is:

    > **one row per order line item**

    This means each row represents one product sold on one order line.

    Why this grain matters:
    - detailed enough for product analysis
    - flexible enough for time, store, and customer analysis
    - realistic for classic DW teaching
    """)
    return


@app.cell
def _():
    # (DROP TABLE IF EXISTS … removed: every CREATE is CREATE OR REPLACE)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE dim_date (
        date_id INTEGER,
        full_date DATE,
        year INTEGER,
        quarter INTEGER,
        month INTEGER,
        month_name VARCHAR
    )
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE dim_customer (
        customer_id INTEGER,
        customer_name VARCHAR,
        city VARCHAR,
        state VARCHAR
    )
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE dim_store (
        store_id INTEGER,
        store_name VARCHAR,
        city VARCHAR,
        state VARCHAR
    )
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE dim_product (
        product_id INTEGER,
        product_name VARCHAR,
        brand_name VARCHAR,
        category_name VARCHAR,
        model_year INTEGER,
        list_price DOUBLE
    )
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE dim_staff (
        staff_id INTEGER,
        staff_name VARCHAR
    )
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql("""
    CREATE OR REPLACE TABLE fact_sales (
        order_id INTEGER,
        line_no INTEGER,
        date_id INTEGER,
        customer_id INTEGER,
        store_id INTEGER,
        product_id INTEGER,
        staff_id INTEGER,
        quantity INTEGER,
        unit_price DOUBLE,
        discount DOUBLE,
        revenue DOUBLE
    )
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Load Sample Dimension Data

    This sample data is intentionally small enough for teaching:
    - easy to inspect
    - easy to explain
    - enough to support realistic DW questions
    """)
    return


@app.cell
def _(dim_date, mo):
    _df = mo.sql("""
    INSERT INTO dim_date VALUES
    (20220115, '2022-01-15', 2022, 1, 1, 'Jan'),
    (20220210, '2022-02-10', 2022, 1, 2, 'Feb'),
    (20220305, '2022-03-05', 2022, 1, 3, 'Mar'),
    (20220420, '2022-04-20', 2022, 2, 4, 'Apr'),
    (20230112, '2023-01-12', 2023, 1, 1, 'Jan'),
    (20230218, '2023-02-18', 2023, 1, 2, 'Feb'),
    (20230322, '2023-03-22', 2023, 1, 3, 'Mar'),
    (20230425, '2023-04-25', 2023, 2, 4, 'Apr')
    """)
    return


@app.cell
def _(dim_customer, mo):
    _df = mo.sql("""
    INSERT INTO dim_customer VALUES
    (1, 'Alice Johnson', 'San Jose', 'CA'),
    (2, 'Bob Smith', 'Sunnyvale', 'CA'),
    (3, 'Carla Gomez', 'Palo Alto', 'CA'),
    (4, 'David Lee', 'Fremont', 'CA'),
    (5, 'Emma Brown', 'Mountain View', 'CA')
    """)
    return


@app.cell
def _(dim_store, mo):
    _df = mo.sql("""
    INSERT INTO dim_store VALUES
    (1, 'Downtown Bikes', 'San Jose', 'CA'),
    (2, 'Valley Bikes', 'Sunnyvale', 'CA'),
    (3, 'Peninsula Bikes', 'Palo Alto', 'CA')
    """)
    return


@app.cell
def _(dim_product, mo):
    _df = mo.sql("""
    INSERT INTO dim_product VALUES
    (101, 'Road-100', 'Trek', 'Road Bikes', 2022, 1200),
    (102, 'Road-200', 'Giant', 'Road Bikes', 2023, 1800),
    (103, 'Mountain-100', 'Trek', 'Mountain Bikes', 2022, 1500),
    (104, 'Helmet Pro', 'Bell', 'Accessories', 2023, 80),
    (105, 'Bike Pump', 'Park Tool', 'Accessories', 2023, 45),
    (106, 'Hybrid-300', 'Specialized', 'Hybrid Bikes', 2023, 950)
    """)
    return


@app.cell
def _(dim_staff, mo):
    _df = mo.sql("""
    INSERT INTO dim_staff VALUES
    (1, 'Mia Chen'),
    (2, 'Noah Patel'),
    (3, 'Olivia Garcia')
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Load Sample Fact Data

    The fact table contains measurable business activity:
    - quantity
    - unit price
    - discount
    - revenue

    Revenue is precomputed here for simplicity:
    > `revenue = quantity * unit_price * (1 - discount)`
    """)
    return


@app.cell
def _(fact_sales, mo):
    _df = mo.sql("""
    INSERT INTO fact_sales VALUES
    (1001, 1, 20220115, 1, 1, 101, 1, 1, 1200, 0.05, 1140),
    (1001, 2, 20220115, 1, 1, 104, 1, 2, 80, 0.00, 160),
    (1002, 1, 20220210, 2, 2, 103, 2, 1, 1500, 0.10, 1350),
    (1003, 1, 20220305, 3, 3, 102, 3, 1, 1800, 0.00, 1800),
    (1003, 2, 20220305, 3, 3, 105, 3, 1, 45, 0.00, 45),
    (1004, 1, 20220420, 4, 1, 106, 1, 2, 950, 0.05, 1805),
    (1005, 1, 20230112, 5, 2, 101, 2, 1, 1200, 0.00, 1200),
    (1005, 2, 20230112, 5, 2, 104, 2, 1, 80, 0.00, 80),
    (1006, 1, 20230218, 2, 1, 102, 1, 1, 1800, 0.15, 1530),
    (1007, 1, 20230322, 1, 3, 103, 3, 1, 1500, 0.00, 1500),
    (1008, 1, 20230425, 4, 2, 106, 2, 1, 950, 0.00, 950),
    (1008, 2, 20230425, 4, 2, 105, 2, 2, 45, 0.00, 90)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) Inspect the Star Schema

    This step is pedagogically important:
    - students should see the warehouse tables
    - students should distinguish fact vs dimension
    - students should connect schema design to later SQL
    """)
    return


@app.cell
def _(dim_product, mo):
    _df = mo.sql("""
    SELECT * FROM dim_product
    """)
    return


@app.cell
def _(dim_store, mo):
    _df = mo.sql("""
    SELECT * FROM dim_store
    """)
    return


@app.cell
def _(fact_sales, mo):
    _df = mo.sql("""
    SELECT * FROM fact_sales
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) First Warehouse Query — Total Revenue

    ### Business Question
    How much revenue does the business generate overall?

    ### Why this matters
    This is the simplest KPI in the warehouse:
    - baseline performance
    - sanity check
    - starting point for more detailed analysis
    """)
    return


@app.cell
def _(fact_sales, mo):
    _res = mo.sql(f"""SELECT SUM(revenue) AS total_revenue FROM fact_sales""")
    _res
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7) Sales by Store

    ### Business Question
    Which stores generate the most revenue?

    ### DW Idea
    This query joins:
    - fact table = measurable events
    - store dimension = context

    ### Business Insight
    This helps:
    - compare store performance
    - identify top-performing locations
    - support resource allocation
    """)
    return


@app.cell
def _(dim_store, fact_sales, mo):
    res = mo.sql(f"""
    SELECT
        s.store_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_store s
      ON f.store_id = s.store_id
    GROUP BY s.store_name
    ORDER BY total_revenue DESC
    """)
    return (res,)


@app.cell
def _(res):
    store_df = res
    store_df
    return (store_df,)


@app.cell
def _(store_df):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))
    plt.bar(store_df["store_name"], store_df["total_revenue"])
    plt.title("Revenue by Store")
    plt.xlabel("Store")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8) Sales by Product Category

    ### Business Question
    Which categories drive the business?

    ### Why this matters
    Category analysis supports:
    - product strategy
    - inventory planning
    - merchandising decisions
    """)
    return


@app.cell
def _(dim_product, fact_sales, mo):
    res_2 = mo.sql(f"""
    SELECT
        p.category_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_product p
      ON f.product_id = p.product_id
    GROUP BY p.category_name
    ORDER BY total_revenue DESC
    """)
    return (res_2,)


@app.cell
def _(res_2):
    cat_df = res_2
    cat_df
    return (cat_df,)


@app.cell
def _(cat_df, plt):
    plt.figure(figsize=(8, 4))
    plt.bar(cat_df["category_name"], cat_df["total_revenue"])
    plt.title("Revenue by Product Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9) Sales by Brand

    ### Business Question
    Which brands contribute most to total revenue?

    ### Business Insight
    Brand performance can influence:
    - supplier relationships
    - promotion decisions
    - assortment planning
    """)
    return


@app.cell
def _(dim_product, fact_sales, mo):
    res_3 = mo.sql(f"""
    SELECT
        p.brand_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_product p
      ON f.product_id = p.product_id
    GROUP BY p.brand_name
    ORDER BY total_revenue DESC
    """)
    return (res_3,)


@app.cell
def _(res_3):
    brand_df = res_3
    brand_df
    return (brand_df,)


@app.cell
def _(brand_df, plt):
    plt.figure(figsize=(8, 4))
    plt.bar(brand_df["brand_name"], brand_df["total_revenue"])
    plt.title("Revenue by Brand")
    plt.xlabel("Brand")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10) Time Analysis — Revenue by Year and Month

    ### Business Question
    How does revenue change over time?

    ### DW Idea
    Time is almost always a conformed dimension in warehousing.

    ### Business Insight
    Time analysis supports:
    - forecasting
    - seasonality detection
    - planning and budgeting
    """)
    return


@app.cell
def _(dim_date, fact_sales, mo):
    res_4 = mo.sql(f"""
    SELECT
        d.year,
        d.month,
        d.month_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    GROUP BY d.year, d.month, d.month_name
    ORDER BY d.year, d.month
    """)
    return (res_4,)


@app.cell
def _(res_4):
    time_df = res_4
    time_df
    return (time_df,)


@app.cell
def _(plt, time_df):
    time_df["period"] = time_df["year"].astype(str) + "-" + time_df["month_name"]

    plt.figure(figsize=(9, 4))
    plt.plot(time_df["period"], time_df["total_revenue"], marker="o")
    plt.title("Revenue by Month")
    plt.xlabel("Period")
    plt.ylabel("Revenue")
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11) Drill-Down Example

    ### OLAP Concept
    A warehouse supports drill-down:
    - from higher-level summary
    - to more detailed views
    - for investigation

    ### Business Example
    Start with revenue by year, then drill down to month.
    """)
    return


@app.cell
def _(dim_date, fact_sales, mo):
    res_5 = mo.sql(f"""
    SELECT
        d.year,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    GROUP BY d.year
    ORDER BY d.year
    """)
    return (res_5,)


@app.cell
def _(res_5):
    year_df = res_5
    year_df
    return (year_df,)


@app.cell
def _(plt, year_df):
    plt.figure(figsize=(6, 4))
    plt.bar(year_df["year"].astype(str), year_df["total_revenue"])
    plt.title("Revenue by Year")
    plt.xlabel("Year")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12) Slice Example

    ### OLAP Concept
    Slice means fixing one dimension value.

    ### Business Question
    What are sales for only the California bike business segment represented here by store locations?

    ### Teaching Note
    In this dataset, all stores are in CA, so the point is conceptual:
    students should understand the SQL pattern.
    """)
    return


@app.cell
def _(dim_store, fact_sales, mo):
    res_6 = mo.sql(f"""
    SELECT
        s.store_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_store s
      ON f.store_id = s.store_id
    WHERE s.state = 'CA'
    GROUP BY s.store_name
    ORDER BY total_revenue DESC
    """)
    return (res_6,)


@app.cell
def _(res_6):
    res_6
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13) Dice Example

    ### OLAP Concept
    Dice means filtering across multiple dimensions.

    ### Business Question
    How did Accessories perform in 2023?

    ### Business Insight
    This is closer to real management questioning:
    - a category
    - over a time period
    - for targeted decision-making
    """)
    return


@app.cell
def _(dim_date, dim_product, fact_sales, mo):
    res_7 = mo.sql(f"""
    SELECT
        d.year,
        p.category_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_date d
      ON f.date_id = d.date_id
    JOIN dim_product p
      ON f.product_id = p.product_id
    WHERE d.year = 2023
      AND p.category_name = 'Accessories'
    GROUP BY d.year, p.category_name
    """)
    return (res_7,)


@app.cell
def _(res_7):
    res_7
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14) Customer Analysis

    ### Business Question
    Which customers generate the most revenue?

    ### Business Insight
    Customer-level analysis supports:
    - loyalty programs
    - VIP identification
    - retention strategy
    """)
    return


@app.cell
def _(dim_customer, fact_sales, mo):
    res_8 = mo.sql(f"""
    SELECT
        c.customer_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_customer c
      ON f.customer_id = c.customer_id
    GROUP BY c.customer_name
    ORDER BY total_revenue DESC
    """)
    return (res_8,)


@app.cell
def _(res_8):
    cust_df = res_8
    cust_df
    return (cust_df,)


@app.cell
def _(cust_df, plt):
    plt.figure(figsize=(9, 4))
    plt.bar(cust_df["customer_name"], cust_df["total_revenue"])
    plt.title("Revenue by Customer")
    plt.xlabel("Customer")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15) Top Products per Store
    This query bridges Week 2 and Week 3:

    - Week 2 skill: window functions
    - Week 3 skill: fact + dimensions
    - Combined result: ranked warehouse analytics
    """)
    return


@app.cell
def _(dim_product, dim_store, fact_sales, mo):
    res_9 = mo.sql(f"""
    SELECT *
    FROM (
        SELECT
            s.store_name,
            p.product_name,
            SUM(f.revenue) AS revenue,
            ROW_NUMBER() OVER (
                PARTITION BY s.store_name
                ORDER BY SUM(f.revenue) DESC
            ) AS rn
        FROM fact_sales f
        JOIN dim_store s
          ON f.store_id = s.store_id
        JOIN dim_product p
          ON f.product_id = p.product_id
        GROUP BY s.store_name, p.product_name
    ) t
    WHERE rn <= 2
    ORDER BY store_name, rn
    """)
    return (res_9,)


@app.cell
def _(res_9):
    top_prod_df = res_9
    top_prod_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 16) Staff Performance

    ### Business Question
    Which staff members are associated with the most revenue?

    ### Business Insight
    This kind of query can support:
    - performance reviews
    - incentive programs
    - staffing decisions
    """)
    return


@app.cell
def _(dim_staff, fact_sales, mo):
    res_10 = mo.sql(f"""
    SELECT
        st.staff_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_staff st
      ON f.staff_id = st.staff_id
    GROUP BY st.staff_name
    ORDER BY total_revenue DESC
    """)
    return (res_10,)


@app.cell
def _(res_10):
    staff_df = res_10
    staff_df
    return (staff_df,)


@app.cell
def _(plt, staff_df):
    plt.figure(figsize=(7, 4))
    plt.bar(staff_df["staff_name"], staff_df["total_revenue"])
    plt.title("Revenue by Staff")
    plt.xlabel("Staff")
    plt.ylabel("Revenue")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 17) Average Order-Line Revenue by Category

    ### Business Question
    What is the average revenue contribution per order line by category?

    ### Business Insight
    This helps compare:
    - big-ticket categories
    - accessory categories
    - per-line profitability characteristics
    """)
    return


@app.cell
def _(dim_product, fact_sales, mo):
    res_11 = mo.sql(f"""
    SELECT
        p.category_name,
        AVG(f.revenue) AS avg_line_revenue
    FROM fact_sales f
    JOIN dim_product p
      ON f.product_id = p.product_id
    GROUP BY p.category_name
    ORDER BY avg_line_revenue DESC
    """)
    return (res_11,)


@app.cell
def _(res_11):
    avg_cat_df = res_11
    avg_cat_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 18) Revenue by Customer State and Store

    ### Business Question
    How do customer geography and store geography interact?

    ### Teaching Goal
    Even with a small dataset, this shows multi-dimensional thinking:
    - customer dimension
    - store dimension
    - fact table in the middle
    """)
    return


@app.cell
def _(dim_customer, dim_store, fact_sales, mo):
    res_12 = mo.sql(f"""
    SELECT
        c.state AS customer_state,
        s.store_name,
        SUM(f.revenue) AS total_revenue
    FROM fact_sales f
    JOIN dim_customer c
      ON f.customer_id = c.customer_id
    JOIN dim_store s
      ON f.store_id = s.store_id
    GROUP BY c.state, s.store_name
    ORDER BY total_revenue DESC
    """)
    return (res_12,)


@app.cell
def _(res_12):
    res_12
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 19) OLAP Tutorial Summary

    ### Core OLAP operations seen here
    - roll-up: month → year
    - drill-down: year → month
    - slice: one state
    - dice: one year + one category

    ### Business Value
    OLAP helps decision-makers move across levels of abstraction quickly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 20) Final Conceptual Summary

    What students should now understand:
    - a fact table stores measurable business events
    - dimensions provide context for analysis
    - a star schema makes analytical SQL simpler

    Why this matters:
    - easier reporting
    - faster querying
    - better business decisions
    """)
    return


if __name__ == "__main__":
    app.run()
