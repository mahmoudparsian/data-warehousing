import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


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

    def show(title, reason):
        display(Markdown(f"## {title}"))
        display(Markdown(f"**Why this matters:** {reason}"))

    def run(sql):
        display(Markdown(f"```sql\n{sql}\n```"))
        df = con.execute(sql).df()
        display(df.head(20))
        return df

    def bar(df, x, y, title):
        plt.figure(figsize=(10,4))
        plt.bar(df[x].astype(str), df[y]); plt.title(title); plt.xlabel(x); plt.ylabel(y)
        plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()

    def line(df, x, y, title):
        plt.figure(figsize=(10,4))
        plt.plot(df[x].astype(str), df[y], marker='o'); plt.title(title); plt.xlabel(x); plt.ylabel(y)
        plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()

    def hist(df, x, title, bins=30):
        plt.figure(figsize=(8,4))
        plt.hist(df[x], bins=bins); plt.title(title); plt.xlabel(x); plt.ylabel("count")
        plt.tight_layout(); plt.show()

    print(con.execute("SELECT COUNT(*) AS total_rows FROM sales").df())
    return bar, hist, line, run, show


@app.cell
def _(run, show):
    show('Dataset shape and schema', 'We verify row counts and structure before trusting analysis.')
    _df = run('''SELECT COUNT(*) AS total_rows FROM sales;''')
    return


@app.cell
def _(run, show):
    show('Data sample', 'A sample confirms realism and value domains.')
    _df = run('''SELECT * FROM sales LIMIT 15;''')
    return


@app.cell
def _(bar, run, show):
    show('Transactions by year', 'Yearly volume validates intended growth pattern.')
    _df = run('''SELECT EXTRACT(YEAR FROM transaction_date) AS sale_year, COUNT(*) AS txn_count FROM sales GROUP BY sale_year ORDER BY sale_year;''')
    bar(_df, 'sale_year', 'txn_count', 'Transactions by Year')
    return


@app.cell
def _(bar, run, show):
    show('Revenue by year', 'Revenue trend shows business growth over time.')
    _df = run('''SELECT EXTRACT(YEAR FROM transaction_date) AS sale_year, SUM(sales_amount) AS total_sales FROM sales GROUP BY sale_year ORDER BY sale_year;''')
    bar(_df, 'sale_year', 'total_sales', 'Revenue by Year')
    return


@app.cell
def _(line, run, show):
    show('Transactions by month', 'Monthly analysis reveals seasonality and the special Q1 shape of 2026.')
    _df = run('''SELECT EXTRACT(MONTH FROM transaction_date) AS sale_month, COUNT(*) AS txn_count FROM sales GROUP BY sale_month ORDER BY sale_month;''')
    line(_df, 'sale_month', 'txn_count', 'Transactions by Month')
    return


@app.cell
def _(bar, run, show):
    show('Revenue by country', 'Country-level revenue identifies strongest markets.')
    _df = run('''SELECT country, SUM(sales_amount) AS total_sales FROM sales GROUP BY country ORDER BY total_sales DESC;''')
    bar(_df, 'country', 'total_sales', 'Revenue by Country')
    return


@app.cell
def _(bar, run, show):
    show('Transactions by sale type', 'Channel mix explains online versus in-store behavior.')
    _df = run('''SELECT sale_type, COUNT(*) AS txn_count FROM sales GROUP BY sale_type ORDER BY txn_count DESC;''')
    bar(_df, 'sale_type', 'txn_count', 'Transactions by Sale Type')
    return


@app.cell
def _(bar, run, show):
    show('Revenue by product', 'Product-level sales show category leaders.')
    _df = run('''SELECT product_name, SUM(sales_amount) AS total_sales FROM sales GROUP BY product_name ORDER BY total_sales DESC;''')
    bar(_df, 'product_name', 'total_sales', 'Revenue by Product')
    return


@app.cell
def _(bar, run, show):
    show('Average price by product', 'Average price distinguishes premium from low-cost products.')
    _df = run('''SELECT product_name, AVG(price) AS avg_price FROM sales GROUP BY product_name ORDER BY avg_price DESC;''')
    bar(_df, 'product_name', 'avg_price', 'Average Price by Product')
    return


@app.cell
def _(bar, run, show):
    show('Gender distribution', 'This confirms the intended 5:3 skew.')
    _df = run('''SELECT gender, COUNT(*) AS txn_count FROM sales GROUP BY gender ORDER BY txn_count DESC;''')
    bar(_df, 'gender', 'txn_count', 'Transactions by Gender')
    return


@app.cell
def _(hist, run, show):
    show('Age distribution', 'Age spread supports segmentation thinking.')
    _df = run('''SELECT age FROM sales;''')
    hist(_df, 'age', 'Age Distribution')
    return


@app.cell
def _(hist, run, show):
    show('Discount distribution', 'Discounting affects profitability and promotion analysis.')
    _df = run('''SELECT discount FROM sales;''')
    hist(_df, 'discount', 'Discount Distribution')
    return


if __name__ == "__main__":
    app.run()
