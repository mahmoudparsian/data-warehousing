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
    # LIMIT vs RANK: Know the Difference

    When ties exist in your data, `LIMIT` and `RANK()` behave **very differently**.

    | Approach | Behavior with ties |
    |---|---|
    | `LIMIT 2` | Always returns exactly 2 rows — ties are silently dropped |
    | `RANK() <= 2` | Returns **all** rows that share the top 2 ranking positions |
    """)
    return


@app.cell
def _():
    import duckdb

    con = duckdb.connect()

    con
    return (con,)


@app.cell
def _(con):
    # Create a sales table — notice three countries are TIED at 700
    con.execute("""
        CREATE OR REPLACE TABLE sales (
            country  VARCHAR,
            revenue  INTEGER
        )
    """).fetchall()

    con.execute("""
        INSERT INTO sales VALUES
            ('USA',     800),
            ('CANADA',  700),
            ('ITALY',   700),
            ('GERMANY', 700),
            ('MEXICO',  500),
            ('FRANCE',  400)
    """).fetchall()

    print("--- Full table scan ---")
    con.sql("""
    SELECT * 
    FROM sales 
    ORDER BY revenue DESC
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Approach 1: `LIMIT 2`

    Returns **exactly 2 rows** — it has no concept of ties.
    CANADA, ITALY, and GERMANY all have 700, but only **one** of them appears.
    Which one? It's **arbitrary** — DuckDB makes no guarantee.
    """)
    return


@app.cell
def _(con):
    print("--- LIMIT 2: always returns exactly 2 rows ---")
    print("--- Ties at 700 are SILENTLY IGNORED ---\n")

    con.sql("""
        SELECT country, revenue
        FROM sales
        ORDER BY revenue DESC
        LIMIT 2
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Approach 2: `RANK()` with `rnk <= 2`

    RANK assigns the **same rank** to tied values.
    All three countries at 700 share **rank 2**, so filtering `rnk <= 2` returns **4 rows**, not 2.

    ```
    USA      800  →  rank 1  }
    CANADA   700  →  rank 2  }
    ITALY    700  →  rank 2  }  all included!
    GERMANY  700  →  rank 2  }
    MEXICO   500  →  rank 5  ←  skipped (rank > 2)
    FRANCE   400  →  rank 6  ←  skipped (rank > 2)
    ```
    """)
    return


@app.cell
def _(con):
    print("--- RANK: first, let's see ranks for ALL rows ---\n")

    con.sql("""
        SELECT country,
               revenue,
               RANK() OVER (ORDER BY revenue DESC) AS rnk
        FROM sales
        ORDER BY rnk
    """).show()
    return


@app.cell
def _(con):
    print("--- RANK with rnk <= 2: returns 4 rows (all ties included) ---\n")

    con.sql("""
        SELECT country, 
               revenue, 
               rnk
        FROM (
            SELECT country,
                   revenue,
                   RANK() OVER (ORDER BY revenue DESC) AS rnk
            FROM sales
        )
        WHERE rnk <= 2
        ORDER BY rnk, country
    """).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Side-by-Side Summary

    | | `LIMIT 2` | `RANK() <= 2` |
    |---|---|---|
    | Rows returned | Always **2** | **4** (1 at rank 1 + 3 tied at rank 2) |
    | Handles ties? | No — arbitrary cutoff | Yes — all ties included |
    | Use case | Pagination, sampling | Top-N analysis where fairness matters |
    """)
    return


@app.cell
def _(con):
    # Bonus: DENSE_RANK vs RANK
    # DENSE_RANK doesn't skip numbers after ties
    print("--- Bonus: RANK vs DENSE_RANK ---\n")

    con.sql("""
        SELECT country,
               revenue,
               RANK()       OVER (ORDER BY revenue DESC) AS rank,
               DENSE_RANK() OVER (ORDER BY revenue DESC) AS dense_rank
        FROM sales
        ORDER BY revenue DESC
    """).show()

    print("Notice: RANK skips 3,4 after the tie → jumps to 5")
    print("        DENSE_RANK doesn't skip     → goes to 3")
    return


@app.cell
def _(con):
    con.close()
    print("Done!")
    return


if __name__ == "__main__":
    app.run()
