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
4. Decide what a duplicate is: the same real thing sent twice. Compare **standardized** values for customers, **exact raw** copies for order lines
   without a line id (and explain why a line id from the source is the real fix).
5. Handle disagreeing sources (keep both values, decide per KPI) and integrate with `UNION ALL` / `UNION ALL BY NAME` plus a `channel` column.
6. Give every row one fate (valid · flagged · rejected · duplicate, week 5), reconcile **every source**, then answer cross-source business questions.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Conformance: schema alignment, key conformance, canonical codes, mapping tables, fates per source, time zones | [slides 1: conformance & integration](lecture_notes_01_conformance_and_integration.md) (4 insurance sources, end to end: 6,467 = 4,160 + 1,037 + 974 + 296) · [slides 2: DuckDB patterns](lecture_notes_02_conforming_in_duckdb.md) (Steps 1–4) | [Lab 7.1](labs/week_07_lab_01_student.md): conform the delivery app · notebook [`week_07_lab_01_student.py`](labs/week_07_lab_01_student.py) |
| 2 | Integration: quarantine, source conflicts, `UNION ALL`, reconciliation, cross-source KPIs | [slides 2](lecture_notes_02_conforming_in_duckdb.md) (Steps 5–7) · [Silver transformations deep dive](Medallion_Architecture_Silver_Transformations.md) · [`notebook_01_multi_source_conformance.py`](notebook_01_multi_source_conformance.py) | [Lab 7.2](labs/week_07_lab_02_student.md): one Silver table, two channels · notebook [`week_07_lab_02_student.py`](labs/week_07_lab_02_student.py) |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 7.1 and 7.2 (sheet `.md` + Marimo notebook, released in class) · `week_07_lab_setup.sql` (rebuilds the week 6 pizza Silver tables into `labs/pizza.duckdb`), [extended practice](labs/week_07_lab_extended_practice_insurance_conformance_student.md): conform 4 messy insurance files (optional) |
| [`notebook_01_multi_source_conformance.py`](notebook_01_multi_source_conformance.py) | Slides 1's pipeline on the 4 messy insurance files, **per source**, with charts: profile, conform (macro + mapping tables), deduplicate, reject / flag, reconcile each source, tests, why the unknown regions are flagged (53% smokers) |
| [`data_messy/`](data_messy/) · [`data/`](data/) | Insurance 2021–2024: messy versions (used by slides 1–2, the notebook and the extended practice) and clean versions (for comparison) |
| [`Medallion_Architecture_Silver_Transformations.md`](Medallion_Architecture_Silver_Transformations.md) | Optional Silver reference: sections 1–4 (casting, dedup with window functions, NULLs, enrichment) run on a small table; the rest are patterns (time zones, MERGE, hashing, quarantine, CDC, …) |

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
