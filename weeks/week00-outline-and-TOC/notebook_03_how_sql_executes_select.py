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
    # How a SQL Engine Executes a SELECT Query

    You **write** a query in one order, but the engine **reads** it in a different order.
    Once you know that order, many SQL error messages stop being mysterious.

    **Part 1:** the logical order, step by step, on a tiny table.<br>
    **Part 2:** what the engine *really* does: `EXPLAIN` and `EXPLAIN ANALYZE`.

    Everything runs in an in-memory DuckDB database: no data files needed.
    """)
    return


@app.cell
def _(mo):
    import time

    import duckdb

    con = duckdb.connect()  # in-memory database

    def run(sql):
        """Run a query and show its result, or show the error message."""
        try:
            return con.execute(sql).df()
        except duckdb.Error as e:
            return mo.callout(mo.md(f"**{type(e).__name__}**\n\n```text\n{e}\n```"), kind="danger")

    def plan(sql):
        """Return the plan text that EXPLAIN / EXPLAIN ANALYZE produces."""
        return con.execute(sql).fetchall()[0][1]

    return con, plan, run, time


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The data: 6 customers, 11 orders
    """)
    return


@app.cell
def _(con, run):
    con.execute("""
    CREATE OR REPLACE TABLE customers AS
    SELECT * FROM (VALUES
        (1, 'Ana',  'West'),
        (2, 'Ben',  'East'),
        (3, 'Chen', 'West'),
        (4, 'Dee',  'East'),
        (5, 'Eli',  'South'),
        (6, 'Fay',  'North')
    ) AS t(customer_id, name, region);

    CREATE OR REPLACE TABLE orders AS
    SELECT * FROM (VALUES
        (101, 1, 120, 'shipped'),
        (102, 1,  80, 'shipped'),
        (103, 2, 200, 'cancelled'),
        (104, 2, 150, 'shipped'),
        (105, 3,  60, 'shipped'),
        (106, 3,  40, 'shipped'),
        (107, 4, 300, 'shipped'),
        (108, 4,  50, 'cancelled'),
        (109, 1,  90, 'shipped'),
        (110, 5,  30, 'shipped'),
        (111, 6, 200, 'shipped')
    ) AS t(order_id, customer_id, amount, status);
    """)
    run("SELECT * FROM orders")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1 — The logical order

    **The question:** which 2 regions have the most shipped revenue (only regions above \$150)?

    ```sql
    SELECT   c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total   -- 5
    FROM     orders o JOIN customers c                                -- 1
             ON o.customer_id = c.customer_id
    WHERE    o.status = 'shipped'                                     -- 2
    GROUP BY c.region                                                 -- 3
    HAVING   SUM(o.amount) > 150                                      -- 4
    ORDER BY total DESC                                               -- 6
    LIMIT    2;                                                       -- 7
    ```

    | Step | Clause | What it does | Think of it as |
    |:---:|---|---|---|
    | 1 | `FROM` / `JOIN` | find the rows, combine the tables | *get the ingredients* |
    | 2 | `WHERE` | keep only the rows you want | *throw away bad ingredients* |
    | 3 | `GROUP BY` | put rows into groups, compute `COUNT`, `SUM`, … | *sort into bowls* |
    | 4 | `HAVING` | keep only the groups you want | *throw away whole bowls* |
    | 5 | `SELECT` | pick and name the output columns (aliases are born here) | *plate the dish* |
    | 6 | `ORDER BY` | sort the result | *line up the plates* |
    | 7 | `LIMIT` | keep the first *n* rows | *serve the first two* |

    > `SELECT` is written **first** but runs **fifth**. That one fact explains most of this notebook.

    Let's run the query one step at a time and look at the table after each step.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 1 — `FROM` + `JOIN`: 11 rows

    Every order is matched with its customer. Nothing is filtered yet.
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT o.order_id, o.amount, o.status, c.name, c.region
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    ORDER BY o.order_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2 — `WHERE`: 9 rows

    The 2 cancelled orders (103 and 108) are gone. `WHERE` looks at **one row at a time**.
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT o.order_id, o.amount, o.status, c.name, c.region
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'shipped'
    ORDER BY o.order_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 3 — `GROUP BY`: 9 rows become 4 groups

    Each region becomes **one row**. `LIST(...)` shows which amounts landed in each group;
    `COUNT` and `SUM` are computed from those lists.
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT c.region,
           LIST(o.amount ORDER BY o.order_id) AS amounts_in_group,
           COUNT(*)      AS n_orders,
           SUM(o.amount) AS total
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'shipped'
    GROUP BY c.region
    ORDER BY c.region
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 4 — `HAVING`: 3 groups left

    South (\$30) is removed. `HAVING` looks at **one group at a time**, so it can use `SUM(...)`.
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'shipped'
    GROUP BY c.region
    HAVING SUM(o.amount) > 150
    ORDER BY c.region
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Steps 5–7 — `SELECT`, `ORDER BY`, `LIMIT`: the final answer

    `SELECT` names the columns (`n_orders`, `total`), `ORDER BY total DESC` sorts by the new name
    (it runs *after* `SELECT`, so the alias exists), and `LIMIT 2` keeps East (\$450) and West (\$390). North (\$200) is cut.
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT   c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total
    FROM     orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE    o.status = 'shipped'
    GROUP BY c.region
    HAVING   SUM(o.amount) > 150
    ORDER BY total DESC
    LIMIT    2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Row count at each step:** 11 → 9 → 4 groups → 3 → 3 → 3 → **2**.

    ## What the order explains

    ### ❌ An aggregate in `WHERE`

    `WHERE` (step 2) runs **before** the groups exist (step 3), so there is no `SUM` to compare yet.
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT c.region, SUM(o.amount) AS total
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE SUM(o.amount) > 150
    GROUP BY c.region
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Fix:** filter groups in `HAVING` (step 4), as in the query above.
    Rule of thumb: **row condition → `WHERE`; group condition → `HAVING`.**

    ### ❌ A column that is neither grouped nor aggregated

    After step 3 there is one row per region. A region has several customer names: which one should the engine show?
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT c.region, c.name, SUM(o.amount) AS total
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.region
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Fix:** add `c.name` to `GROUP BY` (one row per region *and* name), or aggregate it, e.g. `STRING_AGG(c.name, ', ')`.

    ### ⚠️ A `SELECT` alias in `WHERE`: DuckDB is friendly, standard SQL is not

    By the logical order, `amount_x2` doesn't exist yet in step 2. **PostgreSQL, MySQL and SQL Server reject this query.**
    DuckDB accepts it as a convenience (it copies the expression `o.amount * 2` into `WHERE` for you):
    """)
    return


@app.cell
def _(run):
    run("""
    SELECT o.order_id, o.amount * 2 AS amount_x2
    FROM orders o
    WHERE amount_x2 > 300
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For portable SQL, repeat the expression (`WHERE o.amount * 2 > 300`) or compute it first in a CTE.

    ---

    ## Part 2 — What the engine *really* does

    The logical order defines **what** the answer is. It is not a recipe the engine must follow.
    The **optimizer** chooses a **physical plan**: any sequence of operations that gives the *same answer*, as fast as possible.
    For example, it reads only the columns the query needs, and it applies `WHERE` while reading the table.

    You can look at that plan:

    | | `EXPLAIN <query>` | `EXPLAIN ANALYZE <query>` |
    |---|---|---|
    | Runs the query? | **No**: it only plans | **Yes**: it plans *and* runs |
    | Row counts | **estimates** (`~5 rows`) | **actual** (`5 rows`) |
    | Time per step | no | **yes** |
    | Speed | instant, even on a huge table | as slow as the query itself |
    | Use it to… | see the plan of an expensive query safely | find which step is slow; check the estimates |

    **Read a plan from the bottom up:** the table scans are at the bottom, and each box feeds the box above it.
    The final result comes out of the top box.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `EXPLAIN`: our query's plan (nothing is run)
    """)
    return


@app.cell
def _(mo, plan):
    question = """
    SELECT   c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total
    FROM     orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE    o.status = 'shipped'
    GROUP BY c.region
    HAVING   SUM(o.amount) > 150
    ORDER BY total DESC
    LIMIT    2
    """
    mo.plain_text(plan("EXPLAIN " + question))
    return (question,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **How to read it (bottom → top), next to the logical order:**

    | Box in the plan | Logical step | What the optimizer did |
    |---|---|---|
    | 2 × **Seq Scan** (*Table Scan* in `EXPLAIN ANALYZE`): `customers`, `orders` | 1 `FROM` | reads only the columns it needs (`Projections:`): no `name`, no `order_id` |
    | `Filters: status = 'shipped'` *inside* the `orders` scan | 2 `WHERE` | **filter pushdown**: cancelled rows are dropped while reading, before the join |
    | **Hash Join** | 1 `JOIN` | builds a hash table on one side and probes it with the other side |
    | **Hash Group By** | 3 `GROUP BY` | one bucket per region; `count_star()` and `sum(#…)` are computed per bucket |
    | **Filter** `sum(...) > 150` | 4 `HAVING` | runs on the groups, as expected |
    | **Top N** (`Top: 2`, `Order By: total DESC`) | 6 + 7 | `ORDER BY` + `LIMIT` merged: it keeps only the 2 best rows instead of sorting everything |

    Boxes named **Projection** pick or rename columns (step 5). The `__internal_compress…` / `__internal_decompress…`
    projections are DuckDB tricks to make the group-by faster: ignore them.

    So the engine **did not** do "join everything, then filter": it filtered first. Same answer, less work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `EXPLAIN ANALYZE`: the same query, actually run

    Now each box shows the **actual** number of rows that came out of it (no `~`) and the time it took.
    Check them against Part 1: the join gives **9** rows (the cancelled orders were already gone),
    the group-by gives **4**, `HAVING` keeps **3**, and the Top N returns **2**.
Compare with the `EXPLAIN` estimates above: `~6` rows out of the join and `~0` out of `HAVING`.
Estimates are guesses; `EXPLAIN ANALYZE` shows the truth.
    """)
    return


@app.cell
def _(mo, plan, question):
    mo.plain_text(plan("EXPLAIN ANALYZE " + question))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The difference matters on big tables

    A table with **5,000,000** rows. `EXPLAIN` only plans; `EXPLAIN ANALYZE` really reads the 5 million rows.
    """)
    return


@app.cell
def _(con):
    con.execute("""
    CREATE OR REPLACE TABLE big_sales AS
    SELECT i                                            AS sale_id,
           ['West', 'East', 'South', 'North'][i % 4 + 1] AS region,
           (i * 7919 % 1000)::DOUBLE                    AS amount
    FROM range(5000000) AS r(i)
    """)
    con.execute("SELECT COUNT(*) AS n_rows FROM big_sales").df()
    return


@app.cell
def _(con, mo, time):
    big_query = "SELECT region, SUM(amount) AS total FROM big_sales GROUP BY region"

    def seconds(sql):
        _t0 = time.perf_counter()
        con.execute(sql).fetchall()
        return time.perf_counter() - _t0

    t_explain = seconds("EXPLAIN " + big_query)
    t_analyze = seconds("EXPLAIN ANALYZE " + big_query)
    mo.md(f"""
    | Command | Time on this computer |
    |---|---|
    | `EXPLAIN` | {t_explain * 1000:.2f} ms |
    | `EXPLAIN ANALYZE` | {t_analyze * 1000:.2f} ms (≈ {t_analyze / t_explain:.0f}× longer) |

    Your numbers will differ: `EXPLAIN` stays near zero whatever the table size, while `EXPLAIN ANALYZE` grows with the data.
    """)
    return (big_query,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The optimizer rewrites your query: `WHERE` vs `HAVING` on a grouping column

    These two queries give the same answer. Logically, the first filters rows **before** grouping and the second filters groups **after** grouping.
    The optimizer sees that `region = 'West'` can be checked on each row, so it gives both queries **the same plan**:
    """)
    return


@app.cell
def _(mo, plan):
    plan_where = plan("EXPLAIN SELECT region, SUM(amount) FROM big_sales WHERE region = 'West' GROUP BY region")
    plan_having = plan("EXPLAIN SELECT region, SUM(amount) FROM big_sales GROUP BY region HAVING region = 'West'")
    mo.vstack([
        mo.md(f"**Identical plans?** `{plan_where == plan_having}`"),
        mo.plain_text(plan_having),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the `Seq Scan` box: `Filters: region = 'West'` was moved all the way down into the scan, and only
    `~1,250,000` of the 5,000,000 rows are expected to come out of it.
    Still, **write it in `WHERE`**: it states your intent, and not every database is this smart.

    ### ⚠️ `EXPLAIN ANALYZE` really runs the statement

    That includes `DELETE`, `UPDATE`, `INSERT` and `CREATE TABLE … AS`. Use plain `EXPLAIN` to look at the plan of a change without making it:
    """)
    return


@app.cell
def _(con, mo):
    con.execute("CREATE OR REPLACE TABLE scratch AS SELECT * FROM range(10) AS r(i)")
    _counts = []
    for _cmd in ["EXPLAIN DELETE FROM scratch WHERE i < 5",
                 "EXPLAIN ANALYZE DELETE FROM scratch WHERE i < 5"]:
        con.execute(_cmd).fetchall()
        _left = con.execute("SELECT COUNT(*) FROM scratch").fetchall()[0][0]
        _counts.append(f"| `{_cmd}` | {_left} |")
    mo.md("| Command (table starts with 10 rows) | Rows left afterwards |\n|---|---|\n" + "\n".join(_counts))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Check yourself
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "1. You need the regions whose AVERAGE order is above \\$100. WHERE or HAVING? Why?":
            mo.md("`HAVING AVG(amount) > 100`: an average belongs to a **group**, and groups only exist after step 3. `WHERE` runs at step 2, one row at a time."),
        "2. Why can ORDER BY use the alias `total`, while standard SQL rejects it in WHERE?":
            mo.md("`ORDER BY` runs at step 6, **after** `SELECT` (step 5) created the alias. `WHERE` runs at step 2, before it exists. (DuckDB lets you use it in `WHERE` anyway; PostgreSQL and MySQL don't.)"),
        "3. Does LIMIT 2 run before or after ORDER BY? What would go wrong otherwise?":
            mo.md("**After.** If `LIMIT` ran first, you would get 2 arbitrary rows and then sort them: not the top 2. In the plan both are merged into one **Top N** box."),
        "4. One plan box says `~1,250,000 rows`, another says `1,250,000 rows`. What's the difference?":
            mo.md("The `~` means **estimate** (`EXPLAIN`: nothing was run). Without `~` it is the **actual** count (`EXPLAIN ANALYZE`). A big gap between the two tells you the optimizer guessed wrong."),
        "5. You want to see how a big DELETE will run, without deleting anything. Which command?":
            mo.md("`EXPLAIN DELETE …`. `EXPLAIN ANALYZE DELETE …` would really delete the rows."),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📌 Cheat sheet

    ```text
    Written order:   SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
    Logical order:   FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
                     (rows)      (rows)  (groups)   (groups)  (columns) (sort)    (cut)
    ```

    - **`WHERE` filters rows, `HAVING` filters groups.** Aggregates are not allowed in `WHERE`.
    - Aliases are born in `SELECT`: safe in `ORDER BY`; in `WHERE` / `GROUP BY` only in friendly engines like DuckDB.
    - The logical order defines the **answer**; the optimizer picks the **physical plan** (pushdown, Top N, …).
    - **`EXPLAIN`** = the plan, with estimated rows, nothing runs. **`EXPLAIN ANALYZE`** = runs it: actual rows + time.
      Read plans **bottom-up**.
    - The same commands work in the DuckDB CLI and in qStudio: `EXPLAIN SELECT …;`
    """)
    return


if __name__ == "__main__":
    app.run()
