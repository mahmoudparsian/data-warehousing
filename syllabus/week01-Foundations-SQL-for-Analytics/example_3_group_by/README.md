# Example 3 — GROUP BY Masterclass (1 million sales rows)

A generated sales table (`sales.csv`, ~1M rows, 2023–2025) with realistic skew:
USA dominates, FEMALE:MALE ≈ 2:1, uneven product mix.
Columns are described in [`sales_data_dictionary.md`](sales_data_dictionary.md).

| File | What it is | When |
|---|---|---|
| `EDA_sales_data.py` | Exploratory analysis through GROUP BY business questions | Week 1 |
| `Window_Functions_Module.py` | Window functions: SQL + insight + plot | Preview, covered in **week 2** |
| `Medallion_sales_data.py` | The same data in a Bronze → Silver → Gold pipeline | Preview, covered in **weeks 5–8** |
| `generate_sales_data.py` | Script that generated `sales.csv` | — |
