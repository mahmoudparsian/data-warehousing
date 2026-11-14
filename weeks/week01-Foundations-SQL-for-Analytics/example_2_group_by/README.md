# Example 2 — Teaching GROUP BY with a Tiny Table

A 16-row `sales.csv` (`country, product, price`) that is small enough to check every answer by hand.

| File | What it is |
|---|---|
| `sales.csv` | The tiny dataset |
| `Teaching_GROUP_BY_DuckDB.py` | 14 questions → SQL → explanation → insight → plot |
| [`GROUPBY_Advanced_MARP_Slides.md`](GROUPBY_Advanced_MARP_Slides.md) | Slides |

The 14 questions:

1. Display all records from the sales table
2. Total sales for all products for USA
3. Total sales for all products for all countries
4. List of unique countries
5. List of unique products
6. Total product sales per country
7. Total product sales per product
8. Total product sales per country and product
9. Number of sales per country
10. Top-selling product per country
11. Top-selling country overall
12. Full ranking of all countries (by sales)
13. Countries that sold more than $1,500 (→ `HAVING`)
14. Highest-priced product sold per country

💡 Try each question yourself **before** opening the notebook.
