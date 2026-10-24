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
    # 🧱 MEDALLION ARCHITECTURE — GROUP BY MASTERCLASS
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    con = duckdb.connect()
    return con, plt


@app.cell
def _():
    INPUT_PATH = "."
    file_path = f"sales.csv"
    return (file_path,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🥉 Bronze Layer
    """)
    return


@app.cell
def _(con, file_path):
    con.execute(f"""
    CREATE OR REPLACE TABLE bronze_sales AS
    SELECT * FROM read_csv_auto('{file_path}');
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute(f"""
    SELECT * FROM  bronze_sales LIMIT 5;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🥈 Silver Layer
    """)
    return


@app.cell
def _(con):
    con.execute(f"""
    CREATE OR REPLACE TABLE silver_sales AS
    SELECT *,
        EXTRACT(YEAR FROM transaction_date) AS year,
        EXTRACT(MONTH FROM transaction_date) AS month,
        EXTRACT(QUARTER FROM transaction_date) AS quarter,
        STRFTIME(transaction_date, '%A') AS day_of_week,
        price * quantity * (1 - discount) AS sale_price
    FROM bronze_sales;
    """).fetchall()
    return


@app.cell
def _(con):
    con.execute(f"""
    SELECT * FROM  silver_sales LIMIT 5;
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Monthly Revenue
    **Insight Goal:** Trend over time
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT year, month, SUM(sale_price) AS revenue
    FROM silver_sales
    GROUP BY year, month
    ORDER BY year, month
    """).df()

    # Create proper time label
    _df["year_month"] = _df["year"].astype(str) + "-" + _df["month"].astype(str).str.zfill(2)

    plt.figure(figsize=(12, 5))
    plt.plot(_df["year_month"], _df["revenue"], marker='o')

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Year-Month")
    plt.ylabel("Revenue")

    plt.xticks(rotation=60)
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Quarterly Revenue
    **Insight Goal:** Seasonality
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""
    SELECT year, quarter, SUM(sale_price) AS revenue
    FROM silver_sales
    GROUP BY year, quarter
    ORDER BY year, quarter
    """).df()

    # Create proper label: 2023-Q1, etc.
    _df["year_quarter"] = _df["year"].astype(str) + "-Q" + _df["quarter"].astype(str)

    plt.figure(figsize=(12, 5))
    plt.plot(_df["year_quarter"], _df["revenue"], marker='o', linewidth=2)

    plt.title("📊 Quarterly Revenue Trend")
    plt.xlabel("Year-Quarter")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Revenue by Country
    **Insight Goal:** Market performance
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT country, SUM(sale_price) AS revenue
    FROM silver_sales
    GROUP BY country
    ORDER BY revenue DESC""").df()

    plt.figure()
    plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    plt.xticks(rotation=45)
    plt.title("Revenue by Country")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Revenue by Product
    **Insight Goal:** Product strategy
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT product_name, SUM(sale_price) AS revenue
    FROM silver_sales
    GROUP BY product_name
    ORDER BY revenue DESC""").df()

    plt.figure()
    plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    plt.xticks(rotation=45)
    plt.title("Revenue by Product")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 Revenue by Day of Week
    **Insight Goal:** Weekend vs weekday
    """)
    return


@app.cell
def _(con, plt):
    _df = con.execute("""SELECT day_of_week, SUM(sale_price) AS revenue
    FROM silver_sales
    GROUP BY day_of_week""").df()

    plt.figure()
    plt.bar(_df[_df.columns[0]], _df[_df.columns[1]])
    plt.xticks(rotation=45)
    plt.title("Revenue by Day of Week")
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🥇 Gold Layer
    """)
    return


@app.cell
def _(con):
    # 🟨 🧱 Cell 1 — SQL (Gold Layer)
    df = con.execute("""
    SELECT 
        year,
        quarter,
        SUM(sale_price) AS total_revenue,
        COUNT(*) AS total_orders,
        AVG(sale_price) AS avg_order_value
    FROM silver_sales
    GROUP BY year, quarter
    ORDER BY year, quarter
    """).df()

    df.head(20)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    Business Insight:

    1. Quarterly revenue helps identify seasonality patterns.
    2. Compare Q1–Q4 performance across years to detect growth trends.
    3. Total orders vs revenue:
       - High revenue + low orders → high-value purchases
       - High orders + lower revenue → volume-driven sales
    4. Average order value indicates pricing strength and customer spending behavior.

    Key Questions:
    - Which quarter performs best?
    - Is there consistent growth year over year?
    - Are we improving revenue per transaction?
    ```
    """)
    return


@app.cell
def _(df, plt):
    # 📊 🟨 Cell 3 — Plot (Executive Quality)


    # Create label
    df["year_quarter"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)

    plt.figure(figsize=(12, 5))

    plt.plot(df["year_quarter"], df["total_revenue"], marker='o', linewidth=2)

    plt.title("📊 Quarterly Revenue Trend")
    plt.xlabel("Year-Quarter")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, plt):
    # 👉 Add comparison across years

    plt.figure(figsize=(10, 5))

    for year in sorted(df["year"].unique()):
        temp = df[df["year"] == year]
        plt.plot(temp["quarter"], temp["total_revenue"], marker='o', label=year)

    plt.title("Quarterly Revenue by Year")
    plt.xlabel("Quarter")
    plt.ylabel("Revenue")

    plt.xticks([1,2,3,4])
    plt.legend(title="Year")
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
