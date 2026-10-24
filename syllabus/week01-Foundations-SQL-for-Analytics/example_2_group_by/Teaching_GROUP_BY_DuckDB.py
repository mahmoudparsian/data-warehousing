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
    # Teaching GROUP BY with DuckDB

    This notebook answers the requested GROUP BY questions using the small `sales.csv` dataset.

    For each question, the notebook includes:
    1. Natural-language question
    2. SQL query
    3. Explanation of the SQL
    4. Business insight
    5. A simple plot when it helps
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt

    pd.set_option('display.float_format', '{:,.0f}'.format)

    con = duckdb.connect()

    INPUT_PATH = "."
    file_path = f"{INPUT_PATH}/sales.csv"

    con.execute("""
    CREATE OR REPLACE TABLE sales AS
    SELECT * FROM read_csv_auto(?);
    """, [file_path]).fetchall()

    con.execute("SELECT * FROM sales LIMIT 5").df()
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Schema and Row Count
    """)
    return


@app.cell
def _(con):
    schema_df = con.execute("DESCRIBE sales").df()
    row_df = con.execute("SELECT COUNT(*) AS row_count FROM sales").df()
    schema_df, row_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Display all records from sales table

    **Question:** Display all records from sales table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql = """SELECT *
    FROM sales;"""
    print(sql)
    return (sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql):
    _df = con.execute(sql).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This query reads every row and every column from the `sales` table.
    It is the simplest way to inspect the raw data before doing aggregation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    Before using `GROUP BY`, it is important to understand the raw transaction-level data.
    This helps confirm the columns available for later grouping: `country`, `product`, and `price`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Total sales for all products for USA

    **Question:** Find total sales for all products for USA.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_2 = """SELECT 
        country,
        SUM(price) AS total_sales
    FROM sales
    WHERE country = 'USA'
    GROUP BY country;"""
    print(sql_2)
    return (sql_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_2):
    df = con.execute(sql_2).df()
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `WHERE country = 'USA'` filters rows to USA only.
    `SUM(price)` adds the prices of all USA sales.
    `GROUP BY country` returns one aggregated row for USA.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This gives the overall revenue generated in the USA.
    It is useful for country-level performance measurement and for comparing with other markets later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df, plt):
    plt.figure(figsize=(6,4))
    plt.bar(df['country'], df['total_sales'])
    plt.title('Total Sales for USA')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Total sales for all products for all countries

    **Question:** Find total sales for all products for all countries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_3 = """SELECT 
        country,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY country
    ORDER BY total_sales DESC;"""
    print(sql_3)
    return (sql_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_3):
    df_2 = con.execute(sql_3).df()
    df_2
    return (df_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    The query groups all rows by `country` and computes total sales with `SUM(price)`.
    `ORDER BY total_sales DESC` sorts countries from highest to lowest total sales.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This compares country performance directly.
    Management can quickly see which country is strongest and which country may need improvement.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_2, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_2['country'], df_2['total_sales'])
    plt.title('Total Sales by Country')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. List of unique countries

    **Question:** Find the list of unique countries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_4 = """SELECT DISTINCT country
    FROM sales
    ORDER BY country;"""
    print(sql_4)
    return (sql_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_4):
    _df = con.execute(sql_4).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `DISTINCT` removes duplicates and returns each country only once.
    This is not a `GROUP BY` query, but it is often used before aggregation to understand dimensions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This tells us which markets exist in the dataset.
    It is useful when validating the data before performing grouped analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. List of unique products

    **Question:** Find the list of unique products.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_5 = """SELECT DISTINCT product
    FROM sales
    ORDER BY product;"""
    print(sql_5)
    return (sql_5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_5):
    _df = con.execute(sql_5).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `DISTINCT product` returns the unique product categories sold in the table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This shows the product catalog represented in the data.
    It helps define the business dimensions that can be grouped later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Total product sales per country

    **Question:** Find total product sales per country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_6 = """SELECT 
        country,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY country
    ORDER BY total_sales DESC;"""
    print(sql_6)
    return (sql_6,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_6):
    df_3 = con.execute(sql_6).df()
    df_3
    return (df_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This is the classic first `GROUP BY` pattern: aggregate one metric by one dimension.
    Here, the metric is `SUM(price)` and the dimension is `country`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    The result shows how much each country contributes to total sales.
    It can guide market prioritization and country-specific strategy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_3, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_3['country'], df_3['total_sales'])
    plt.title('Total Product Sales per Country')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Total product sales per product

    **Question:** Find total product sales per product.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_7 = """SELECT 
        product,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY product
    ORDER BY total_sales DESC;"""
    print(sql_7)
    return (sql_7,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_7):
    df_4 = con.execute(sql_7).df()
    df_4
    return (df_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This groups the rows by product instead of country.
    Each product receives one aggregated total using `SUM(price)`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This reveals which product line drives the most revenue.
    It helps with product strategy, promotions, and inventory decisions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_4, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_4['product'], df_4['total_sales'])
    plt.title('Total Product Sales per Product')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Total product sales per country and product

    **Question:** Find total product sales per country and product.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_8 = """SELECT 
        country,
        product,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY country, product
    ORDER BY country, total_sales DESC;"""
    print(sql_8)
    return (sql_8,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_8):
    _df = con.execute(sql_8).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This query uses a multi-column `GROUP BY`.
    It creates one group for each `(country, product)` combination and computes total sales for each pair.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This provides a more detailed view than grouping by country or product alone.
    It helps answer questions such as: which product is strongest inside each country?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Number of sales per country

    **Question:** Find the number of sales per country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_9 = """SELECT 
        country,
        COUNT(*) AS num_sales
    FROM sales
    GROUP BY country
    ORDER BY num_sales DESC;"""
    print(sql_9)
    return (sql_9,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_9):
    df_5 = con.execute(sql_9).df()
    df_5
    return (df_5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `COUNT(*)` counts the number of rows in each country group.
    This measures transaction volume rather than revenue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    A country may have many transactions but not the highest revenue.
    This distinction is important: volume and value are not always the same.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_5, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_5['country'], df_5['num_sales'])
    plt.title('Number of Sales per Country')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Top selling product per country

    **Question:** Write a SQL query to find top selling product per country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_10 = """SELECT *
    FROM (
        SELECT 
            country,
            product,
            SUM(price) AS total_sales,
            RANK() OVER (
                PARTITION BY country
                ORDER BY SUM(price) DESC
            ) AS rnk
        FROM sales
        GROUP BY country, product
    ) t
    WHERE rnk = 1
    ORDER BY country;"""
    print(sql_10)
    return (sql_10,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_10):
    df_6 = con.execute(sql_10).df()
    df_6
    return (df_6,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    First, `GROUP BY country, product` computes sales totals per product within each country.
    Then `RANK() OVER (PARTITION BY country ORDER BY SUM(price) DESC)` ranks products inside each country.
    Finally, `WHERE rnk = 1` keeps the top product per country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This shows the best-performing product in each market.
    It is useful for local marketing strategy and identifying country-specific preferences.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_6, plt):
    plt.figure(figsize=(8,4))
    labels = df_6['country'] + '-' + df_6['product']
    plt.bar(labels, df_6['total_sales'])
    plt.title('Top Selling Product per Country')
    plt.ylabel('Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. Top selling country overall

    **Question:** Write a SQL query to find top selling country overall.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_11 = """SELECT 
        country,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY country
    ORDER BY total_sales DESC
    LIMIT 1;"""
    print(sql_11)
    return (sql_11,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_11):
    _df = con.execute(sql_11).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This groups by country, computes total sales, sorts from highest to lowest, and returns the top row only.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This identifies the best-performing market overall.
    It is a simple but important executive-level KPI.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. Full ranking of all countries

    **Question:** Show full ranking of all countries based on sale of products.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_12 = """SELECT 
        country,
        SUM(price) AS total_sales,
        RANK() OVER (ORDER BY SUM(price) DESC) AS country_rank
    FROM sales
    GROUP BY country
    ORDER BY country_rank;"""
    print(sql_12)
    return (sql_12,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_12):
    df_7 = con.execute(sql_12).df()
    df_7
    return (df_7,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `GROUP BY country` computes country totals, and the window function `RANK()` assigns a ranking based on descending total sales.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This gives a complete leaderboard of markets.
    It is more informative than only showing the top country because it shows the relative position of every country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_7, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_7['country'], df_7['total_sales'])
    for i, v in enumerate(df_7['country_rank']):
        plt.text(i, df_7['total_sales'].iloc[i] + 20, f'Rank {int(v)}', ha='center')
    plt.title('Country Ranking by Total Sales')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. Countries with more than $1500 in sales

    **Question:** Find list of countries which have sold products more than $1500.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_13 = """SELECT 
        country,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY country
    HAVING SUM(price) > 1800
    ORDER BY total_sales DESC;"""
    print(sql_13)
    return (sql_13,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_13):
    _df = con.execute(sql_13).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `HAVING` filters groups after aggregation.
    This is different from `WHERE`, which filters rows before aggregation.
    Here, only countries with grouped total sales above 1500 are returned.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This identifies strong markets that pass a business threshold.
    Threshold-based grouping is common in reporting and decision-making.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. Highest price product sold per country

    **Question:** Find highest price product sold per country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_14 = """SELECT 
        country,
        MAX(price) AS highest_price
    FROM sales
    GROUP BY country
    ORDER BY highest_price DESC;"""
    print(sql_14)
    return (sql_14,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_14):
    df_8 = con.execute(sql_14).df()
    df_8
    return (df_8,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    `MAX(price)` returns the highest individual transaction value inside each country group.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This highlights the most expensive sale observed in each market.
    It helps identify where premium products or high-value purchases occur.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_8, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_8['country'], df_8['highest_price'])
    plt.title('Highest Price Sold per Country')
    plt.ylabel('Price')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Extra GROUP BY Practice
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## E1. Average selling price per country

    **Question:** Find average selling price per country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_15 = """SELECT 
        country,
        AVG(price) AS avg_price
    FROM sales
    GROUP BY country
    ORDER BY avg_price DESC;"""
    print(sql_15)
    return (sql_15,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_15):
    df_9 = con.execute(sql_15).df()
    df_9
    return (df_9,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This groups rows by country and computes the average transaction price using `AVG(price)`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    A country can have fewer sales but a higher average price.
    This helps distinguish premium markets from high-volume markets.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_9, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_9['country'], df_9['avg_price'])
    plt.title('Average Selling Price per Country')
    plt.ylabel('Average Price')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## E2. Average selling price per product

    **Question:** Find average selling price per product.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_16 = """SELECT 
        product,
        AVG(price) AS avg_price
    FROM sales
    GROUP BY product
    ORDER BY avg_price DESC;"""
    print(sql_16)
    return (sql_16,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_16):
    df_10 = con.execute(sql_16).df()
    df_10
    return (df_10,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This computes the average transaction price for each product category.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This helps compare premium vs lower-priced product lines and can support pricing analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plot
    """)
    return


@app.cell
def _(df_10, plt):
    plt.figure(figsize=(7,4))
    plt.bar(df_10['product'], df_10['avg_price'])
    plt.title('Average Selling Price per Product')
    plt.ylabel('Average Price')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## E3. Country-product matrix with count and sales

    **Question:** Find transaction count and total sales for each country-product combination.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL
    """)
    return


@app.cell
def _():
    sql_17 = """SELECT 
        country,
        product,
        COUNT(*) AS num_sales,
        SUM(price) AS total_sales
    FROM sales
    GROUP BY country, product
    ORDER BY country, product;"""
    print(sql_17)
    return (sql_17,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Run SQL
    """)
    return


@app.cell
def _(con, sql_17):
    _df = con.execute(sql_17).df()
    _df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL Explanation
    This is a richer multi-dimensional aggregation because it combines both `COUNT(*)` and `SUM(price)` for each `(country, product)` pair.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Business Insight
    This shows both revenue and transaction volume together.
    It helps distinguish frequent low-value sales from fewer high-value sales.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Final Teaching Notes

    ## Key ideas reinforced
    - `GROUP BY` groups rows into categories
    - `SUM`, `COUNT`, `AVG`, and `MAX` summarize each group
    - `HAVING` filters grouped results
    - Window functions such as `RANK()` help with top-N analysis after aggregation

    ## Practical business takeaway
    The same dataset can answer:
    - market performance questions
    - product performance questions
    - ranking questions
    - threshold questions
    - premium-price questions
    """)
    return


if __name__ == "__main__":
    app.run()
