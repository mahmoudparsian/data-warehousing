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
    # 🦆 DuckDB GROUP BY Tutorial
    ## Teaching Notebook with Visualizations
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

    con = duckdb.connect()
    return con, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create Table and Insert Data
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE scores(country VARCHAR, team VARCHAR, score INTEGER);
    """).fetchall()

    con.execute("""
    INSERT INTO scores VALUES
    ('USA','RED',10),('USA','RED',20),('USA','RED',30),
    ('USA','BLUE',20),('USA','BLUE',40),('USA','BLUE',70),
    ('CANADA','RED',30),('CANADA','RED',60),('CANADA','RED',80),
    ('CANADA','BLUE',10),('CANADA','BLUE',40),('CANADA','BLUE',90),
    ('GERMANY','RED',20),('GERMANY','RED',40),
    ('GERMANY','BLUE',30),('GERMANY','BLUE',70);
    """).fetchall()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # View All rows:
    """)
    return


@app.cell
def _(con):
    con.execute("SELECT * FROM scores").df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY Country — Total Score
    """)
    return


@app.cell
def _(con):
    df_country = con.execute("""
    SELECT country, SUM(score) AS total_score
    FROM scores
    GROUP BY country
    ORDER BY total_score DESC
    """).df()

    df_country
    return (df_country,)


@app.cell
def _(df_country, plt):
    plt.figure()
    plt.bar(df_country['country'], df_country['total_score'])
    plt.title("Total Score by Country")
    plt.xlabel("Country")
    plt.ylabel("Total Score")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY Team — Total Score
    """)
    return


@app.cell
def _(con):
    df_team = con.execute("""
    SELECT team, SUM(score) AS total_score
    FROM scores
    GROUP BY team
    """).df()

    df_team
    return (df_team,)


@app.cell
def _(df_team, plt):
    plt.figure()
    plt.bar(df_team['team'], df_team['total_score'])
    plt.title("Total Score by Team")
    plt.xlabel("Team")
    plt.ylabel("Total Score")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY Country + Team
    """)
    return


@app.cell
def _(con):
    df_ct = con.execute("""
    SELECT country, team, SUM(score) AS total_score
    FROM scores
    GROUP BY country, team
    ORDER BY country, team
    """).df()

    df_ct
    return (df_ct,)


@app.cell
def _(df_ct, plt):
    pivot = df_ct.pivot(index='country', columns='team', values='total_score')

    pivot.plot(kind='bar')
    plt.title("Score by Country and Team")
    plt.xlabel("Country")
    plt.ylabel("Total Score")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY Country — Average Score
    """)
    return


@app.cell
def _(con):
    df_avg = con.execute("""
    SELECT country, AVG(score) AS avg_score
    FROM scores
    GROUP BY country
    """).df()

    df_avg
    return (df_avg,)


@app.cell
def _(df_avg, plt):
    plt.figure()
    plt.bar(df_avg['country'], df_avg['avg_score'])
    plt.title("Average Score by Country")
    plt.xlabel("Country")
    plt.ylabel("Average Score")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## GROUP BY Country — Count of Records
    """)
    return


@app.cell
def _(con):
    df_count = con.execute("""
    SELECT country, COUNT(*) AS cnt
    FROM scores
    GROUP BY country
    """).df()

    df_count
    return (df_count,)


@app.cell
def _(df_count, plt):
    plt.figure()
    plt.bar(df_count['country'], df_count['cnt'])
    plt.title("Count of Records by Country")
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
