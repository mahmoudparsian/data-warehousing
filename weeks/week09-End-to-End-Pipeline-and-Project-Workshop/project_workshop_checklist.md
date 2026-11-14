# 🛠️ Project Workshop: Checklist

Use the second half of Session 2 to move your team project forward. Work through this list with your teammate;
the instructor will come round to each team. Bring your dataset and your notebook.

Project rules and grading: [`../PROJECT/DW_Project_Guidelines.md`](../PROJECT/DW_Project_Guidelines.md) ·
steps: [`../PROJECT/Project-Step-by-Step-Medallion_Architecture.md`](../PROJECT/Project-Step-by-Step-Medallion_Architecture.md)

| # | Project step | Done? | Where you learned it |
|---|---|---|---|
| 1 | **Dataset described**: source, rows, columns, what one row means | ☐ | week 2 (EDA), [PROJECT/data_set_examples](../PROJECT/data_set_examples.md) |
| 2 | **EDA** on the raw data: NULLs, duplicates, formats, outliers, suspicious values | ☐ | week 2 (Lab 2.2), [EDA guidelines](../PROJECT/DW_EDA_Guidelines.md) |
| 3 | **Bronze**: raw files landed as text, with `_source_file` / `_batch_id` / `_ingested_at`; load errors recorded (`store_rejects`) | ☐ | week 6 (Lab 6.1) |
| 4 | **Business rules** written down (fix / reject / flag), one line each | ☐ | weeks 3, 5, 6 |
| 5 | **Silver**: rules applied; rejected rows kept with a reason; types cast; duplicates removed (raw first) | ☐ | weeks 5–7 |
| 6 | **Reconciliation**: Bronze rows = valid + rejected + duplicates (+ flagged) | ☐ | weeks 3, 5, 6, 7 |
| 7 | Second source? **Conformed** with mapping tables (codes, names, time zones) | ☐ | week 7 |
| 8 | **Grain** of the fact table in one sentence, tested on the data | ☐ | weeks 3, 8 |
| 9 | **Star schema**: date dimension as a full calendar (+ Unknown), other dimensions with surrogate keys, fact with additive measures | ☐ | weeks 3, 4, 8 |
| 10 | **Validation**: fact rows and totals = Silver; no orphan keys | ☐ | week 8 |
| 11 | **7 OLAP queries**: question → SQL → result → chart → business insight + action | ☐ | weeks 4, 8 |
| 12 | KPIs computed correctly (ratios of sums; distinct counts recomputed) | ☐ | week 8 |
| 13 | **New batch**: what happens when next month's file arrives? (load log, idempotent load, rebuild touched periods) | ☐ | week 9 |
| 14 | **Tableau** dashboard from a Gold mart | ☐ | weeks 4, 8 |
| 15 | **Story** for the presentation: 3 insights, 3 recommendations | ☐ | week 10 |

## Questions to answer before you leave today

1. What is the grain of your fact table?
2. Which three business rules affect the most rows, and how many rows each?
3. Which of your 7 OLAP queries leads to the most useful **action**?
4. What is still missing from the list above, and who does it by when?
