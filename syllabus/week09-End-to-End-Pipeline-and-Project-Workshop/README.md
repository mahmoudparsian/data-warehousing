# Week 9 — End-to-End Pipeline, Incremental Processing & Project Workshop

**Block D · Wrap-up (weeks 9–10)**

Until now every lab rebuilt the warehouse from scratch. Real pipelines run **every day or every month** as new data arrives,
and they must stay correct when data comes **late** or is **re-sent corrected**. This week the pizza shop's delivery app
sends one file per month, and we run the whole pipeline (Bronze → Silver → Gold → mart) **incrementally**,
then prove the result equals a full rebuild. The second half of Session 2 is a **project workshop**.

## 🎯 Learning objectives

By the end of the week you can:

1. Explain full rebuild vs incremental processing, and what *state* an incremental pipeline needs.
2. Build an idempotent load with a **load log** and lineage columns (`_run_id`, `_source_file`), parameterized with session variables.
3. Process only a run's new rows through Silver and Gold, with reproducible surrogate keys.
4. Detect late-arriving data and rebuild only the **affected partitions** of a mart.
5. Replace a corrected re-send (supersede, delete by lineage, reprocess).
6. Prove that incremental = full rebuild.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Pipelines over time: state, watermarks, idempotency, incremental Silver and Gold | [slides 1: pipelines + incremental](week09_slides_1_pipelines_incremental.md) (Parts 0–9) · [slides 2: DuckDB patterns](week09_slides_2_incremental_in_duckdb.md) (Patterns 1–5) | [Lab 9.1](labs/week_09_lab_01_student.md): monthly files, one run at a time · notebook `week_09_lab_01_student.py` |
| 2 | Late data, partition rebuilds, corrections, validation · **project workshop** | [slides 1](week09_slides_1_pipelines_incremental.md) (Parts 10–20) · [slides 2](week09_slides_2_incremental_in_duckdb.md) (Patterns 6–8) · [project checklist](project_workshop_checklist.md) | [Lab 9.2](labs/week_09_lab_02_student.md): late data, a corrected re-send, the proof · notebook `week_09_lab_02_student.py` |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 9.1 and 9.2 (sheet `.md` + Marimo notebook, released in class) · `week_09_lab_setup.sql` (the week 6–8 pizza warehouse for POS sales + empty delivery pipeline + `silver.delivery_conform(run_id)` macro), [extended practice](labs/week_09_lab_extended_practice_insurance_incremental_student.md): updates/upserts on insurance data (optional) |
| [`pizza_incremental/landing/`](pizza_incremental/landing/) | The delivery app's export, one file per **UTC** month (`delivery_app_2016_01.csv` … `_12.csv`, `delivery_app_2017_01.csv`), plus a corrected re-send `delivery_app_2016_06_v2.csv` |
| `week09_notebook.py` | Day 1 / Day 2 incremental pipeline demo with updates and late rows (insurance data) |
| [`project_workshop_checklist.md`](project_workshop_checklist.md) | 15-step checklist for your team project, mapped to the weeks where each step was taught |

## ⚙️ Setup

```bash
cd labs
duckdb pizza.duckdb < week_09_lab_setup.sql
```
Start each session with `SET TimeZone = 'UTC';`. Lab 9.2 also builds a second database, `pizza_full.duckdb` (git-ignored like all `.duckdb` files).

## ✅ Before week 10

- Finish both labs.
- Project: finish every ☐ on the [checklist](project_workshop_checklist.md) except the story (step 15). Week 10 is about the story.
