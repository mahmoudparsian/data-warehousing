# Example 1 — SQL Foundations on an Insurance Dataset

Used in **Session 1** and in [Lab 1.1](../labs/week_01_lab_01_student.md).

| File | What it is |
|---|---|
| `insurance.csv` | 1,338 customers: `age, gender, bmi, children, smoker, region, charges` |
| [`insurance_metadata_description.md`](insurance_metadata_description.md) | What each column means |
| `week1_sql_foundations.py` | 10 basic, 10 intermediate and 5 advanced queries, each with SQL, explanation, business insight and a plot |
| [`week1_sql_foundations.marp.md`](week1_sql_foundations.marp.md) | Slide version (Marp) |

Quick start (DuckDB CLI, run in this folder):

```sql
CREATE TABLE insurance AS SELECT * FROM read_csv_auto('insurance.csv');
SELECT smoker, ROUND(AVG(charges), 2) AS avg_charges FROM insurance GROUP BY smoker;
```

> One cell in the notebook contains an **intentional error** (a missing comma), so you can see what DuckDB's error messages look like.
