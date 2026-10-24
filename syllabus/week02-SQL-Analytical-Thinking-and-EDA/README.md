# Week 2 — SQL Analytical Thinking & Exploratory Data Analysis

**Block A · SQL analytics review (weeks 1–2)**

Week 1 answered questions about groups. This week we answer questions about
**individuals compared with their group** (window functions), and we learn to
**profile data before we trust it** (EDA). EDA is the first step of every data-warehouse project.

## 🎯 Learning objectives

By the end of the week you can:

1. Explain the difference between `GROUP BY` (collapses rows) and `OVER()` (keeps rows).
2. Use `PARTITION BY`, `ORDER BY` and frames in window functions.
3. Rank within groups with `ROW_NUMBER`, `RANK`, `DENSE_RANK` and solve "top-N per group".
4. Compute percent of total, running totals, moving averages and `LAG`/`LEAD` changes.
5. Profile a dataset with SQL: shape, NULLs, suspicious values, duplicates, distributions, outliers.
6. Spot a misleading trend caused by a change in the mix of a group.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Analytical thinking + window functions | [slides 1: analytical thinking](week02_slides_1.md) · [slides 2: window functions](week02_slides_2_window_functions.md) · `week02_notebook_1.py` (exercises) · `week02_notebook_3.py` (advanced, with plots) | [Lab 2.1](labs/week_02_lab_01_student.md): window functions · notebook `week_02_lab_01_student.py` |
| 2 | Exploratory data analysis with SQL | [What is EDA?](EDA/1.What_is_Exploratory_Data_Analysis.md) (slides) · `EDA/2.EDA_basic.py` · `EDA/3.EDA_comprehensive.py` | [Lab 2.2](labs/week_02_lab_02_student.md): EDA on 4 yearly files · notebook `week_02_lab_02_student.py` |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 2.1 and 2.2 (sheet `.md` + Marimo notebook, released in class), plus [`week_02_lab_extended_practice_student.md`](labs/week_02_lab_extended_practice_student.md) (16 more window-function tasks, optional) |
| `week02_notebook_2.py` | 10 questions on insurance data: NL query → SQL → plot → insight |
| [`EDA/`](EDA/) | EDA slides, two notebooks, and `data/insurance.2021–2024.csv` (one file per year) |
| [`EDA/more_examples/`](EDA/more_examples/) | More EDA case studies (car sales, online retail, used cars) plus an [EDA report template](EDA/more_examples/data_exploration_TOC.md) |
| [`Ranking_Algorithms/`](Ranking_Algorithms/) | Ranking functions explained with examples. Files 2 and 3 use **MySQL**; the syntax is the same in DuckDB |
| [`Join_Operation/`](Join_Operation/) | **Review:** INNER / LEFT / RIGHT / FULL / CROSS joins. You need joins for star schemas in week 4 |
| [`super_store_data_analysis/`](super_store_data_analysis/) | Optional practice: 19 analysis queries on 51k Superstore orders (written for MySQL) |

## ⚙️ Setup

Same as week 1, plus `seaborn` for `EDA/2.EDA_basic.py`: `pip install duckdb pandas matplotlib seaborn marimo`
(extras for the more-examples notebooks: `openpyxl scipy plotly`; see [Required software](../../course_information/required_software.md)).
Open each Marimo notebook from its own folder (`marimo edit <notebook>.py`): they use relative paths.

## ✅ Before week 3

- Finish both labs.
- Review [joins](Join_Operation/join_operation_in_action_1_4_types.md) if they feel rusty.
- Keep your **3 data-quality rules** from Lab 2.2 (exit ticket). We use them in week 3 (ETL).
