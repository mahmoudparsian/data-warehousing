# Business Intelligence and Data Warehousing

**MSIS-2419 · Winter Quarter 2027 (January–March)** · Department of Information Systems & Analytics, Santa Clara University

## 1. Course Information

**Catalog:** 4 units · graduate · 10 weeks, 2 sessions per week (100 minutes each).
*Introduces the business, technology, and managerial issues related to BI and DW solutions. Students will acquire practical skills in collecting business requirements, planning, defining, designing and developing a BI solution. Emphasis is placed on learning how to derive business value from BI and DW solutions. Hands-on experience will be obtained using a variety of BI tools.*
**Prerequisites:** ISBA 2401 (Data Analytics with Python) and ISBA 2402 (Database Management Systems — Fundamentals of SQL). See [Prerequisites](prerequisite.md).


1. A data warehouse is a

   1. subject-oriented,
   2. integrated,
   3. non-volatile, and
   4. time-variant

   collection of data in support of management's decisions (Bill Inmon).

2. This course introduces the business, technology and managerial issues of business intelligence (BI) and
   data warehousing (DW). Students acquire practical skills in collecting business requirements, planning,
   designing and building a BI solution, with emphasis on deriving **business value** from it.

3. A data warehouse is the central component of a modern data stack: the tools that collect, clean, integrate,
   store and serve data for reporting, analysis and machine learning.

## 2. Course Description

1. **SQL for analytics (weeks 1–2):** questions → SQL → insight; `GROUP BY`, `HAVING`, `CASE`, window functions,
   and exploratory data analysis (EDA) with SQL.

2. **Classic data warehousing (weeks 3–4):** OLTP vs OLAP, facts, dimensions and grain, ETL, star schemas,
   slowly changing dimensions, and OLAP operations (`ROLLUP`, `CUBE`, `GROUPING SETS`), with a first Tableau dashboard.

3. **Medallion architecture (weeks 5–8):** Bronze (land everything, with lineage), Silver (clean, conform and integrate
   several sources), and Gold (a star schema, KPIs and data marts), on files (a lakehouse) and in a database.

4. **Wrap-up (weeks 9–10):** incremental pipelines (load logs, late data, corrections, proving incremental = full rebuild),
   KPIs that add up, dashboards, and data storytelling.

5. **One running case study:** a pizza shop's sales data, from raw files (weeks 6–7), through a Gold star schema (week 8)
   and monthly incremental loads (week 9), to the final data story (week 10).

6. **Hands on, every session:** a 30-minute in-class lab in every session (20 labs), in **DuckDB** with **Marimo** notebooks,
   plus **Tableau** and Python charts for dashboards.

7. **Project:** in teams, students design, build and present a data warehouse on a dataset of their choice
   ([project guidelines](../syllabus/PROJECT/DW_Project_Guidelines.md)).

## 3. Learning Outcomes

By the end of the course, students can:

1. Translate business questions into analytical SQL (aggregation, `CASE`, window functions) and explain the results
2. Profile a dataset (EDA) and turn its problems into explicit data-quality rules
3. Design a star schema: grain, facts, dimensions, surrogate keys, slowly changing dimensions
4. Build ETL / ELT pipelines that are traceable (lineage) and reconcile every row
5. Implement the Medallion architecture (Bronze, Silver, Gold) on files and in a database
6. Conform and integrate data from several sources (mapping tables, time zones, deduplication)
7. Load data incrementally and idempotently, handle late data and corrections, and prove the result
8. Write OLAP queries (roll-up, drill-down, slice, dice, pivot, `ROLLUP`/`CUBE`/`GROUPING SETS`)
9. Define KPIs correctly (additive vs non-additive measures) and build data marts for business users
10. Build dashboards (Tableau, Python) and present a data story with a recommendation
