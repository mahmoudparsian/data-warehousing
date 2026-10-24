# Example 4 — GROUP BY Across Several Years (1 million sales rows)

Four yearly files with the same columns, used in [Lab 1.2](../labs/week_01_lab_02_student.md):

| File | Rows | Period |
|---|---|---|
| `sales_2023.csv` | 100,000 | full year |
| `sales_2024.csv` | 200,000 | full year |
| `sales_2025.csv` | 400,000 | full year |
| `sales_2026.csv` | 300,000 | Jan–Mar only |

Columns and business rules (e.g. `sales_amount = quantity * price - discount`;
`transaction_id` is **not** unique): [`sales_metadata_dictionary.md`](sales_metadata_dictionary.md)

| Notebook | What it is |
|---|---|
| `groupby_duckdb_sales_tutorial.py` | GROUP BY, top-N and business-insight queries with plots |
| `sales_comprehensive_eda.py` | Exploratory data analysis of all four years |

Read all four years as one table:

```sql
CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales_202*.csv');
```
