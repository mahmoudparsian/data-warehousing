# Required Software

Step-by-step setup (and a notebook to check it): [Week 0: Software setup](../weeks/week00-outline-and-TOC/README.md).

------
## 1. [DuckDB](https://duckdb.org/docs/installation/)

* The database for the whole course: the CLI (`duckdb`) and the Python package (`pip install "duckdb>=2.0"`)
* **DuckDB 2.0 or newer** for both (it needs Python 3.11+): `duckdb --version` and
  `python3 -c "import duckdb; print(duckdb.__version__)"` must both start with **2.**
* Keep **one DuckDB version** for the CLI and Python: a database file written by a newer version can't be opened by an older one
* Installing the CLI — Mac: `brew install duckdb`. Windows: **not** `winget` (its DuckDB package stops at 1.5.6); download it by hand,
  step by step in [Week 0: Windows: install the DuckDB CLI 2.0](../weeks/week00-outline-and-TOC/README.md#windows-install-the-duckdb-cli-20)

------

## 2. [Python](https://www.python.org) 3.11+

* `pip install "duckdb>=2.0" pandas matplotlib seaborn`
* Extras for the week 2 EDA examples: `pip install openpyxl scipy plotly`

------

## 3. [Marimo](https://marimo.io) notebooks

* All course notebooks and the in-class lab notebooks are Marimo notebooks (`.py` files)
* `pip install marimo sqlglot` (`sqlglot` runs the SQL cells), then `marimo edit <notebook>.py` from the notebook's folder

------

## 4. [Tableau](https://www.tableau.com)

* Dashboards, from week 4 on (Tableau Desktop / Public, free with a student license)
* No Tableau? The same charts in Python (pandas + matplotlib) are accepted

------

## 5. Optional

* [MySQL](https://dev.mysql.com/downloads/mysql/): only for the MySQL **reference** examples (week 3 ETL example, week 4 vacation-rental example, bonus module)
* An OpenAI API key, only for the optional bonus module (LLM + SQL)
* A shell (Terminal / PowerShell), for running the DuckDB CLI
