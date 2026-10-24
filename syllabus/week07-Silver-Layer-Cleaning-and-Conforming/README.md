# Week 7 — Silver: Conforming & Integrating Sources

**Block C · Medallion architecture + star schema (weeks 5–8)**

Real warehouses rarely have one source. In 2016 the pizza shop from week 6 also sold through a **delivery app**,
which sends its own export with different column names, spellings, size words, prices as text, and timestamps in UTC.
This week we **conform** that source (same columns, same codes, same meaning) and **integrate** it with the shop's
own sales into one Silver table, `silver.sales_lines`, ready for the Gold star schema in week 8.

## 🎯 Learning objectives

By the end of the week you can:

1. Write a schema mapping between two sources and spot every needed transformation.
2. Normalize spellings with a macro and map codes with **mapping tables** (not long `CASE`s); quarantine what can't be mapped.
3. Convert timestamps to the business's time zone and explain the session-time-zone trap.
4. Explain why exact duplicates are removed **before** conforming.
5. Handle disagreeing sources (keep both values, decide per KPI) and integrate with `UNION ALL` / `UNION ALL BY NAME` plus a `channel` column.
6. Reconcile every source, then answer cross-source business questions.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Conformance: schema alignment, canonical codes, mapping tables, time zones | [slides 1: conformance & integration](week07_slides_1_conformance_and_integration.md) · [slides 2: DuckDB patterns](week07_slides_2_conforming_in_practice.md) (Steps 1–4) | [Lab 7.1](labs/week_07_lab_01_student.md): conform the delivery app · notebook `week_07_lab_01_student.py` |
| 2 | Integration: quarantine, source conflicts, `UNION ALL`, reconciliation, cross-source KPIs | [slides 2](week07_slides_2_conforming_in_practice.md) (Steps 5–7) · [Silver transformations deep dive](Medallion_Architecture_Silver_Transformations.md) · `week07_notebook.py` | [Lab 7.2](labs/week_07_lab_02_student.md): one Silver table, two channels · notebook `week_07_lab_02_student.py` |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 7.1 and 7.2 (sheet `.md` + Marimo notebook, released in class) · `week_07_lab_setup.sql` (rebuilds the week 6 pizza Silver tables into `labs/pizza.duckdb`), [extended practice](labs/week_07_lab_extended_practice_insurance_conformance_student.md): conform 4 messy insurance files (optional) |
| `week07_notebook.py` | Multi-source conformance demo on the 4 messy insurance files: profile per source, align, conform, integrate, validate |
| [`data/`](data/) · [`data_messy/`](data_messy/) | Insurance 2021–2024: clean and messy versions (used by the slides, notebook and extended practice) |
| [`Medallion_Architecture_Silver_Transformations.md`](Medallion_Architecture_Silver_Transformations.md) | Silver deep dive: casting, dedup with window functions, nulls, enrichment, time zones, … |

The pizza data (including the new `delivery_app_2016.csv`) lives in week 6:
[`../week06-Bronze-and-Silver-Cleaning/pizza_sales_medallion/data/`](../week06-Bronze-and-Silver-Cleaning/pizza_sales_medallion/data/).

## ⚙️ Setup

```bash
cd labs
duckdb pizza.duckdb < week_07_lab_setup.sql
```
Then start every session with `SET TimeZone = 'UTC';` so everyone gets the same results.

## ✅ Before week 8

- Finish both labs. Week 8 builds the Gold star schema on `silver.sales_lines`; its setup script rebuilds that table, so you don't need to keep `pizza.duckdb`.
