# Week 4 — Star Schema in Depth & OLAP

**Block B · Classic data warehousing (weeks 3–4)**

Week 3 built a first star schema. This week makes it production-ready, so it keeps **history** correctly
(slowly changing dimensions) and shares dimensions across facts. Then we analyze it the way business users do:
**OLAP** roll-up, drill-down, slice, dice and pivot, with `ROLLUP`, `CUBE` and `GROUPING SETS`.
Our first **Tableau** chart closes the week.

## 🎯 Learning objectives

By the end of the week you can:

1. Explain SCD Type 1 vs Type 2, and implement Type 2 (`valid_from`, `valid_to`, `is_current`, new surrogate key).
2. Load facts against the dimension version that was valid at the time of the fact, and spot a fan-out join.
3. Explain conformed dimensions, factless fact tables and data marts.
4. Perform roll-up, drill-down, slice, dice and pivot in SQL.
5. Use `ROLLUP`, `CUBE`, `GROUPING SETS` and `GROUPING()` to produce subtotals in one query.
6. Export a summary from DuckDB and build a first chart in Tableau.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Star schema in depth: SCD, conformed dimensions, factless facts, data marts | [slides](week04_slides_star_schema_SCD_OLAP.md) (first half) · [SCD module](star_schema/slowly_changing_dimensions/0.README.md) · demo: [`week04_notebook_bike_store_star_schema_OLAP.py`](week04_notebook_bike_store_star_schema_OLAP.py) | [Lab 4.1](labs/week_04_lab_01_student.md): SCD Type 1 and 2 · notebook `week_04_lab_01_student.py` |
| 2 | OLAP: roll-up, drill-down, slice, dice, pivot; `ROLLUP`, `CUBE`, `GROUPING SETS`; first Tableau chart | [slides](week04_slides_star_schema_SCD_OLAP.md) (second half) · [OLAP index](OLAP/README.md) · [ROLLUP & CUBE in DuckDB](OLAP/OLAP_basics/ROLLUP_and_CUBE_Tutorial_using_DuckDB.md) · [45 OLAP queries](OLAP/OLAP_by_DuckDB/OLAP_Queries_ROLLUP_CUBE_GROUPINGSETS.md) | [Lab 4.2](labs/week_04_lab_02_student.md): OLAP on 1M sales + Tableau · notebook `week_04_lab_02_student.py` |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 4.1 (+ `week_04_lab_01_setup.sql`) and 4.2 (sheet `.md` + Marimo notebook, released in class); [extended practice](labs/week_04_lab_extended_practice_bike_store_student.md) with 16 Bike Store tasks (optional) |
| `week04_notebook_bike_store_star_schema_OLAP.py` | Demo: build a Bike Store star schema, then OLAP queries (roll-up, drill-down, slice, dice, top-N per store) |
| [`OLAP/`](OLAP/) | OLAP concepts, one file per operation, the **DuckDB online-sales star** ([`OLAP_by_DuckDB/`](OLAP/OLAP_by_DuckDB/), 1M rows, used in Lab 4.2), lecture PDFs, MySQL/Snowflake references |
| [`star_schema/`](star_schema/) | Star schema concepts and the SCD module, plus many worked examples (below) |

### Star schema examples (`star_schema/`)

- **Concepts:** [`star_schema_concepts/`](star_schema/star_schema_concepts/) · [`star_schema_examples/`](star_schema/star_schema_examples/) (diagrams) · [`intro-to-DW-and-Star-Schema/`](star_schema/intro-to-DW-and-Star-Schema/) (the 4 DW properties: subject-oriented, integrated, time-variant, non-volatile)
- **Worked examples:** book seller, bike store, music streaming, vacation rental, e-commerce, diabetes, stock transactions, sales transactions.
  Most include the schema SQL and OLAP queries. Several are written for **MySQL** (reference): the modeling is the same, only the loading scripts differ.
- **Big tutorial (MySQL):** [`star_schema_tutorial/`](star_schema/star_schema_tutorial/README.md): 100k-row OLTP → star schema → OLAP, with a workbook.

## ⚙️ Setup

- DuckDB CLI and Python (`duckdb pandas matplotlib marimo`), as before ([Required software](../../course_information/required_software.md)).
- **Tableau** Desktop or Public (free with a student license). Tableau decks: [`../../resources/Tableau/`](../../resources/Tableau/).
- Build the online-sales star once before Session 2 (about 2 seconds):
  `cd OLAP/OLAP_by_DuckDB && duckdb online_sales.duckdb < build_and_load_all_duckdb.sql`

## ✅ Before week 5

- Finish both labs; keep your Tableau screenshot.
- Think about where data quality checks belonged in weeks 3–4 (ETL rules, validation, SCD). Week 5 organizes all of that into **Bronze → Silver → Gold**.
