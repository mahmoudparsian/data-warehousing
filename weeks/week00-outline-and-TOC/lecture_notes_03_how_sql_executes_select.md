---
marp: true
paginate: true
theme: default
---

# How a SQL Engine Executes a SELECT Query

**Part 1:** the logical order, step by step
**Part 2:** what the engine *really* does: `EXPLAIN` vs `EXPLAIN ANALYZE`

Notebook version (same data, same numbers): `notebook_03_how_sql_executes_select.py`

---

## You write it in one order, the engine reads it in another

```text
Written order:   SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
Logical order:   FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

> `SELECT` is written **first** but runs **fifth**.
> That one fact explains most of the SQL errors you will meet in this course.

---

<style scoped>table { font-size: 0.75em; }</style>

## The 7 logical steps

| Step | Clause | What it does | Think of it as |
|:---:|---|---|---|
| 1 | `FROM` / `JOIN` | find the rows, combine the tables | *get the ingredients* |
| 2 | `WHERE` | keep only the rows you want | *throw away bad ingredients* |
| 3 | `GROUP BY` | put rows into groups, compute `COUNT`, `SUM`, … | *sort into bowls* |
| 4 | `HAVING` | keep only the groups you want | *throw away whole bowls* |
| 5 | `SELECT` | pick and name the output columns (aliases are born here) | *plate the dish* |
| 6 | `ORDER BY` | sort the result | *line up the plates* |
| 7 | `LIMIT` | keep the first *n* rows | *serve the first two* |

---

<style scoped>pre { font-size: 0.62em; }</style>

## The data: 6 customers, 11 orders

```sql
CREATE OR REPLACE TABLE customers AS
SELECT * FROM (VALUES
    (1, 'Ana', 'West'), (2, 'Ben', 'East'), (3, 'Chen', 'West'),
    (4, 'Dee', 'East'), (5, 'Eli', 'South'), (6, 'Fay', 'North')
) AS t(customer_id, name, region);

CREATE OR REPLACE TABLE orders AS
SELECT * FROM (VALUES
    (101, 1, 120, 'shipped'), (102, 1,  80, 'shipped'), (103, 2, 200, 'cancelled'),
    (104, 2, 150, 'shipped'), (105, 3,  60, 'shipped'), (106, 3,  40, 'shipped'),
    (107, 4, 300, 'shipped'), (108, 4,  50, 'cancelled'), (109, 1,  90, 'shipped'),
    (110, 5,  30, 'shipped'), (111, 6, 200, 'shipped')
) AS t(order_id, customer_id, amount, status);
```

---

## The question

**Which 2 regions have the most shipped revenue (only regions above \$150)?**

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

Let's run it **one step at a time** and look at the table after each step.

---

<style scoped>table { font-size: 0.55em; } pre { font-size: 0.6em; }</style>

## Step 1 — `FROM` + `JOIN`: 11 rows

```sql
SELECT o.order_id, o.amount, o.status, c.name, c.region
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_id;
```

<!-- RESULT -->

| order_id | amount | status    | name | region |
|---------:|-------:|-----------|------|--------|
|      101 |    120 | shipped   | Ana  | West   |
|      102 |     80 | shipped   | Ana  | West   |
|      103 |    200 | cancelled | Ben  | East   |
|      104 |    150 | shipped   | Ben  | East   |
|      105 |     60 | shipped   | Chen | West   |
|      106 |     40 | shipped   | Chen | West   |
|      107 |    300 | shipped   | Dee  | East   |
|      108 |     50 | cancelled | Dee  | East   |
|      109 |     90 | shipped   | Ana  | West   |
|      110 |     30 | shipped   | Eli  | South  |
|      111 |    200 | shipped   | Fay  | North  |

*(11 rows)*

<!-- /RESULT -->

---

<style scoped>table { font-size: 0.55em; } pre { font-size: 0.6em; }</style>

## Step 2 — `WHERE`: 9 rows (one row at a time)

```sql
SELECT o.order_id, o.amount, o.status, c.name, c.region
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'shipped'
ORDER BY o.order_id;
```

<!-- RESULT -->

| order_id | amount | status  | name | region |
|---------:|-------:|---------|------|--------|
|      101 |    120 | shipped | Ana  | West   |
|      102 |     80 | shipped | Ana  | West   |
|      104 |    150 | shipped | Ben  | East   |
|      105 |     60 | shipped | Chen | West   |
|      106 |     40 | shipped | Chen | West   |
|      107 |    300 | shipped | Dee  | East   |
|      109 |     90 | shipped | Ana  | West   |
|      110 |     30 | shipped | Eli  | South  |
|      111 |    200 | shipped | Fay  | North  |

*(9 rows)*

<!-- /RESULT -->

The 2 cancelled orders (103 and 108) are gone.

---

<style scoped>pre { font-size: 0.65em; }</style>

## Step 3 — `GROUP BY`: 9 rows become 4 groups

```sql
SELECT c.region,
       LIST(o.amount ORDER BY o.order_id) AS amounts_in_group,
       COUNT(*)      AS n_orders,
       SUM(o.amount) AS total
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'shipped'
GROUP BY c.region
ORDER BY c.region;
```

<!-- RESULT -->

| region | amounts_in_group      | n_orders | total |
|--------|-----------------------|---------:|------:|
| East   | [150, 300]            |        2 |   450 |
| North  | [200]                 |        1 |   200 |
| South  | [30]                  |        1 |    30 |
| West   | [120, 80, 60, 40, 90] |        5 |   390 |

*(4 rows)*

<!-- /RESULT -->

`LIST(...)` shows which amounts landed in each "bowl".

---

<style scoped>pre { font-size: 0.7em; }</style>

## Step 4 — `HAVING`: 3 groups left (one group at a time)

```sql
SELECT c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'shipped'
GROUP BY c.region
HAVING SUM(o.amount) > 150
ORDER BY c.region;
```

<!-- RESULT -->

| region | n_orders | total |
|--------|---------:|------:|
| East   |        2 |   450 |
| North  |        1 |   200 |
| West   |        5 |   390 |

*(3 rows)*

<!-- /RESULT -->

South (\$30) is removed. `HAVING` sees groups, so it can use `SUM(...)`.

---

<style scoped>pre { font-size: 0.7em; }</style>

## Steps 5–7 — `SELECT`, `ORDER BY`, `LIMIT`

```sql
SELECT   c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total
FROM     orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE    o.status = 'shipped'
GROUP BY c.region
HAVING   SUM(o.amount) > 150
ORDER BY total DESC
LIMIT    2;
```

<!-- RESULT -->

| region | n_orders | total |
|--------|---------:|------:|
| East   |        2 |   450 |
| West   |        5 |   390 |

*(2 rows)*

<!-- /RESULT -->

`ORDER BY total` works: it runs *after* `SELECT` created the alias. North (\$200) is cut by `LIMIT 2`.

---

## Row count at each step

| Step | 1 `FROM`/`JOIN` | 2 `WHERE` | 3 `GROUP BY` | 4 `HAVING` | 5 `SELECT` | 6 `ORDER BY` | 7 `LIMIT` |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Rows | 11 | 9 | 4 groups | 3 | 3 | 3 | **2** |

- `WHERE` filters **rows**; `HAVING` filters **groups**.
- `SELECT` and `ORDER BY` don't remove rows; `LIMIT` does.

---

## ❌ An aggregate in `WHERE`

`WHERE` (step 2) runs **before** the groups exist (step 3):

```sql
SELECT c.region, SUM(o.amount) AS total
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE SUM(o.amount) > 150
GROUP BY c.region;
```

<!-- ERROR -->

```text
Binder Error: WHERE clause cannot contain aggregates!

LINE 3: WHERE SUM(o.amount) > 150
              ^^^^^^^^^^^^^
```

<!-- /ERROR -->

**Fix:** `HAVING SUM(o.amount) > 150`. Row condition → `WHERE`; group condition → `HAVING`.

---

<style scoped>pre { font-size: 0.65em; }</style>

## ❌ A column that is neither grouped nor aggregated

After step 3 there is **one row per region**, but a region has several names: which one?

```sql
SELECT c.region, c.name, SUM(o.amount) AS total
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.region;
```

<!-- ERROR -->

```text
Binder Error: column "name" must appear in the GROUP BY clause or must be part of an aggregate function.
Either add it to the GROUP BY list, or use ANY_VALUE("name") if the exact value of "name" is not important.

LINE 1: SELECT c.region, c.name, SUM(o.amount) AS total
                         ^^^^^^
```

<!-- /ERROR -->

**Fix:** `GROUP BY c.region, c.name`, or aggregate it: `STRING_AGG(c.name, ', ')`.

---

<style scoped>table { font-size: 0.7em; } pre { font-size: 0.75em; } p { margin: 0.4em 0; }</style>

## ⚠️ A `SELECT` alias in `WHERE`

By the logical order, `amount_x2` doesn't exist yet at step 2.
**PostgreSQL, MySQL and SQL Server reject this.** DuckDB accepts it as a convenience:

```sql
SELECT o.order_id, o.amount * 2 AS amount_x2
FROM orders o
WHERE amount_x2 > 300;
```

<!-- RESULT -->

| order_id | amount_x2 |
|---------:|----------:|
|      103 |       400 |
|      107 |       600 |
|      111 |       400 |

*(3 rows)*

<!-- /RESULT -->

For portable SQL: `WHERE o.amount * 2 > 300`, or compute it first in a CTE.

---

# Part 2 — What the engine *really* does

The logical order defines **what** the answer is.
The **optimizer** chooses **how**: a *physical plan*, any sequence of operations that gives
**the same answer**, as fast as possible.

- reads only the columns the query needs
- applies `WHERE` while reading the table (**filter pushdown**)
- merges `ORDER BY` + `LIMIT` into one **Top N** step

---

## `EXPLAIN` vs `EXPLAIN ANALYZE`

| | `EXPLAIN <query>` | `EXPLAIN ANALYZE <query>` |
|---|---|---|
| Runs the query? | **No**: it only plans | **Yes**: it plans *and* runs |
| Row counts | **estimates** (`~6 rows`) | **actual** (`9 rows`) |
| Time per step | no | **yes** |
| Speed | instant, even on a huge table | as slow as the query itself |
| Use it to… | see the plan of an expensive query safely | find the slow step; check the estimates |

**Read a plan bottom-up:** table scans at the bottom; each box feeds the box above it.

---

<style scoped>section{display:grid;grid-template-columns:1fr 1.25fr;grid-template-rows:auto 1fr;column-gap:24px;align-content:start;padding-top:40px} h2{grid-column:1/3;margin-bottom:8px} pre{margin:0;align-self:start} section>pre:nth-of-type(2), section>div:nth-of-type(2) pre{font-size:.34em;line-height:1.05} section>pre:first-of-type{font-size:.5em}</style>

## `EXPLAIN` of our query (nothing runs)

```sql
EXPLAIN
SELECT   c.region, COUNT(*) AS n_orders, SUM(o.amount) AS total
FROM     orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE    o.status = 'shipped'
GROUP BY c.region
HAVING   SUM(o.amount) > 150
ORDER BY total DESC
LIMIT    2;
```

<!-- RESULT -->

```text
╭─ Top N ─────────────────────────────────╮
│ Top: 2                                  │
│ Order By: total DESC                    │
│ ~0 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Projection ───────┴────────────────────╮
│ Projections: region, n_orders, total    │
│ ~0 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Filter ───────────┴────────────────────╮
│ Expression: sum(amount) > 150           │
│ ~0 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Projection ───────┴────────────────────╮
│ Projections:                            │
│ __internal_decompress_string(#0), #1,   │
│ #2                                      │
│ ~3 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Hash Group By ────┴────────────────────╮
│ Groups: #0                              │
│ Aggregates: sum(#1), count_star()       │
│ ~3 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Projection ───────┴────────────────────╮
│ Projections: region, amount             │
│ ~6 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Projection ───────┴────────────────────╮
│ Projections:                            │
│ __internal_compress_string_ubigint(#0), │
│ #1                                      │
│ ~6 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Hash Join ────────┴────────────────────╮
│ Join Type: INNER                        │
│ Conditions: customer_id = customer_id   │
│ ~6 rows                                 │
╰────────────────────┬────────────────────╯
                     ├──────────────────────────────────────╮
╭─ Seq Scan ─────────┴────────────────────╮  ╭─ Seq Scan ───┴──────────────╮
│ Table: memory.main.customers            │  │ Table: memory.main.orders   │
│ Type: Sequential Scan                   │  │ Type: Sequential Scan       │
│ Projections: customer_id, region        │  │ Projections: customer_id,   │
│ ~6 rows                                 │  │              amount         │
╰─────────────────────────────────────────╯  │ Filters: status = 'shipped' │
                                             │ ~6 rows                     │
                                             ╰─────────────────────────────╯
```

<!-- /RESULT -->

---

<style scoped>table { font-size: 0.62em; } p { font-size: 0.8em; }</style>

## How to read it (bottom → top)

| Box in the plan | Logical step | What the optimizer did |
|---|---|---|
| 2 × **Seq Scan** | 1 `FROM` | reads only the needed columns (no `name`, no `order_id`) |
| `Filters: status = 'shipped'` *inside* the scan | 2 `WHERE` | **filter pushdown**: cancelled rows dropped while reading, before the join |
| **Hash Join** | 1 `JOIN` | hash table on one side, probed by the other |
| **Hash Group By** | 3 `GROUP BY` | one bucket per region: `sum`, `count_star()` |
| **Filter** `sum(amount) > 150` | 4 `HAVING` | on the groups, as expected |
| **Projection** `region, n_orders, total` | 5 `SELECT` | names the columns |
| **Top N** `Top: 2`, `total DESC` | 6 + 7 | keeps the 2 best rows instead of sorting everything |

`__internal_compress…` / `__internal_decompress…` projections: DuckDB speed tricks, ignore them.

---

<style scoped>table { font-size: 0.68em; } p { font-size: 0.8em; }</style>

## `EXPLAIN ANALYZE`: estimates vs actual rows

Same query, run with `EXPLAIN ANALYZE` (DuckDB 2.0.0). The plan has the same boxes;
each box now shows the **actual** rows that came out of it, and its time:

| Box | `EXPLAIN` estimate | `EXPLAIN ANALYZE` actual | Part 1 |
|---|:---:|:---:|---|
| Scan `orders` (with `status = 'shipped'`) | ~6 | **9** | step 2: 9 rows |
| Hash Join | ~6 | **9** | |
| Hash Group By | ~3 | **4** | step 3: 4 groups |
| Filter (`HAVING`) | ~0 | **3** | step 4: 3 groups |
| Top N | ~0 | **2** | step 7: 2 rows |

Estimates are guesses. A big gap between estimate and actual = the optimizer guessed wrong
(a common reason for a slow plan on big tables).

---

<style scoped>section{display:grid;grid-template-columns:1.2fr 1fr;grid-template-rows:auto 1fr;column-gap:24px;align-content:start;padding-top:40px} h2{grid-column:1/3;margin-bottom:8px} pre{margin:0;align-self:start} section>pre:nth-of-type(2), section>div:nth-of-type(2) pre{font-size:.5em;line-height:1.1} section>pre:first-of-type{font-size:.5em}</style>

## The optimizer rewrites your query: `HAVING` → scan filter

```sql
CREATE OR REPLACE TABLE big_sales AS
SELECT i AS sale_id, ['West', 'East', 'South', 'North'][i % 4 + 1] AS region,
       (i * 7919 % 1000)::DOUBLE AS amount
FROM range(5000000) AS r(i);

EXPLAIN SELECT region, SUM(amount) FROM big_sales GROUP BY region HAVING region = 'West';
```

<!-- RESULT -->

```text
╭─ Projection ────────────────────────────╮
│ Projections:                            │
│ __internal_decompress_string(#0), #1    │
│ ~4 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Hash Group By ────┴────────────────────╮
│ Groups: #0                              │
│ Aggregates: sum(#1)                     │
│ ~4 rows                                 │
╰────────────────────┬────────────────────╯
╭─ Projection ───────┴────────────────────╮
│ Projections: region, amount             │
│ ~1,250,000 rows                         │
╰────────────────────┬────────────────────╯
╭─ Projection ───────┴────────────────────╮
│ Projections:                            │
│ __internal_compress_string_ubigint(#0), │
│ #1                                      │
│ ~1,250,000 rows                         │
╰────────────────────┬────────────────────╯
╭─ Seq Scan ─────────┴────────────────────╮
│ Table: memory.main.big_sales            │
│ Type: Sequential Scan                   │
│ Projections: region, amount             │
│ Filters: region = 'West'                │
│ ~1,250,000 rows                         │
╰─────────────────────────────────────────╯
```

<!-- /RESULT -->

---

## `WHERE` or `HAVING` on a grouping column: same plan

- The `HAVING region = 'West'` filter was moved **down into the scan**: only ~1,250,000 of the 5,000,000 rows go on.
- `... WHERE region = 'West' GROUP BY region` gives **exactly the same plan** (the notebook compares the two: `True`).
- Still, **write it in `WHERE`**: it states your intent, and not every database is this smart.

---

<style scoped>pre { font-size: 0.6em; } table { font-size: 0.6em; } p { margin: 0.3em 0; }</style>

## ⚠️ `EXPLAIN ANALYZE` really runs the statement

Including `DELETE`, `UPDATE`, `INSERT`, `CREATE TABLE … AS`:

```sql
CREATE OR REPLACE TABLE scratch AS SELECT * FROM range(10) AS r(i);
EXPLAIN DELETE FROM scratch WHERE i < 5;
SELECT COUNT(*) AS rows_left_after_explain FROM scratch;
```

<!-- RESULT -->

| rows_left_after_explain |
|------------------------:|
|                      10 |

*(1 row)*

<!-- /RESULT -->

```sql
EXPLAIN ANALYZE DELETE FROM scratch WHERE i < 5;
SELECT COUNT(*) AS rows_left_after_explain_analyze FROM scratch;
```

<!-- RESULT -->

| rows_left_after_explain_analyze |
|--------------------------------:|
|                               5 |

*(1 row)*

<!-- /RESULT -->

---

## ✅ Check yourself

1. You need the regions whose **average** order is above \$100. `WHERE` or `HAVING`? Why?
2. Why can `ORDER BY` use the alias `total`, while standard SQL rejects it in `WHERE`?
3. Does `LIMIT 2` run before or after `ORDER BY`? What would go wrong otherwise?
4. One plan box says `~6 rows`, another says `9 rows`. What's the difference?
5. You want to see how a big `DELETE` will run, without deleting anything. Which command?

---

## ✅ Answers

1. `HAVING AVG(amount) > 100`: an average belongs to a **group**; groups exist only after step 3, `WHERE` is step 2.
2. `ORDER BY` is step 6, **after** `SELECT` (step 5) created the alias; `WHERE` is step 2. (DuckDB allows it in `WHERE` anyway.)
3. **After.** Otherwise you'd get 2 arbitrary rows, then sort them. In the plan both are one **Top N** box.
4. `~` = **estimate** (`EXPLAIN`, nothing ran); no `~` = **actual** count (`EXPLAIN ANALYZE`).
5. `EXPLAIN DELETE …`. `EXPLAIN ANALYZE DELETE …` really deletes.

---

## 📌 Cheat sheet

```text
Logical order:   FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
                 (rows)      (rows)  (groups)   (groups)  (columns) (sort)    (cut)
```

- **`WHERE` filters rows, `HAVING` filters groups.** No aggregates in `WHERE`.
- Aliases are born in `SELECT`: safe in `ORDER BY`; in `WHERE` only in friendly engines like DuckDB.
- Logical order = the **answer**; the optimizer picks the **physical plan** (pushdown, Top N, …).
- **`EXPLAIN`** = plan + estimates, nothing runs. **`EXPLAIN ANALYZE`** = runs it: actual rows + time.
- Read plans **bottom-up**. Works the same in the DuckDB CLI and qStudio: `EXPLAIN SELECT …;`
