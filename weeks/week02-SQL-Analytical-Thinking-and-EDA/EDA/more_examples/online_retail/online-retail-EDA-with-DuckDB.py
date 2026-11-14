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
    # Online Retail EDA — Pure DuckDB Edition

    A flagship exploratory-data-analysis notebook that does **everything in SQL**
    via [DuckDB](https://duckdb.org/).  Pandas is used *only* to hand data to Matplotlib for plotting.

    ## What makes this notebook different

    | Concern | Approach |
    |---|---|
    | **Data loading** | DuckDB's `spatial` extension reads the `.xlsx` file directly — no `pd.read_excel` |
    | **Data cleaning** | SQL `CREATE TABLE … AS SELECT` with `COALESCE`, `CASE`, and `WHERE` |
    | **Aggregation & analytics** | Window functions, `DATE_TRUNC`, `DATE_PART`, CTEs |
    | **Visualization** | Matplotlib on small result-sets returned by `.df()` |

    ## Dataset

    **UCI Online Retail Dataset** (`online_retail.xlsx`)
    ~542 K transaction lines from a UK-based online retailer, Dec 2010 – Dec 2011.

    ```
    online_retail (main) % xlsx2csv online_retail.xlsx | column -t -s, | head

    InvoiceNo  StockCode     Description                             Quantity                  InvoiceDate         UnitPrice       CustomerID      Country
    536365     85123A        WHITE HANGING HEART T-LIGHT HOLDER      6                         12/01/10 08:26      2.55            17850           United Kingdom
    536365     71053         WHITE METAL LANTERN                     6                         12/01/10 08:26      3.39            17850           United Kingdom
    536365     84406B        CREAM CUPID HEARTS COAT HANGER          8                         12/01/10 08:26      2.75            17850           United Kingdom
    536365     84029G        KNITTED UNION FLAG HOT WATER BOTTLE     6                         12/01/10 08:26      3.39            17850           United Kingdom
    536365     84029E        RED WOOLLY HOTTIE WHITE HEART.          6                         12/01/10 08:26      3.39            17850           United Kingdom
    536365     22752         SET 7 BABUSHKA NESTING BOXES            2                         12/01/10 08:26      7.65            17850           United Kingdom
    536365     21730         GLASS STAR FROSTED T-LIGHT HOLDER       6                         12/01/10 08:26      4.25            17850           United Kingdom
    536366     22633         HAND WARMER UNION JACK                  6                         12/01/10 08:28      1.85            17850           United Kingdom
    536366     22632         HAND WARMER RED POLKA DOT               6                         12/01/10 08:28      1.85            17850           United Kingdom
    ```

    | Column | Description |
    |---|---|
    | `InvoiceNo` | 6-digit invoice number; prefix **C** = cancellation |
    | `StockCode` | 5-digit product code |
    | `Description` | Product name |
    | `Quantity` | Quantity per transaction |
    | `InvoiceDate` | Date and time of the transaction |
    | `UnitPrice` | Unit price in GBP |
    | `CustomerID` | 5-digit customer number |
    | `Country` | Customer's country |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1 — Setup
    """)
    return


@app.cell
def _():
    try:
        import duckdb
    except ImportError:
        pass  # (pip install removed: see the course setup)
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    plt.rcParams.update({'figure.figsize': (10, 4), 'axes.titlesize': 13, 'axes.labelsize': 11, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'figure.dpi': 110})
    COLORS = {'bar': '#4C72B0', 'line': '#DD8452', 'accent': '#55A868', 'cancel': '#C44E52'}
    # ── visual defaults ──────────────────────────────────────────────
    print(f'DuckDB {duckdb.__version__}  ✓')
    return COLORS, duckdb, mticker, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 — Load the Excel file *directly* into DuckDB

    DuckDB's **`spatial`** extension ships an XLSX/ODS reader (`st_read`).
    No pandas, no openpyxl — one SQL statement.
    """)
    return


@app.cell
def _(duckdb):
    # Create a DuckDB connection object
    con = duckdb.connect("online_retail.duckdb")

    # install the spatial extension (only needed once per database)
    con.execute("INSTALL spatial; LOAD spatial;").fetchall()

    # drop any prior copy so the notebook is re-runnable
    con.execute("DROP TABLE IF EXISTS raw").fetchall()

    con.execute("""
        CREATE OR REPLACE TABLE raw AS
        SELECT *
        FROM st_read(
                'online_retail.xlsx',
                layer = 'Online Retail',
                open_options = ['HEADERS=FORCE']
             )
    """).fetchall()

    row_count = con.execute("SELECT COUNT(*) FROM raw").fetchall()[0][0]
    print(f"Loaded {row_count:,} rows from online_retail.xlsx")
    return (con,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 — Schema inspection
    """)
    return


@app.cell
def _(con):
    con.sql("DESCRIBE raw").show()
    return


@app.cell
def _(con):
    con.sql("SELECT * FROM raw LIMIT 5").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 — Missing-value audit (all columns)
    """)
    return


@app.cell
def _(con):
    con.sql("""
        WITH counts AS (
            SELECT
                COUNT(*)                                              AS total_rows,
                SUM(CASE WHEN InvoiceNo   IS NULL THEN 1 ELSE 0 END) AS InvoiceNo,
                SUM(CASE WHEN StockCode   IS NULL THEN 1 ELSE 0 END) AS StockCode,
                SUM(CASE WHEN Description IS NULL THEN 1 ELSE 0 END) AS Description,
                SUM(CASE WHEN Quantity    IS NULL THEN 1 ELSE 0 END) AS Quantity,
                SUM(CASE WHEN InvoiceDate IS NULL THEN 1 ELSE 0 END) AS InvoiceDate,
                SUM(CASE WHEN UnitPrice   IS NULL THEN 1 ELSE 0 END) AS UnitPrice,
                SUM(CASE WHEN CustomerID  IS NULL THEN 1 ELSE 0 END) AS CustomerID,
                SUM(CASE WHEN Country     IS NULL THEN 1 ELSE 0 END) AS Country
            FROM raw
        )
        UNPIVOT counts
        ON InvoiceNo, StockCode, Description, Quantity,
           InvoiceDate, UnitPrice, CustomerID, Country
        INTO
            NAME column_name
            VALUE null_count
    """).show()

    # Also show the total row count for context
    total = con.execute("SELECT COUNT(*) FROM raw").fetchall()[0][0]
    print(f"\nTotal rows: {total:,}")
    return


@app.cell
def _(con):
    # missing-value percentages — easier to scan
    con.sql("""
        SELECT
            ROUND(100.0 * SUM(CASE WHEN Description IS NULL THEN 1 ELSE 0 END)
                  / COUNT(*), 2)  AS pct_null_Description,
            ROUND(100.0 * SUM(CASE WHEN CustomerID  IS NULL THEN 1 ELSE 0 END)
                  / COUNT(*), 2)  AS pct_null_CustomerID
        FROM raw
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Take-away:** `CustomerID` is missing in ~25 % of rows; `Description` in ~0.3 %.
    All other columns are fully populated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 — Descriptive statistics (SQL-only)
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            -- Quantity
            MIN(Quantity)                        AS qty_min,
            PERCENTILE_CONT(0.25) WITHIN GROUP
                (ORDER BY Quantity)              AS qty_q1,
            MEDIAN(Quantity)                     AS qty_median,
            ROUND(AVG(Quantity), 2)              AS qty_mean,
            PERCENTILE_CONT(0.75) WITHIN GROUP
                (ORDER BY Quantity)              AS qty_q3,
            MAX(Quantity)                        AS qty_max,
            -- UnitPrice
            MIN(UnitPrice)                       AS price_min,
            ROUND(MEDIAN(UnitPrice), 2)          AS price_median,
            ROUND(AVG(UnitPrice), 2)             AS price_mean,
            MAX(UnitPrice)                       AS price_max
        FROM raw
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Negative quantities are *cancellations* (invoice numbers prefixed with **C**).
    Zero or negative unit prices are test/adjustment rows.
    We will separate these in the cleaned table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 — Cancellation overview

    Before we clean, let's quantify cancellations.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            CASE WHEN InvoiceNo LIKE 'C%' THEN 'Cancelled' ELSE 'Normal' END AS order_type,
            COUNT(*)                               AS rows,
            COUNT(DISTINCT InvoiceNo)              AS invoices,
            ROUND(SUM(Quantity * UnitPrice), 2)    AS gross_value
        FROM raw
        GROUP BY order_type
        ORDER BY order_type
    """).show()
    return


@app.cell
def _(COLORS, con, plt):
    # cancellation rate by month
    df_cancel = con.sql("""
        SELECT
            DATE_TRUNC('month', InvoiceDate)::DATE   AS month,
            COUNT(DISTINCT InvoiceNo) FILTER
                (WHERE InvoiceNo LIKE 'C%')          AS cancelled_invoices,
            COUNT(DISTINCT InvoiceNo) FILTER
                (WHERE InvoiceNo NOT LIKE 'C%')      AS normal_invoices
        FROM raw
        GROUP BY month
        ORDER BY month
    """).df()

    df_cancel["cancel_rate_pct"] = (
        100 * df_cancel["cancelled_invoices"]
        / (df_cancel["cancelled_invoices"] + df_cancel["normal_invoices"])
    ).round(1)

    _fig, _ax = plt.subplots()
    _ax.bar(df_cancel["month"].astype(str), df_cancel["cancel_rate_pct"],
           color=COLORS["cancel"], width=0.6)
    _ax.set_title("Monthly Cancellation Rate (% of invoices)")
    _ax.set_ylabel("%")
    _ax.set_xlabel("Month")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 — Build the cleaned table

    Rules applied:

    1. Keep only **non-cancelled** rows (`InvoiceNo` does NOT start with `C`)
    2. `Quantity > 0` and `UnitPrice > 0`
    3. Fill missing `Description` → `'Unknown'`
    4. Cast `CustomerID` to `INTEGER` (fill missing → `0`)
    5. Add a computed `TotalPrice` column
    """)
    return


@app.cell
def _(con):
    con.execute("DROP TABLE IF EXISTS clean").fetchall()

    con.execute("""
        CREATE OR REPLACE TABLE clean AS
        SELECT
            InvoiceNo,
            StockCode,
            COALESCE(Description, 'Unknown')              AS Description,
            Quantity,
            InvoiceDate,
            UnitPrice,
            ROUND(Quantity * UnitPrice, 2)                 AS TotalPrice,
            COALESCE(CAST(CustomerID AS INTEGER), 0)       AS CustomerID,
            Country,
            -- derived time dimensions
            CAST(InvoiceDate AS DATE)                      AS InvoiceDay,
            DATE_TRUNC('month', InvoiceDate)::DATE         AS InvoiceMonth,
            EXTRACT(DOW  FROM InvoiceDate)                 AS DayOfWeek,   -- 0=Sun
            EXTRACT(HOUR FROM InvoiceDate)                 AS HourOfDay
        FROM raw
        WHERE InvoiceNo NOT LIKE 'C%'
          AND Quantity  > 0
          AND UnitPrice > 0
    """).fetchall()

    con.sql("""
        SELECT
            COUNT(*)                   AS rows,
            COUNT(DISTINCT InvoiceNo)  AS invoices,
            COUNT(DISTINCT CustomerID) AS customers,
            COUNT(DISTINCT StockCode)  AS products,
            COUNT(DISTINCT Country)    AS countries,
            MIN(InvoiceDate)::DATE     AS first_date,
            MAX(InvoiceDate)::DATE     AS last_date
        FROM clean
    """).show()
    return


@app.cell
def _(con):
    con.sql("SELECT * FROM clean LIMIT 5").show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 — Revenue overview
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            ROUND(SUM(TotalPrice), 2)              AS total_revenue,
            ROUND(AVG(TotalPrice), 2)              AS avg_line_revenue,
            ROUND(MEDIAN(TotalPrice), 2)           AS median_line_revenue,
            COUNT(DISTINCT InvoiceNo)              AS total_invoices,
            ROUND(SUM(TotalPrice)
                  / COUNT(DISTINCT InvoiceNo), 2)  AS avg_order_value
        FROM clean
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 — Monthly revenue trend
    """)
    return


@app.cell
def _(con):
    df_monthly = con.sql("""
        SELECT
            InvoiceMonth                                    AS month,
            ROUND(SUM(TotalPrice), 2)                       AS revenue,
            COUNT(DISTINCT InvoiceNo)                       AS orders,
            COUNT(DISTINCT CustomerID)                      AS unique_customers,
            -- month-over-month growth
            ROUND(100.0 * (SUM(TotalPrice)
                  - LAG(SUM(TotalPrice)) OVER (ORDER BY InvoiceMonth))
                  / LAG(SUM(TotalPrice)) OVER (ORDER BY InvoiceMonth), 1
            ) AS mom_growth_pct
        FROM clean
        GROUP BY InvoiceMonth
        ORDER BY InvoiceMonth
    """).df()

    df_monthly
    return (df_monthly,)


@app.cell
def _(COLORS, df_monthly, mticker, plt):
    _fig, _ax1 = plt.subplots(figsize=(11, 4.5))

    _ax1.bar(df_monthly["month"].astype(str), df_monthly["revenue"],
            color=COLORS["bar"], alpha=0.8, label="Revenue (GBP)")
    _ax1.set_ylabel("Revenue (GBP)")
    _ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))

    _ax2 = _ax1.twinx()
    _ax2.plot(df_monthly["month"].astype(str), df_monthly["orders"],
             color=COLORS["line"], marker="o", linewidth=2, label="Orders")
    _ax2.set_ylabel("Order count")

    _ax1.set_title("Monthly Revenue & Order Count")
    _ax1.set_xlabel("Month")
    plt.xticks(rotation=45, ha="right")

    # combined legend
    h1, l1 = _ax1.get_legend_handles_labels()
    h2, l2 = _ax2.get_legend_handles_labels()
    _ax1.legend(h1 + h2, l1 + l2, loc="upper left")

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10 — Top 10 countries by revenue
    """)
    return


@app.cell
def _(con):
    df_country = con.sql("""
        SELECT
            Country,
            ROUND(SUM(TotalPrice), 2)        AS revenue,
            COUNT(DISTINCT InvoiceNo)         AS orders,
            COUNT(DISTINCT CustomerID)        AS customers,
            ROUND(SUM(TotalPrice)
                  / COUNT(DISTINCT InvoiceNo), 2) AS avg_order_value
        FROM clean
        GROUP BY Country
        ORDER BY revenue DESC
        LIMIT 10
    """).df()

    df_country
    return (df_country,)


@app.cell
def _(COLORS, df_country, mticker, plt):
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # revenue
    _ax1.barh(df_country["Country"][::-1], df_country["revenue"][::-1],
             color=COLORS["bar"])
    _ax1.set_title("Revenue by Country (Top 10)")
    _ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1e6:.1f}M'))
    _ax1.set_xlabel("Revenue")

    # avg order value
    _ax2.barh(df_country["Country"][::-1], df_country["avg_order_value"][::-1],
             color=COLORS["accent"])
    _ax2.set_title("Avg Order Value by Country (Top 10)")
    _ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
    _ax2.set_xlabel("Avg Order Value (GBP)")

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11 — Top 15 products by quantity sold
    """)
    return


@app.cell
def _(con):
    df_products = con.sql("""
        SELECT
            Description,
            SUM(Quantity)                      AS total_qty,
            ROUND(SUM(TotalPrice), 2)          AS revenue,
            COUNT(DISTINCT InvoiceNo)          AS times_ordered
        FROM clean
        WHERE Description != 'Unknown'
        GROUP BY Description
        ORDER BY total_qty DESC
        LIMIT 15
    """).df()

    df_products
    return (df_products,)


@app.cell
def _(COLORS, df_products, mticker, plt):
    _fig, _ax = plt.subplots(figsize=(10, 6))
    _ax.barh(df_products["Description"][::-1], df_products["total_qty"][::-1],
            color=COLORS["bar"])
    _ax.set_title("Top 15 Products by Quantity Sold")
    _ax.set_xlabel("Units Sold")
    _ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 12 — Top 15 products by *revenue*
    """)
    return


@app.cell
def _(COLORS, con, mticker, plt):
    df_rev_prod = con.sql("""
        SELECT
            Description,
            ROUND(SUM(TotalPrice), 2) AS revenue,
            SUM(Quantity)              AS total_qty
        FROM clean
        WHERE Description != 'Unknown'
        GROUP BY Description
        ORDER BY revenue DESC
        LIMIT 15
    """).df()

    _fig, _ax = plt.subplots(figsize=(10, 6))
    _ax.barh(df_rev_prod["Description"][::-1], df_rev_prod["revenue"][::-1],
            color=COLORS["accent"])
    _ax.set_title("Top 15 Products by Revenue")
    _ax.set_xlabel("Revenue (GBP)")
    _ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1e3:.0f}K'))
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 13 — Temporal patterns: day-of-week & hour-of-day
    """)
    return


@app.cell
def _(COLORS, con, plt):
    df_dow = con.sql("""
        SELECT
            DayOfWeek,
            CASE DayOfWeek
                WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue'
                WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri'
                WHEN 6 THEN 'Sat'
            END AS day_name,
            COUNT(DISTINCT InvoiceNo)      AS orders,
            ROUND(SUM(TotalPrice), 2)      AS revenue
        FROM clean
        GROUP BY DayOfWeek
        ORDER BY DayOfWeek
    """).df()

    df_hour = con.sql("""
        SELECT
            HourOfDay,
            COUNT(DISTINCT InvoiceNo)      AS orders,
            ROUND(SUM(TotalPrice), 2)      AS revenue
        FROM clean
        GROUP BY HourOfDay
        ORDER BY HourOfDay
    """).df()

    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(14, 4.5))

    _ax1.bar(df_dow["day_name"], df_dow["orders"], color=COLORS["bar"])
    _ax1.set_title("Orders by Day of Week")
    _ax1.set_ylabel("Orders")

    _ax2.bar(df_hour["HourOfDay"].astype(int), df_hour["orders"], color=COLORS["line"])
    _ax2.set_title("Orders by Hour of Day")
    _ax2.set_xlabel("Hour (24 h)")
    _ax2.set_ylabel("Orders")

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 14 — Basket-size analysis

    How many distinct line items does a typical invoice contain?
    """)
    return


@app.cell
def _(con):
    con.sql("""
        WITH basket AS (
            SELECT
                InvoiceNo,
                COUNT(*)                  AS line_items,
                SUM(Quantity)             AS total_units,
                ROUND(SUM(TotalPrice), 2) AS basket_value
            FROM clean
            GROUP BY InvoiceNo
        )
        SELECT
            ROUND(AVG(line_items), 1)     AS avg_line_items,
            MEDIAN(line_items)            AS median_line_items,
            MAX(line_items)               AS max_line_items,
            ROUND(AVG(total_units), 1)    AS avg_units,
            ROUND(AVG(basket_value), 2)   AS avg_basket_value,
            ROUND(MEDIAN(basket_value), 2) AS median_basket_value
        FROM basket
    """).show()
    return


@app.cell
def _(COLORS, con, plt):
    df_basket = con.sql("""
        WITH basket AS (
            SELECT InvoiceNo,
                   COUNT(*) AS line_items
            FROM clean
            GROUP BY InvoiceNo
        )
        SELECT
            CASE
                WHEN line_items = 1        THEN '1'
                WHEN line_items BETWEEN 2  AND 5  THEN '2-5'
                WHEN line_items BETWEEN 6  AND 10 THEN '6-10'
                WHEN line_items BETWEEN 11 AND 20 THEN '11-20'
                ELSE '21+'
            END AS bucket,
            COUNT(*) AS invoices
        FROM basket
        GROUP BY bucket
        ORDER BY MIN(line_items)
    """).df()

    _fig, _ax = plt.subplots(figsize=(7, 4))
    _ax.bar(df_basket["bucket"], df_basket["invoices"], color=COLORS["bar"])
    _ax.set_title("Basket Size Distribution (line items per invoice)")
    _ax.set_xlabel("Line items")
    _ax.set_ylabel("Number of invoices")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 15 — Top 10 customers by lifetime spend
    """)
    return


@app.cell
def _(con):
    con.sql("""
        SELECT
            CustomerID,
            COUNT(DISTINCT InvoiceNo)              AS orders,
            SUM(Quantity)                           AS total_units,
            ROUND(SUM(TotalPrice), 2)              AS lifetime_spend,
            MIN(InvoiceDate)::DATE                  AS first_order,
            MAX(InvoiceDate)::DATE                  AS last_order
        FROM clean
        WHERE CustomerID != 0
        GROUP BY CustomerID
        ORDER BY lifetime_spend DESC
        LIMIT 10
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 16 — Customer frequency: one-timers vs. repeat buyers
    """)
    return


@app.cell
def _(con):
    df_freq = con.sql("""
        WITH cust AS (
            SELECT  CustomerID,
                    COUNT(DISTINCT InvoiceNo) AS order_count
            FROM clean
            WHERE CustomerID != 0
            GROUP BY CustomerID
        )
        SELECT
            CASE
                WHEN order_count = 1          THEN '1 order'
                WHEN order_count BETWEEN 2  AND 5  THEN '2-5 orders'
                WHEN order_count BETWEEN 6  AND 10 THEN '6-10 orders'
                WHEN order_count BETWEEN 11 AND 20 THEN '11-20 orders'
                ELSE '21+ orders'
            END AS segment,
            COUNT(*)              AS customers,
            ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
        FROM cust
        GROUP BY segment
        ORDER BY MIN(order_count)
    """).df()

    df_freq
    return (df_freq,)


@app.cell
def _(COLORS, df_freq, plt):
    _fig, _ax = plt.subplots(figsize=(7, 4))
    wedges, texts, autotexts = _ax.pie(
        df_freq["customers"], labels=df_freq["segment"],
        autopct="%1.1f%%", startangle=140,
        colors=[COLORS["bar"], COLORS["line"], COLORS["accent"],
                COLORS["cancel"], "#937860"]
    )
    _ax.set_title("Customer Frequency Segments")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 17 — RFM snapshot (Recency, Frequency, Monetary)

    A lightweight RFM analysis using SQL window-function quartiles.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        WITH rfm_raw AS (
            SELECT
                CustomerID,
                -- days since last purchase (relative to dataset max date)
                DATE_DIFF('day',
                    MAX(InvoiceDate),
                    (SELECT MAX(InvoiceDate) FROM clean)
                ) AS recency,
                COUNT(DISTINCT InvoiceNo)   AS frequency,
                ROUND(SUM(TotalPrice), 2)   AS monetary
            FROM clean
            WHERE CustomerID != 0
            GROUP BY CustomerID
        ),
        rfm_scored AS (
            SELECT *,
                NTILE(4) OVER (ORDER BY recency   DESC) AS r_score,  -- lower recency = better
                NTILE(4) OVER (ORDER BY frequency  ASC) AS f_score,
                NTILE(4) OVER (ORDER BY monetary   ASC) AS m_score
            FROM rfm_raw
        )
        SELECT
            r_score || '-' || f_score || '-' || m_score AS rfm,
            CASE
                WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
                WHEN r_score >= 3 AND f_score >= 2                  THEN 'Loyal'
                WHEN r_score >= 3                                   THEN 'Recent'
                WHEN f_score >= 3                                   THEN 'Frequent'
                WHEN m_score >= 3                                   THEN 'Big Spenders'
                WHEN r_score <= 1 AND f_score <= 1                  THEN 'At Risk'
                ELSE 'Other'
            END AS segment,
            COUNT(*)                    AS customers,
            ROUND(AVG(monetary), 2)     AS avg_monetary,
            ROUND(AVG(frequency), 1)    AS avg_frequency,
            ROUND(AVG(recency), 0)      AS avg_recency_days
        FROM rfm_scored
        GROUP BY segment, rfm
        ORDER BY customers DESC
        LIMIT 15
    """).show()
    return


@app.cell
def _(COLORS, con, plt):
    # segment summary
    df_rfm_seg = con.sql("""
        WITH rfm_raw AS (
            SELECT
                CustomerID,
                DATE_DIFF('day',
                    MAX(InvoiceDate),
                    (SELECT MAX(InvoiceDate) FROM clean)
                ) AS recency,
                COUNT(DISTINCT InvoiceNo) AS frequency,
                ROUND(SUM(TotalPrice), 2) AS monetary
            FROM clean
            WHERE CustomerID != 0
            GROUP BY CustomerID
        ),
        rfm_scored AS (
            SELECT *,
                NTILE(4) OVER (ORDER BY recency   DESC) AS r_score,
                NTILE(4) OVER (ORDER BY frequency  ASC) AS f_score,
                NTILE(4) OVER (ORDER BY monetary   ASC) AS m_score
            FROM rfm_raw
        ),
        segmented AS (
            SELECT *,
                CASE
                    WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
                    WHEN r_score >= 3 AND f_score >= 2                  THEN 'Loyal'
                    WHEN r_score >= 3                                   THEN 'Recent'
                    WHEN f_score >= 3                                   THEN 'Frequent'
                    WHEN m_score >= 3                                   THEN 'Big Spenders'
                    WHEN r_score <= 1 AND f_score <= 1                  THEN 'At Risk'
                    ELSE 'Other'
                END AS segment
            FROM rfm_scored
        )
        SELECT
            segment,
            COUNT(*)                 AS customers,
            ROUND(AVG(monetary), 2)  AS avg_spend,
            ROUND(AVG(frequency), 1) AS avg_orders,
            ROUND(AVG(recency), 0)   AS avg_recency
        FROM segmented
        GROUP BY segment
        ORDER BY customers DESC
    """).df()

    _fig, _ax = plt.subplots(figsize=(8, 4))
    bars = _ax.barh(df_rfm_seg["segment"][::-1], df_rfm_seg["customers"][::-1],
                   color=COLORS["bar"])
    _ax.set_title("RFM Customer Segments")
    _ax.set_xlabel("Number of customers")
    _ax.bar_label(bars, padding=3)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 18 — Revenue concentration (Pareto / 80-20 rule)
    """)
    return


@app.cell
def _(COLORS, con, plt):
    df_pareto = con.sql("""
        WITH cust_rev AS (
            SELECT  CustomerID,
                    SUM(TotalPrice) AS revenue
            FROM clean
            WHERE CustomerID != 0
            GROUP BY CustomerID
        ),
        ranked AS (
            SELECT  *,
                    ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rn,
                    COUNT(*) OVER ()                          AS total_cust
            FROM cust_rev
        )
        SELECT
            ROUND(100.0 * rn / total_cust, 2) AS pct_customers,
            ROUND(100.0 * SUM(revenue) OVER (ORDER BY revenue DESC)
                  / SUM(revenue) OVER (), 2)  AS cumulative_revenue_pct
        FROM ranked
        ORDER BY rn
    """).df()

    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax.plot(df_pareto["pct_customers"], df_pareto["cumulative_revenue_pct"],
            color=COLORS["bar"], linewidth=2)
    _ax.axhline(80, color="gray", linestyle="--", linewidth=0.8)
    _ax.axvline(20, color="gray", linestyle="--", linewidth=0.8)
    _ax.fill_between(df_pareto["pct_customers"], df_pareto["cumulative_revenue_pct"],
                    alpha=0.15, color=COLORS["bar"])
    _ax.set_title("Revenue Concentration (Pareto Curve)")
    _ax.set_xlabel("% of Customers (ranked by revenue)")
    _ax.set_ylabel("Cumulative % of Revenue")
    _ax.set_xlim(0, 100)
    _ax.set_ylim(0, 100)
    _ax.text(22, 75, "80/20 reference", fontsize=9, color="gray")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 19 — Daily revenue time-series with 7-day moving average
    """)
    return


@app.cell
def _(COLORS, con, mticker, plt):
    df_daily = con.sql("""
        SELECT
            InvoiceDay                            AS day,
            ROUND(SUM(TotalPrice), 2)             AS revenue,
            ROUND(AVG(SUM(TotalPrice)) OVER (
                ORDER BY InvoiceDay
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ), 2)                                 AS ma_7d
        FROM clean
        GROUP BY InvoiceDay
        ORDER BY InvoiceDay
    """).df()

    _fig, _ax = plt.subplots(figsize=(13, 4.5))
    _ax.fill_between(df_daily["day"], df_daily["revenue"],
                    alpha=0.25, color=COLORS["bar"], label="Daily revenue")
    _ax.plot(df_daily["day"], df_daily["ma_7d"],
            color=COLORS["line"], linewidth=2, label="7-day moving avg")
    _ax.set_title("Daily Revenue with 7-Day Moving Average")
    _ax.set_ylabel("Revenue (GBP)")
    _ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1e3:.0f}K'))
    _ax.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 20 — UK vs. International revenue share over time
    """)
    return


@app.cell
def _(COLORS, con, mticker, plt):
    df_uk = con.sql("""
        SELECT
            InvoiceMonth AS month,
            ROUND(SUM(TotalPrice) FILTER
                (WHERE Country = 'United Kingdom'), 2)    AS uk_revenue,
            ROUND(SUM(TotalPrice) FILTER
                (WHERE Country != 'United Kingdom'), 2)   AS intl_revenue
        FROM clean
        GROUP BY InvoiceMonth
        ORDER BY InvoiceMonth
    """).df()

    _fig, _ax = plt.subplots(figsize=(11, 4.5))
    _ax.bar(df_uk["month"].astype(str), df_uk["uk_revenue"],
           label="UK", color=COLORS["bar"])
    _ax.bar(df_uk["month"].astype(str), df_uk["intl_revenue"],
           bottom=df_uk["uk_revenue"],
           label="International", color=COLORS["accent"])
    _ax.set_title("UK vs International Revenue by Month")
    _ax.set_ylabel("Revenue (GBP)")
    _ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1e6:.1f}M'))
    plt.xticks(rotation=45, ha="right")
    _ax.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 21 — Unit-price distribution (log scale)
    """)
    return


@app.cell
def _(COLORS, con, plt):
    df_price_dist = con.sql("""
        SELECT
            CASE
                WHEN UnitPrice < 1    THEN '<£1'
                WHEN UnitPrice < 2    THEN '£1-2'
                WHEN UnitPrice < 5    THEN '£2-5'
                WHEN UnitPrice < 10   THEN '£5-10'
                WHEN UnitPrice < 20   THEN '£10-20'
                WHEN UnitPrice < 50   THEN '£20-50'
                ELSE '£50+'
            END AS price_band,
            COUNT(*)          AS transactions,
            SUM(Quantity)     AS total_units
        FROM clean
        GROUP BY price_band
        ORDER BY MIN(UnitPrice)
    """).df()

    _fig, _ax = plt.subplots(figsize=(8, 4))
    _ax.bar(df_price_dist["price_band"], df_price_dist["transactions"],
           color=COLORS["bar"])
    _ax.set_title("Transaction Count by Unit Price Band")
    _ax.set_xlabel("Unit Price")
    _ax.set_ylabel("Transactions (log scale)")
    _ax.set_yscale("log")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 22 — Monthly cohort: new vs returning customers
    """)
    return


@app.cell
def _(COLORS, con, plt):
    df_cohort = con.sql("""
        WITH first_purchase AS (
            SELECT CustomerID,
                   MIN(InvoiceMonth) AS cohort_month
            FROM clean
            WHERE CustomerID != 0
            GROUP BY CustomerID
        ),
        monthly_activity AS (
            SELECT DISTINCT
                   c.CustomerID,
                   c.InvoiceMonth AS activity_month,
                   f.cohort_month
            FROM clean c
            JOIN first_purchase f USING (CustomerID)
            WHERE c.CustomerID != 0
        )
        SELECT
            activity_month                                          AS month,
            COUNT(*) FILTER (WHERE activity_month = cohort_month)   AS new_customers,
            COUNT(*) FILTER (WHERE activity_month != cohort_month)  AS returning_customers
        FROM monthly_activity
        GROUP BY activity_month
        ORDER BY activity_month
    """).df()

    _fig, _ax = plt.subplots(figsize=(11, 4.5))
    _ax.bar(df_cohort["month"].astype(str), df_cohort["new_customers"],
           label="New", color=COLORS["bar"])
    _ax.bar(df_cohort["month"].astype(str), df_cohort["returning_customers"],
           bottom=df_cohort["new_customers"],
           label="Returning", color=COLORS["accent"])
    _ax.set_title("New vs Returning Customers by Month")
    _ax.set_ylabel("Unique Customers")
    plt.xticks(rotation=45, ha="right")
    _ax.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 23 — Products frequently bought together (association pairs)

    Self-join invoices to find the most common product co-occurrences.
    """)
    return


@app.cell
def _(con):
    con.sql("""
        WITH invoice_products AS (
            SELECT DISTINCT InvoiceNo, Description
            FROM clean
            WHERE Description != 'Unknown'
        )
        SELECT
            a.Description AS product_a,
            b.Description AS product_b,
            COUNT(*)      AS co_occurrences
        FROM invoice_products a
        JOIN invoice_products b
          ON a.InvoiceNo = b.InvoiceNo
         AND a.Description < b.Description      -- avoid duplicates & self-joins
        GROUP BY a.Description, b.Description
        ORDER BY co_occurrences DESC
        LIMIT 10
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 24 — Summary of SQL concepts demonstrated

    | SQL Feature | Where Used |
    |---|---|
    | `st_read()` (spatial extension) | §2 — native XLSX loading |
    | `CREATE TABLE … AS SELECT` | §7 — data cleaning |
    | `COALESCE`, `CASE WHEN` | §7 — null handling & bucketing |
    | `GROUP BY` + aggregates | Throughout — counts, sums, averages |
    | `DATE_TRUNC`, `EXTRACT` | §9, §13 — time-series & temporal |
    | `FILTER (WHERE …)` | §6, §20, §22 — conditional aggregates |
    | `LAG()` window function | §9 — month-over-month growth |
    | `NTILE()` window function | §17 — RFM quartile scoring |
    | `SUM() OVER (ORDER BY …)` | §18 — running cumulative totals |
    | Moving-window frame | §19 — 7-day moving average |
    | CTE (`WITH … AS`) | §14, §16–§18, §22–§23 |
    | Self-join | §23 — market basket pairs |
    | `ROW_NUMBER()`, `PERCENT_RANK()` | §18 — Pareto curve |

    ### Key business insights

    1. **Revenue peaks** in Sep–Nov, driven by holiday buying.
    2. The **UK dominates** (~85 % of revenue), but international AOV can be higher.
    3. **~25 % of rows** lack a CustomerID — a data-quality gap worth investigating.
    4. Revenue follows the **Pareto principle**: a small share of customers drives most revenue.
    5. **Weekday mornings** (10–12 h) are the busiest ordering window.
    6. Cancellation rates hover around **2–3 %** of invoices per month.

    ---
    *Notebook authored for Data Warehousing — Week 3: Classic Data Warehousing.*
    """)
    return


@app.cell
def _(con):
    con.close()
    print("DuckDB connection closed.  ✓")
    return


if __name__ == "__main__":
    app.run()
