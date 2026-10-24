# Week 6 — Bronze in Depth & Silver Cleaning

**Block C · Medallion architecture + star schema (weeks 5–8)**

Week 5 showed the whole Medallion idea. Now we go layer by layer on one realistic case: a **pizza shop**
that sends its data in two yearly batches plus a menu, with real-world problems (two date formats, NULL keys,
duplicates, ids that restart in every file, and a file that won't even load).

- **Session 1, Bronze:** land every file so nothing is lost, every row is traceable, and load errors are recorded.
- **Session 2, Silver cleaning:** turn Bronze into typed, deduplicated, referentially consistent tables, and prove it.

Week 7 continues with Silver **conformance** (combining different sources); week 8 builds **Gold**.

## 🎯 Learning objectives

By the end of the week you can:

1. Inventory a landing folder and land files as text with lineage (`_source_file`, `_batch_id`, `_ingested_at`).
2. Handle a load failure correctly: `store_rejects` and `reject_errors` (and why never `ignore_errors`), including encoding problems.
3. Append a new batch idempotently, and detect keys that collide across batches.
4. Profile Bronze into a Silver to-do list.
5. Apply Silver rules: parse mixed formats, drop invalid rows, deduplicate, cast types.
6. Check referential integrity before joining; reconcile Bronze → Silver; validate against a known control total.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Bronze in depth | [slides: Bronze in depth](week06_slides_1_bronze_in_depth.md) · [pizza shop data](pizza_sales_medallion/README.md) · [story](pizza_sales_medallion/pizza_dw_story.md) | [Lab 6.1](labs/week_06_lab_01_student.md): land 2 batches + the menu · notebook `week_06_lab_01_student.py` |
| 2 | Silver cleaning: data-quality dimensions, profiling, nulls, standardization, outliers, dedup, enrichment, validation | [slides: Silver cleaning](week06_slides_2_silver_cleaning.md) · `week06_notebook.py` (the same ideas on insurance data) | [Lab 6.2](labs/week_06_lab_02_student.md): Bronze → trusted Silver order lines · notebook `week_06_lab_02_student.py` |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 6.1 and 6.2 (sheet `.md` + Marimo notebook, released in class) (they share `labs/pizza.duckdb`, which is git-ignored); [extended practice](labs/week_06_lab_extended_practice_silver_insurance_student.md): Silver on insurance data (optional) |
| [`pizza_sales_medallion/`](pizza_sales_medallion/) | Pizza shop data (2015 + 2016 + menu), business rules, and `pizza_shop_dw.py`: the full pipeline to a Gold star schema with analysis |
| `week06_notebook.py` | Silver deep-dive notebook: profiling, cleaning, validation, before/after KPIs (insurance data) |

## ⚙️ Setup

As before. The labs use a DuckDB **database file** (`duckdb pizza.duckdb` in `labs/`) so Lab 6.2 can continue from Lab 6.1.

## ✅ Before week 7

- Finish both labs. Week 7 rebuilds these Silver tables with its own setup script, so you don't need to keep `pizza.duckdb`.
- Read sections 1–4 (casting, dedup, nulls, enrichment) of the [Silver transformations deep dive](../week07-Silver-Layer-Cleaning-and-Conforming/Medallion_Architecture_Silver_Transformations.md).
