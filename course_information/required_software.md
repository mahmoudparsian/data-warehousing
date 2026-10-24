# Required Software

Step-by-step setup (and a notebook to check it): [Week 0: Software setup](../syllabus/week00-outline-and-TOC/README.md).

------
## 1. [DuckDB](https://duckdb.org/docs/installation/)

* The database for the whole course: the CLI (`duckdb`) and the Python package (`pip install duckdb`)
* Keep **one DuckDB version** for the CLI and Python: a database file written by a newer version can't be opened by an older one

------

## 2. [Python](https://www.python.org) 3.11+

* `pip install duckdb pandas matplotlib seaborn`
* Extras for the week 2 EDA examples: `pip install openpyxl scipy plotly`

------

## 3. [Marimo](https://marimo.io) notebooks

* All course notebooks and the in-class lab notebooks are Marimo notebooks (`.py` files)
* `pip install marimo`, then `marimo edit <notebook>.py` from the notebook's folder

------

## 4. [Tableau](https://www.tableau.com)

* Dashboards, from week 4 on (Tableau Desktop / Public, free with a student license)
* No Tableau? The same charts in Python (pandas + matplotlib) are accepted

------

## 5. Optional

* [MySQL](https://dev.mysql.com/downloads/mysql/): only for the MySQL **reference** examples (week 3 ETL example, week 4 vacation-rental example, bonus module)
* An OpenAI API key, only for the optional bonus module (LLM + SQL)
* A shell (Terminal / PowerShell), for running the DuckDB CLI
