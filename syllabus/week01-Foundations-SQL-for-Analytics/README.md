# Week 1 — Foundations of SQL for Analytics

**Block A · SQL analytics review (weeks 1–2)**

SQL is not about writing queries. It is about answering business questions.
This week reviews the core of analytical SQL in DuckDB:
`SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `CASE`, `ORDER BY … LIMIT`.

## 🎯 Learning objectives

By the end of the week you can:

1. Load a CSV file into DuckDB and explore it (rows, columns, types).
2. Turn a business question into a `SELECT … WHERE … GROUP BY` query.
3. Explain the difference between `WHERE` (filters rows) and `HAVING` (filters groups).
4. Build segments with `CASE` and compare them.
5. Turn a query result into a one-sentence business insight.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Question → SQL → insight; filtering and aggregation on insurance data | [slides](lectures_and_notebooks/week01_slides.md) · `lectures_and_notebooks/week01_notebook_2.py` (exercises, matches the slides) · `week01_notebook_1.py` (EDA storytelling) | [Lab 1.1](labs/week_01_lab_01_student.md): insurance · notebook [`week_01_lab_01_student.py`](labs/week_01_lab_01_student.py) |
| 2 | GROUP BY in depth: multi-column groups, `HAVING`, `CASE`, top-N, percent of total | [slides: HAVING & CASE](lectures_and_notebooks/week01_slides_2_having_case.md) · [Understanding GROUP BY](understanding_GROUP_BY/Understanding_GROUP_BY.md) · `understanding_GROUP_BY/group_by_notebook.py` · [Example 2](example_2_group_by/) (tiny table) | [Lab 1.2](labs/week_01_lab_02_student.md): 400k sales rows · notebook [`week_01_lab_02_student.py`](labs/week_01_lab_02_student.py) |

## 📂 What's in this folder

| Folder | Contents |
|---|---|
| [`lectures_and_notebooks/`](lectures_and_notebooks/) | Week 1 slides and notebooks. `week01_notebook_3.py` is the full "master" notebook; `week01_insurance_EDA.py` is a pandas EDA |
| [`labs/`](labs/) | The two in-class labs: each as a sheet (`.md`) and a Marimo notebook (`marimo edit week_01_lab_01_student.py` from `labs/`) |
| [`example_1_insurance/`](example_1_insurance/) | Insurance dataset + 25 graded-difficulty queries |
| [`example_2_group_by/`](example_2_group_by/) | 14 GROUP BY questions on a 16-row table |
| [`example_3_group_by/`](example_3_group_by/) | 1M-row sales EDA; previews of window functions (week 2) and Medallion (weeks 5–8) |
| [`example_4_group_by/`](example_4_group_by/) | 4 yearly sales files (1M rows total), used in Lab 1.2 |
| [`example_5_ranking/`](example_5_ranking/) | [Ranking functions](example_5_ranking/ranking_functions.md): preview for week 2 |
| [`understanding_GROUP_BY/`](understanding_GROUP_BY/) | GROUP BY explained step by step |

## ⚙️ Setup

You need DuckDB and Python with `duckdb pandas matplotlib marimo` (see [Required software](../../course_information/required_software.md)).

- Every notebook is a **Marimo** notebook (`.py`): open it from its own folder, e.g. `marimo edit week01_notebook_2.py`.
- Notebooks read data with **relative paths**; the lecture notebooks read `../example_1_insurance/insurance.csv`.

## ✅ Before week 2

- Finish any lab questions you did not complete in class.
- Optional: try the 14 questions in [Example 2](example_2_group_by/) without looking at the notebook.
