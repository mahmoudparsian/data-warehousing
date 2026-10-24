# Week 5 — Medallion Architecture: Introduction

**Block C · Medallion architecture + star schema (weeks 5–8)**

Weeks 3–4 built a classic warehouse: ETL cleaned the data **on the way in**, and the original was gone.
The **Medallion architecture** organizes the same work into layers that keep everything:

```
🟫 Bronze (raw, as it arrived) → ⚪ Silver (clean, validated, typed) → 🟡 Gold (business-ready, star schema / KPIs)
```

This week: the idea end to end, first as **schemas in one database**, then as a **lakehouse** (layers = folders of files).
Week 6 goes deep into Bronze and Silver cleaning, week 7 into Silver conformance, and week 8 into Gold.

## 🎯 Learning objectives

By the end of the week you can:

1. Explain what each Medallion layer is for, and why Bronze is never "fixed".
2. Add lineage columns (`_source_file`, `_ingested_at`) to a Bronze layer.
3. Turn written business rules into Silver SQL: reject with a reason (quarantine), flag, fix, standardize, deduplicate.
4. Reconcile layers: Bronze rows = valid + flagged + rejected + duplicates.
5. Build Gold tables that answer business questions from Silver.
6. Explain warehouse vs lake vs lakehouse; write Parquet layers with DuckDB (`COPY … PARTITION_BY`) and query them in place.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Why Medallion; Bronze → Silver → Gold with business rules | [slides](slides_and_notebook/week05_slides.md) · [Medallion in a nutshell](Medallion_Architecture_in_a_Nutshell.md) · [Classic DW vs Medallion](../week00-outline-and-TOC/week00_5_dw_vs_medallion_slides.md) · demo: [10-rows case study](case_study_10_rows/) | [Lab 5.1](labs/week_05_lab_01_student.md): 1,400 messy sales → 3 layers · notebook [`week_05_lab_01_student.py`](labs/week_05_lab_01_student.py) |
| 2 | Medallion as a lakehouse: files, Parquet, partitions | [slides: lakehouse with DuckDB](slides_and_notebook/week05_slides_2_lakehouse_with_duckdb.md) · [From DW to lakehouse](lakehouse/introduction_to_lakehouse/1.From_DW_to_Lakehouse_DuckDB_Tutorial.md) · demo: [`lakehouse/examples/insurance_4_years/`](lakehouse/examples/insurance_4_years/) | [Lab 5.2](labs/week_05_lab_02_student.md): layers as Parquet files · notebook [`week_05_lab_02_student.py`](labs/week_05_lab_02_student.py) |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 5.1, 5.2 (sheet `.md` + Marimo notebook, released in class); optional extended practice: [Medallion mapping (no code)](labs/week_05_lab_extended_practice_mapping_student.md), [ETL + OLAP + Medallion](labs/week_05_lab_extended_practice_etl_olap_medallion_student.md) |
| [`slides_and_notebook/`](slides_and_notebook/) | Session 1 and 2 slides; `week05_notebook.py` (Medallion on the insurance data with pandas + DuckDB) |
| [`case_study_10_rows/`](case_study_10_rows/) | **Start here.** 10 rows, every kind of problem, traced through all three layers to a star schema |
| [`sales_1200_clean_records/`](sales_1200_clean_records/) · [`sales_1400_messy_records/`](sales_1400_messy_records/) · [`sales_18K_messy_records/`](sales_18K_messy_records/) | The same pipeline on growing, messier data (with business rules and notebooks) |
| [`Medallion_Architecture_Introduction.md`](Medallion_Architecture_Introduction.md) | Slides: the 4 layers with DuckDB SQL examples |
| [Silver transformations deep dive](../week07-Silver-Layer-Cleaning-and-Conforming/Medallion_Architecture_Silver_Transformations.md) | Now in week 7 (preview) |
| [`lakehouse/`](lakehouse/) | Lakehouse concepts ([intro](lakehouse/introduction_to_lakehouse/)) and three examples: [insurance, 4 years](lakehouse/examples/insurance_4_years/) (small), [White House visitor logs](lakehouse/examples/whitehouse_visitor_logs/) (real, 191 MB), [used cars](lakehouse/examples/used_cars_dataset/) (1.4 GB capstone) |

The book-seller Medallion example from week 3 is here: [clean](../week03-Classic-Data-Warehousing/book_seller_basic_dw_clean_data/) · [messy](../week03-Classic-Data-Warehousing/book_seller_basic_dw_messy_data/).

## ⚙️ Setup

As before (DuckDB CLI; Python with `duckdb pandas matplotlib seaborn marimo`; [Required software](../../course_information/required_software.md)).
Large data: the used-cars and White House examples need a download or unzip first (see their READMEs).
Files the labs create (`silver_*/`, `*.parquet`) are git-ignored.

## ✅ Before week 6

- Finish both labs. Week 6 starts a new running case, a pizza shop, and goes deep into Bronze and Silver. Bring the reconciliation habit from Lab 5.1.
- Read [Medallion in a nutshell](Medallion_Architecture_in_a_Nutshell.md).
