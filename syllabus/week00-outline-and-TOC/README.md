# Week 0 — Course Outline & Table of Contents

**MSIS-2419 · Business Intelligence and Data Warehousing** · Winter 2027 (January–March)

Where this course goes, how each week works, and the software you need.

## 🗺️ The 10 weeks

| Block | Week | Topic |
|---|---|---|
| **A. SQL analytics review** | 1 | [Foundations of SQL for Analytics](../week01-Foundations-SQL-for-Analytics/) |
| | 2 | [SQL Analytical Thinking & EDA](../week02-SQL-Analytical-Thinking-and-EDA/) |
| **B. Classic data warehousing** | 3 | [Classic Data Warehousing & ETL](../week03-Classic-Data-Warehousing/) |
| | 4 | [Star Schema & OLAP](../week04-Star-Schema-and-OLAP/) |
| **C. Medallion architecture** | 5 | [Medallion Architecture: Introduction](../week05-Medallion-Architecture-Introduction/) |
| | 6 | [Bronze in Depth & Silver Cleaning](../week06-Bronze-and-Silver-Cleaning/) |
| | 7 | [Silver: Conforming & Integrating Sources](../week07-Silver-Layer-Cleaning-and-Conforming/) |
| | 8 | [Gold Layer & Star Schema](../week08-Gold-Layer-Star-Schema/) |
| **D. Wrap-up** | 9 | [End-to-End Pipeline & Project Workshop](../week09-End-to-End-Pipeline-and-Project-Workshop/) |
| | 10 | [Final Project & Data Storytelling](../week10-Final-Project-Data-Storytelling/) |
| *Optional* | — | [Bonus: LLM + SQL Integration](../bonus-LLM-SQL-Integration/) |

Project guidelines: [`../PROJECT/`](../PROJECT/)

## 📅 How each week works

- **2 sessions × 100 minutes**
- Each session: lecture + live demo, then a **30-minute in-class lab** (2 labs per week)
- Labs are **released at the start of their session** in each week's `labs/` folder (a lab sheet `.md` + a Marimo notebook `.py`). Do them in class and submit as instructed.

## ⚙️ Software setup (do this before week 1)

| Tool | Used for | Install |
|---|---|---|
| **DuckDB** | The database for the whole course | [duckdb.org/docs/installation](https://duckdb.org/docs/installation/) (CLI) |
| **Python 3.11+** | All notebooks (they are Marimo notebooks: `.py` files) | `pip install duckdb pandas matplotlib seaborn` |
| **Marimo** | The course notebooks (`.py`) and the in-class **lab notebooks** (`week_NN_lab_0X_student.py` in each `labs/` folder) | `pip install marimo`, then `marimo edit week_01_lab_01_student.py` from the lab's folder |
| **EDA extras** | Excel files, statistics and interactive charts in the week 2 EDA examples | `pip install openpyxl scipy plotly` |
| **Tableau** | Dashboards (from week 4 on) | Tableau Desktop / Public, free with a student license |

> ⚠️ **Keep one DuckDB version.** A `.duckdb` *file* written by a newer DuckDB can't be opened by an older one.
> Check that `duckdb --version` (CLI) and `python3 -c "import duckdb; print(duckdb.__version__)"` match.
> This matters for the labs that use a database file (Lab 4.2 and weeks 6–10) if you open the same file from both the DuckDB CLI and a notebook.

Check your setup by running [`week00_3_demo_notebook.py`](week00_3_demo_notebook.py) with `marimo edit week00_3_demo_notebook.py` (from this folder): it needs no data files.

## 📂 In this folder

| File | What it is |
|---|---|
| [`week00_1_table_of_contents.md`](week00_1_table_of_contents.md) | Course structure: why SQL → warehousing → Medallion (slides) |
| [`week00_2_outline_slides.md`](week00_2_outline_slides.md) | Week-by-week outline with one example per week (slides) |
| [`week00_5_dw_vs_medallion_slides.md`](week00_5_dw_vs_medallion_slides.md) | Classic DW vs Medallion architecture (slides) |
| [`KPI_examples.md`](KPI_examples.md) | What a KPI is, with practical examples |
| `week00_3_demo_notebook.py` | Live demo: messy data → wrong answer → cleaned → right answer |
| `week00_4_duckdb_sqlplot_pattern.py` | The **SQL → DataFrame → plot** pattern used all quarter |
