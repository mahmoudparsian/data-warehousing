import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb
    import pandas as pd
    import matplotlib.pyplot as plt
    from IPython.display import display, Markdown

    INPUT_PATHS = ["sales_2023.csv","sales_2024.csv","sales_2025.csv","sales_2026.csv"]
    con = duckdb.connect()
    union_sql = " UNION ALL ".join([f"SELECT * FROM read_csv_auto('{p}')" for p in INPUT_PATHS])
    con.execute(f"CREATE OR REPLACE TABLE sales AS {union_sql}").fetchall()

    def show_query_block(title, nlq, sql):
        display(Markdown(f"## {title}"))
        display(Markdown(f"**Natural Language Question:** {nlq}"))
        display(Markdown("**SQL Query:**"))
        display(Markdown(f"```sql\n{sql}\n```"))

    def run_query(sql):
        df = con.execute(sql).df()
        display(df.head(20))
        return df

    def plot_result(df, kind="bar", x=None, y=None, title=None, bins=25):
        if df.empty:
            print("No rows to plot."); return
        plt.figure(figsize=(10,4))
        if kind == "bar":
            plt.bar(df[x].astype(str), df[y]); plt.xlabel(x); plt.ylabel(y)
        elif kind == "line":
            plt.plot(df[x].astype(str), df[y], marker="o"); plt.xlabel(x); plt.ylabel(y)
        elif kind == "hist":
            plt.hist(df[x], bins=bins); plt.xlabel(x); plt.ylabel("count")
        plt.title(title if title else "")
        plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()

    def insight(lines):
        md = "\n".join([f"- {line}" for line in lines])
        display(Markdown(f"**Business Insight:**\n{md}"))

    print(con.execute("SELECT COUNT(*) AS total_rows FROM sales").df())
    return insight, plot_result, plt, run_query, show_query_block


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '1. GROUP BY — Monthly Sales'
    _nlq = 'What is the total sales amount by month across all years?'
    _sql = '''SELECT EXTRACT(MONTH FROM transaction_date) AS sale_month, SUM(sales_amount) AS total_sales FROM sales GROUP BY sale_month ORDER BY sale_month;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='line', x='sale_month', y='total_sales', title='Monthly Sales')
    insight(['Monthly sales show seasonality and calendar effects.', 'This helps identify stronger and weaker months for planning.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '2. GROUP BY — Yearly Sales'
    _nlq = 'What is the total sales amount by year?'
    _sql = '''SELECT EXTRACT(YEAR FROM transaction_date) AS sale_year, SUM(sales_amount) AS total_sales FROM sales GROUP BY sale_year ORDER BY sale_year;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='sale_year', y='total_sales', title='Yearly Sales')
    insight(['Yearly growth validates whether the business is expanding over time.', 'This is a foundational KPI for executive reporting.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '3. GROUP BY — Sales by Country'
    _nlq = 'How much sales amount comes from each country?'
    _sql = '''SELECT country, SUM(sales_amount) AS total_sales FROM sales GROUP BY country ORDER BY total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='country', y='total_sales', title='Sales by Country')
    insight(['USA should dominate because the dataset was designed that way.', 'Country ranking helps prioritize markets and sales strategy.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '4. GROUP BY — Sales by Gender'
    _nlq = 'How much sales amount comes from each gender group?'
    _sql = '''SELECT gender, SUM(sales_amount) AS total_sales FROM sales GROUP BY gender ORDER BY total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='gender', y='total_sales', title='Sales by Gender')
    insight(['A higher female volume should generally lift female revenue.', 'This helps connect demographic skew to business outcomes.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '5. GROUP BY — Sales by Age Group'
    _nlq = 'What is total sales amount by age group?'
    _sql = '''SELECT CASE WHEN age BETWEEN 18 AND 25 THEN '18-25' WHEN age BETWEEN 26 AND 35 THEN '26-35' WHEN age BETWEEN 36 AND 45 THEN '36-45' WHEN age BETWEEN 46 AND 55 THEN '46-55' WHEN age BETWEEN 56 AND 65 THEN '56-65' ELSE '66-80' END AS age_group, SUM(sales_amount) AS total_sales FROM sales GROUP BY age_group ORDER BY age_group;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='age_group', y='total_sales', title='Sales by Age Group')
    insight(['Age segmentation reveals which customer bands generate the most revenue.', 'This can guide marketing and product positioning.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '6. GROUP BY — Transactions by Product'
    _nlq = 'How many transactions are there for each product?'
    _sql = '''SELECT product_name, COUNT(*) AS txn_count FROM sales GROUP BY product_name ORDER BY txn_count DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='product_name', y='txn_count', title='Transactions by Product')
    insight(['This reveals volume leaders, not necessarily revenue leaders.', 'High-frequency products are operationally important.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '7. GROUP BY — Revenue by Product'
    _nlq = 'What is total sales amount by product?'
    _sql = '''SELECT product_name, SUM(sales_amount) AS total_sales FROM sales GROUP BY product_name ORDER BY total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='product_name', y='total_sales', title='Revenue by Product')
    insight(['Premium categories may lead revenue even if their transaction count is lower.', 'This helps compare frequency versus financial impact.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '8. GROUP BY — Average Discount by Sale Type'
    _nlq = 'What is the average discount by sale type?'
    _sql = '''SELECT sale_type, AVG(discount) AS avg_discount FROM sales GROUP BY sale_type ORDER BY avg_discount DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='sale_type', y='avg_discount', title='Average Discount by Sale Type')
    insight(['Online and in-store channels may use promotions differently.', 'Discount behavior helps explain margin differences.'])
    return


@app.cell
def _(insight, run_query, show_query_block):
    _title = '9. GROUP BY — Revenue by Sale Type and Country'
    _nlq = 'What is total sales amount by sale type and country?'
    _sql = '''SELECT country, sale_type, SUM(sales_amount) AS total_sales FROM sales GROUP BY country, sale_type ORDER BY country, total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    insight(['This shows how channel mix varies by market.', 'It helps identify countries where online or in-store dominates value creation.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '10. GROUP BY — Average Basket Value by Country'
    _nlq = 'What is the average sales amount per transaction by country?'
    _sql = '''SELECT country, AVG(sales_amount) AS avg_sales_amount FROM sales GROUP BY country ORDER BY avg_sales_amount DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='country', y='avg_sales_amount', title='Average Basket Value by Country')
    insight(['A smaller market can still have a larger average basket.', 'This helps separate volume from transaction quality.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '11. Top-N — Top 5 Most Expensive Transactions'
    _nlq = 'What are the top 5 most expensive transactions by sales amount?'
    _sql = '''SELECT transaction_id, transaction_date, product_name, country, sales_amount FROM sales ORDER BY sales_amount DESC LIMIT 5;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='transaction_id', y='sales_amount', title='Top 5 Transactions by Sales Amount')
    insight(['These transactions show the extreme upper tail of the dataset.', 'High-ticket orders often come from expensive products and larger quantities.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '12. Top-N — Top 5 Products by Revenue'
    _nlq = 'Which are the top 5 products by total sales amount?'
    _sql = '''SELECT product_name, SUM(sales_amount) AS total_sales FROM sales GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='product_name', y='total_sales', title='Top 5 Products by Revenue')
    insight(['Top revenue products deserve close planning and forecasting attention.', 'This is a high-value product ranking KPI.'])
    return


@app.cell
def _(insight, run_query, show_query_block):
    _title = '13. Top-N — Top 3 Countries per Year by Revenue'
    _nlq = 'For each year, what are the top 3 countries by revenue?'
    _sql = '''SELECT sale_year, country, total_sales FROM ( SELECT EXTRACT(YEAR FROM transaction_date) AS sale_year, country, SUM(sales_amount) AS total_sales, ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM transaction_date) ORDER BY SUM(sales_amount) DESC) AS rn FROM sales GROUP BY sale_year, country ) t WHERE rn <= 3 ORDER BY sale_year, total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    insight(['This shows whether the same countries dominate every year.', 'Per-group top-N queries are essential for dimensional analytics.'])
    return


@app.cell
def _(insight, run_query, show_query_block):
    _title = '14. Top-N — Top 2 Products per Country by Transaction Count'
    _nlq = 'For each country, what are the top 2 products by transaction count?'
    _sql = '''SELECT country, product_name, txn_count FROM ( SELECT country, product_name, COUNT(*) AS txn_count, ROW_NUMBER() OVER (PARTITION BY country ORDER BY COUNT(*) DESC) AS rn FROM sales GROUP BY country, product_name ) t WHERE rn <= 2 ORDER BY country, txn_count DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    insight(['Different markets often prefer different products.', 'This helps tailor local assortment and promotions.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '15. Top-N — Top 5 Months by Revenue'
    _nlq = 'What are the top 5 months by revenue across the dataset?'
    _sql = '''SELECT EXTRACT(MONTH FROM transaction_date) AS sale_month, SUM(sales_amount) AS total_sales FROM sales GROUP BY sale_month ORDER BY total_sales DESC LIMIT 5;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='sale_month', y='total_sales', title='Top 5 Months by Revenue')
    insight(['Best-performing months are useful for promotion timing and inventory planning.', 'This highlights seasonality from a revenue perspective.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '16. Business Query — Revenue by Price Band'
    _nlq = 'How is revenue distributed across price bands?'
    _sql = '''SELECT CASE WHEN price < 100 THEN 'Under 100' WHEN price < 500 THEN '100-499' WHEN price < 1000 THEN '500-999' WHEN price < 2000 THEN '1000-1999' ELSE '2000+' END AS price_band, SUM(sales_amount) AS total_sales FROM sales GROUP BY price_band ORDER BY total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='price_band', y='total_sales', title='Revenue by Price Band')
    insight(['Price-band analysis shows whether the business is volume-driven or premium-driven.', 'It can help frame assortment and positioning strategy.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '17. Business Query — Revenue by Quantity'
    _nlq = 'What is the total sales amount by quantity purchased?'
    _sql = '''SELECT quantity, SUM(sales_amount) AS total_sales FROM sales GROUP BY quantity ORDER BY quantity;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='quantity', y='total_sales', title='Revenue by Quantity')
    insight(['Higher-quantity orders may contribute outsized revenue.', 'This helps understand order-size behavior and bundling opportunities.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '18. Business Query — Average Discount by Product'
    _nlq = 'Which products receive the highest average discount?'
    _sql = '''SELECT product_name, AVG(discount) AS avg_discount FROM sales GROUP BY product_name ORDER BY avg_discount DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='bar', x='product_name', y='avg_discount', title='Average Discount by Product')
    insight(['Some categories may rely more heavily on discounting to drive demand.', 'This can prompt margin and promotion review.'])
    return


@app.cell
def _(insight, run_query, show_query_block):
    _title = '19. Business Query — Revenue by Country and Gender'
    _nlq = 'How much revenue comes from each country-gender combination?'
    _sql = '''SELECT country, gender, SUM(sales_amount) AS total_sales FROM sales GROUP BY country, gender ORDER BY country, total_sales DESC;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    insight(['This combines demographic and geographic slices for richer segmentation.', 'It can reveal market-specific customer composition.'])
    return


@app.cell
def _(insight, plot_result, run_query, show_query_block):
    _title = '20. Business Query — Monthly Sales for 2026 Q1'
    _nlq = 'How do sales trend across January, February, and March of 2026?'
    _sql = '''SELECT EXTRACT(MONTH FROM transaction_date) AS sale_month, SUM(sales_amount) AS total_sales FROM sales WHERE EXTRACT(YEAR FROM transaction_date) = 2026 GROUP BY sale_month ORDER BY sale_month;'''
    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)
    plot_result(_df, kind='line', x='sale_month', y='total_sales', title='2026 Q1 Sales Trend')
    insight(['This isolates the intentionally partial-year 2026 file.', 'Short-window time analysis is useful for quarter-level business monitoring.'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 21. Pie Chart — Revenue Share by Product"
    ### What percentage of total revenue comes from each product?
    """)
    return


@app.cell
def _(insight, plt, run_query, show_query_block):
    _title = "21. Pie Chart — Revenue Share by Product"
    _nlq = "What percentage of total revenue comes from each product?"

    _sql = """
    SELECT 
        product_name,
        SUM(sales_amount) AS total_sales
    FROM sales
    GROUP BY product_name
    ORDER BY total_sales DESC;
    """

    show_query_block(_title, _nlq, _sql)
    _df = run_query(_sql)

    # Pie Chart
    plt.figure(figsize=(6,6))
    plt.pie(
        _df["total_sales"],
        labels=_df["product_name"],
        autopct='%1.1f%%'
    )
    plt.title("Revenue Share by Product")
    plt.tight_layout()
    plt.show()

    insight([
        "This shows which products dominate total revenue contribution.",
        "If a few products take most of the share, the business is highly concentrated."
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Cell 22 — Revenue Share by Country
    ### What percentage of total revenue comes from each country?
    """)
    return


if __name__ == "__main__":
    app.run()
