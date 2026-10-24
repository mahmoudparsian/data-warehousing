# Week 3 — Classic Data Warehousing & ETL

**Block B · Classic data warehousing (weeks 3–4)**

Operational (OLTP) systems run the business; a data warehouse (OLAP) lets us **analyze** it.
This week: why warehouses exist, how a star schema is built from operational tables,
and how ETL turns messy source data into trusted warehouse data.
Week 4 goes deeper into star schemas (SCD, conformed dimensions) and OLAP.

## 🎯 Learning objectives

By the end of the week you can:

1. Explain OLTP vs OLAP, and normalized vs denormalized design.
2. Describe the Inmon and Kimball approaches to building a warehouse.
3. Identify the **grain**, **facts (measures)** and **dimensions** of a business process.
4. Build a small star schema from operational tables with **surrogate keys**, and validate it against the source.
5. Explain ETL vs ELT, and write an ETL step in SQL: extract as text, profile, clean, deduplicate, load, **reconcile**.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | What a data warehouse is; OLTP vs OLAP; fact, dimension, grain | [slides: Classic DW](week03_slides_1_intro_to_DW.md) · [intro-to-DW deck](slides_intro_to_DW/) (pptx/pdf) · [OLTP vs OLAP table](resources/1-OLTP_vs_OLAP_comparison_table.md) · demo: [`book_seller_basic_dw_clean_data/`](book_seller_basic_dw_clean_data/) | [Lab 3.1](labs/week_03_lab_01_student.md): operational tables → star schema · notebook `week_03_lab_01_student.py` |
| 2 | ETL / ELT for data warehousing | [slides: ETL for DW](ETL/week03_slides_2_ETL_for_DW.md) · [ETL & ELT in pictures](ETL/resources/README.md) · demo: [`book_seller_basic_dw_messy_data/`](book_seller_basic_dw_messy_data/) | [Lab 3.2](labs/week_03_lab_02_student.md): ETL on messy sales data · notebook `week_03_lab_02_student.py` |

## 📂 What's in this folder

| Folder | Contents |
|---|---|
| [`labs/`](labs/) | Labs 3.1 and 3.2 (sheet `.md` + Marimo notebook, released in class) |
| [`book_seller_basic_dw_clean_data/`](book_seller_basic_dw_clean_data/) | Book seller: 2 operational tables → star schema (demo notebook) |
| [`book_seller_basic_dw_messy_data/`](book_seller_basic_dw_messy_data/) | Same business, messy data: a full cleaning + star-schema pipeline (demo notebook) |
| [`Normalization/`](Normalization/) | 1NF/2NF/3NF, update/insert/delete anomalies, and [why warehouses denormalize](Normalization/Importance_of_Denormalization_in_Data_Warehousing.md) |
| [`Data_Modeling/`](Data_Modeling/) | Data modeling and dimensional modeling: [overview](Data_Modeling/README.md) plus reading (PDF/pptx) |
| [`resources/`](resources/) | OLTP vs OLAP · intro to DW & BI · [star schema tutorial](resources/5-star-schema-introduction/star_schema_tutorial_practical_guide.md) · [retail star schema demo](resources/6-demo_star_schema/) · complete ETL examples 3 and 4 (MySQL) |
| [`ETL/`](ETL/) | ETL slides; [`resources/`](ETL/resources/) with many ETL examples (see below) |
| [`slides_intro_to_DW/`](slides_intro_to_DW/) | Introduction to data warehousing (pptx and 28-page PDF) |

### ETL examples (`ETL/resources/`)

- **DuckDB (use these first):**
  - ⭐ [`ETL_movies_to_star_schema/`](ETL/resources/ETL_movies_to_star_schema/): the complete story. 2M ratings: OLTP database → Python ETL → star schema → 20 OLAP queries. Run it with `python3 run_pipeline.py`.
  - [`ETL_using_DuckDB/`](ETL/resources/ETL_using_DuckDB/etl_using_duckdb.md) · [`ETL_with_Python_and_DuckDB/`](ETL/resources/ETL_with_Python_and_DuckDB/)
- **MySQL (reference, optional):** call center, insurance, electric vehicles, financial, Excel/CSV/Parquet loaders, PETL.
  The ETL ideas are the same; only the database connection differs.
- **Preview of weeks 5–8:** [`ETL/etl_medallion_olap_overview_slides.md`](ETL/etl_medallion_olap_overview_slides.md) and `ETL/etl_medallion_pipeline_notebook.py` (ETL as Bronze → Silver → Gold).

## ⚙️ Setup

DuckDB CLI, or Python with `duckdb pandas matplotlib jupysql duckdb-engine`.
Notebooks use relative paths, so open them from their own folder.

## ✅ Before week 4

- Finish both labs. Keep your star schema from Lab 3.1: week 4 queries it with OLAP operations.
- Read the [star schema tutorial](resources/5-star-schema-introduction/star_schema_tutorial_practical_guide.md).
- Install **Tableau** (Desktop or Public, free with a student license). We start using it in week 4.
