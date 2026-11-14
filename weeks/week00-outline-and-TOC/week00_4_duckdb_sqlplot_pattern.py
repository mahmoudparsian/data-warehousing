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
    # DuckDB SQL → Plot Pattern (Clean Teaching Version)

    Pattern used throughout:
    1) Write SQL
    2) Execute via DuckDB
    3) Visualize with a small helper

    This avoids magic commands and keeps focus on **SQL → Insight**.
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
    import matplotlib.pyplot as plt

    con = duckdb.connect()

    # Load CSV (make sure insurance.csv is in your working directory)
    con.execute("""
    CREATE OR REPLACE TABLE insurance AS
    SELECT * FROM read_csv_auto('../week01-Foundations-SQL-for-Analytics/example_1_insurance/insurance.csv');
    """).fetchall()

    con.execute("SELECT * FROM insurance LIMIT 5").df()
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Helper: sqlplot(query, kind)

    A tiny wrapper so students stay SQL-first.
    No colors specified (matplotlib default).
    """)
    return


@app.cell
def _(con, plt):
    def sqlplot(query, kind="bar", x=None, y=None, bins=20):
        df = con.execute(query).df()
        plt.figure()

        # -----------------------
        # BAR
        # -----------------------
        if kind == "bar":
            if x is None or y is None:
                x, y = df.columns[0], df.columns[1]
            plt.bar(df[x], df[y])
            plt.xlabel(x)
            plt.ylabel(y)

        # -----------------------
        # HORIZONTAL BAR (better labels)
        # -----------------------
        elif kind == "barh":
            if x is None or y is None:
                x, y = df.columns[1], df.columns[0]
            plt.barh(df[y], df[x])
            plt.xlabel(x)
            plt.ylabel(y)

        # -----------------------
        # HISTOGRAM
        # -----------------------
        elif kind == "hist":
            col = x if x else df.columns[0]
            plt.hist(df[col], bins=bins)
            plt.xlabel(col)
            plt.ylabel("count")

        # -----------------------
        # SCATTER
        # -----------------------
        elif kind == "scatter":
            if x is None or y is None:
                x, y = df.columns[0], df.columns[1]
            plt.scatter(df[x], df[y])
            plt.xlabel(x)
            plt.ylabel(y)

        # -----------------------
        # LINE (time series)
        # -----------------------
        elif kind == "line":
            if x is None or y is None:
                x, y = df.columns[0], df.columns[1]
            plt.plot(df[x], df[y])
            plt.xlabel(x)
            plt.ylabel(y)

        # -----------------------
        # PIE (proportion)
        # -----------------------
        elif kind == "pie":
            if x is None or y is None:
                x, y = df.columns[0], df.columns[1]
            plt.pie(df[y], labels=df[x], autopct='%1.1f%%')
            plt.title("Distribution")

        # -----------------------
        # BOX (distribution insight)
        # -----------------------
        elif kind == "box":
            col = x if x else df.columns[0]
            plt.boxplot(df[col])
            plt.ylabel(col)

        else:
            raise ValueError("Unsupported kind")

        plt.title("Result")
        plt.tight_layout()
        plt.show()

    return (sqlplot,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1) Distribution of Charges

    **Business question:** How are costs distributed?

    **SQL:** select raw values to inspect distribution.
    """)
    return


@app.cell
def _(sqlplot):
    _query = """
    SELECT charges
    FROM insurance
    """
    sqlplot(_query, kind="hist", x="charges", bins=20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    query = \"\"\"
    SELECT charges
    FROM insurance
    \"\"\"
    sqlplot(query, kind="pie", x="charges", bins=20)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2) Charges by Smoker

    **Business question:** Do smokers cost more?

    **SQL pattern:** aggregation (GROUP BY).
    """)
    return


@app.cell
def _(sqlplot):
    _query = """
    SELECT smoker, AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY smoker
    """
    sqlplot(_query, kind="bar", x="smoker", y="avg_charges")
    return


@app.cell
def _(sqlplot):
    # Smoker Distribution
    # What percentage of customers are smokers vs non-smokers?

    # Business Insight
    #	•	Shows population composition
    #	•	Typically:
    #	•	non-smokers dominate
    #	•	smokers are a smaller segment

    sqlplot("""
    SELECT smoker, COUNT(*) AS cnt
    FROM insurance
    GROUP BY smoker
    """, kind="pie")
    return


@app.cell
def _(sqlplot):
    #  Revenue Share by Smoker
    # Deeper Insight
    #	•	now pie shows financial impact, not population
    #	•	smokers may:
    #	•	   be fewer
    #	•	   but contribute disproportionately to total cost

    sqlplot("""
    SELECT smoker, SUM(charges) AS total_charges
    FROM insurance
    GROUP BY smoker
    """, kind="pie")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3) Charges by Region

    **Business question:** Which regions are more expensive?

    **SQL pattern:** aggregation by segment.
    """)
    return


@app.cell
def _(sqlplot):
    _query = """
    SELECT region, AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY region
    """
    sqlplot(_query, kind="bar", x="region", y="avg_charges")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4) Age vs Charges

    **Business question:** Does age relate to cost?

    **SQL pattern:** select two columns for relationship.
    """)
    return


@app.cell
def _(sqlplot):
    _query = """
    SELECT age, charges
    FROM insurance
    """
    sqlplot(_query, kind="scatter", x="age", y="charges")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5) BMI vs Charges

    **Business question:** Does BMI relate to cost?
    """)
    return


@app.cell
def _(sqlplot):
    _query = """
    SELECT bmi, charges
    FROM insurance
    """
    sqlplot(_query, kind="scatter", x="bmi", y="charges")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6) Children vs Charges

    **Business question:** Does family size affect cost?

    **SQL pattern:** aggregation by discrete group.
    """)
    return


@app.cell
def _(sqlplot):
    _query = """
    SELECT children, AVG(charges) AS avg_charges
    FROM insurance
    GROUP BY children
    """
    sqlplot(_query, kind="bar", x="children", y="avg_charges")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wrap-Up

    Pattern to remember:

    SQL → Result → Plot → Insight → Decision

    Keep visualization simple; focus on the **question and interpretation**.
    """)
    return


if __name__ == "__main__":
    app.run()
