# MSIS-2419 — Business Intelligence and Data Warehousing

[← Course home](../README.md) · **Syllabus**

**Santa Clara University · Leavey School of Business · Department of Information Systems & Analytics — Graduate Program**<br>
**Winter Quarter 2027 · 4 units · 10 weeks, 20 sessions**

This syllabus collects, in one document, what the course repository
publishes in its separate pages. If this page and a linked page ever
disagree, the linked page in [`course_information/`](./) is the one that
applies, and the instructor will correct this page.

---

## 1. Course Information

| | |
|---|---|
| **Course** | MSIS-2419 — Business Intelligence and Data Warehousing |
| **Units** | 4 (graduate) |
| **Quarter** | Winter 2027: January 4 – March 20, 2027 |
| **Format** | 10 weeks · 20 sessions (2 per week) · 95 minutes per session, each with a 30-minute in-class lab |
| **Meetings** | Mondays and Wednesdays, 5:45–7:20 pm (Pacific Time) · no class on Mon Jan 18 (Martin Luther King Jr. Day) and Mon Feb 15 (Presidents' Day) |
| **Classroom** | *To be announced on Camino* <!-- TODO(syllabus): room --> |
| **Prerequisites** | ISBA 2401 (Data Analytics with Python) and ISBA 2402 / MSIS-2402 (Database Management Systems — Fundamentals of SQL) — see [Prerequisites](prerequisite.md) |
| **Learning management system** | Camino (Canvas) — announcements, Discussions, gradebook |
| **Course materials** | Course repository: <https://github.com/mahmoudparsian/data-warehousing> — or one ZIP per week ([`DOWNLOADING_COURSE_FILES.md`](DOWNLOADING_COURSE_FILES.md)) |

### Instructor

| | |
|---|---|
| **Instructor** | [Dr. Mahmoud Parsian](https://www.scu.edu/business/isa/faculty/parsian/) ([`instructor.md`](instructor.md)) |
| **Email** | [mparsian@scu.edu](mailto:mparsian@scu.edu) |
| **Office** | Lucas Hall, Room 316U |
| **Office hours** | *To be announced on Camino* (Zoom, and by appointment) <!-- TODO(syllabus): office hours --> — see [`office_hours.md`](office_hours.md) |
| **Teaching assistant** | *To be announced* <!-- TODO(syllabus): TA --> |

All quarter dates are kept in one page: [Class Meeting Dates & Hours](class_meeting_dates_hours.md).

---

## 2. Course Description

From the SCU catalog:

> Introduces the business, technology, and managerial issues related to BI and DW
> solutions. Students will acquire practical skills in collecting business
> requirements, planning, defining, designing and developing a BI solution.
> Emphasis is placed on learning how to derive business value from BI and DW
> solutions. Hands-on experience will be obtained using a variety of BI tools.

A data warehouse is a **subject-oriented, integrated, non-volatile, and
time-variant** collection of data in support of management's decisions (Bill
Inmon). This term the course moves through four parts:

1. **SQL for analytics** (weeks 1–2): business questions → SQL → insight; `GROUP BY`,
   `HAVING`, `CASE`, window functions, and exploratory data analysis (EDA) with SQL.
2. **Classic data warehousing** (weeks 3–4): OLTP vs. OLAP, facts, dimensions and grain,
   ETL, star schemas, slowly changing dimensions, OLAP operations (`ROLLUP`, `CUBE`,
   `GROUPING SETS`), and a first Tableau dashboard.
3. **Medallion architecture** (weeks 5–8): Bronze (land everything, with lineage),
   Silver (clean, conform, integrate several sources), and Gold (a star schema, KPIs,
   data marts), on files (a lakehouse) and in a database.
4. **Wrap-up** (weeks 9–10): incremental pipelines (load logs, late data, corrections,
   proving incremental = full rebuild), KPIs that add up, dashboards, data storytelling.

**One running case study:** a pizza shop's sales data, from raw files (weeks 6–7)
through a Gold star schema (week 8) and monthly incremental loads (week 9) to the
final data story (week 10). Every session has a hands-on lab in **DuckDB** with
**Marimo** notebooks; dashboards use **Tableau** or Python charts. Details:
[`course_info_and_desc.md`](course_info_and_desc.md).

---

## 3. Learning Outcomes

By the end of the course, students can:

1. Translate business questions into analytical SQL (aggregation, `CASE`, window functions) and explain the results
2. Profile a dataset (EDA) and turn its problems into explicit data-quality rules
3. Design a star schema: grain, facts, dimensions, surrogate keys, slowly changing dimensions
4. Build ETL / ELT pipelines that are traceable (lineage) and reconcile every row
5. Implement the Medallion architecture (Bronze, Silver, Gold) on files and in a database
6. Conform and integrate data from several sources (mapping tables, time zones, deduplication)
7. Load data incrementally and idempotently, handle late data and corrections, and prove the result
8. Write OLAP queries (roll-up, drill-down, slice, dice, pivot, `ROLLUP` / `CUBE` / `GROUPING SETS`)
9. Define KPIs correctly (additive vs. non-additive measures) and build data marts for business users
10. Build dashboards (Tableau, Python) and present a data story with a recommendation

---

## 4. Course Schedule

Two sessions per week; every session has a **30-minute in-class lab** (20 labs).
Week pages, slides, notebooks and labs: [Weekly schedule](../weeks/README.md) — start with
[Week 0: course outline and software setup](../weeks/week00-outline-and-TOC/README.md).

| Week | Topic | Labs |
|:---:|---|---|
| 1 | Foundations of SQL for Analytics | 1.1 From Business Questions to SQL · 1.2 `GROUP BY`, `HAVING` and `CASE` |
| 2 | SQL Analytical Thinking & Exploratory Data Analysis | 2.1 Window Functions · 2.2 EDA with SQL |
| 3 | Classic Data Warehousing & ETL | 3.1 Your First Star Schema · 3.2 ETL: Extract, Clean and Load |
| 4 | Star Schema in Depth & OLAP | 4.1 Slowly Changing Dimensions · 4.2 OLAP on a Star Schema (and Tableau) |
| 5 | Medallion Architecture: Introduction | 5.1 Your First Medallion Pipeline · 5.2 Medallion as a Lakehouse |
| 6 | Bronze in Depth & Silver Cleaning | 6.1 Bronze in Depth · 6.2 Silver Cleaning |
| 7 | Silver: Conforming & Integrating Sources | 7.1 Conforming a Second Source · 7.2 Integrating Two Sources |
| 8 | Gold Layer & Star Schema | 8.1 Gold: A Star Schema · 8.2 Gold KPIs and Data Marts (and Tableau) |
| 9 | End-to-End Pipeline, Incremental Processing & Project Workshop | 9.1 An Incremental Pipeline · 9.2 Late Data, Corrections, Proving the Pipeline Right |
| 10 | Final Project & Data Storytelling | 10.1 From Gold to a Data Story · 10.2 Dashboard and One-Slide Story |
| Bonus | *Optional:* LLM + SQL Integration | [Bonus module](../weeks/bonus-LLM-SQL-Integration/README.md) |

| Assessment | When |
|---|---|
| **Midterm Exam** | *To be announced on Camino* <!-- TODO(syllabus): midterm date --> — during a class session ([`midterm_exam.md`](midterm_exam.md)) |
| **Final project presentations** | Week 10 ([Project guidelines](../weeks/PROJECT/DW_Project_Guidelines.md)) <!-- TODO(syllabus): presentation dates --> |
| **Final Exam** | *Finals week, to be announced on Camino* <!-- TODO(syllabus): final exam date, time, room --> ([`final_exam.md`](final_exam.md)) |

---

## 5. Required Materials

**Books** ([`required_books.md`](required_books.md)):

1. *Data Warehousing Tutorial* — TutorialsPoint ([online version](https://www.tutorialspoint.com/dwh/index.htm))
2. *Building the Data Lakehouse* — Bill Inmon, Mary Levins, Ranjeet Srivastava ([PDF](https://www.databricks.com/wp-content/uploads/2021/10/The-Data-Lakehouse.pdf))

**Software** — set up before the first lab, following
[Week 0: software setup](../weeks/week00-outline-and-TOC/README.md) (it includes a
notebook that checks your installation). Full list: [`required_software.md`](required_software.md).

| Tool | Used for |
|---|---|
| DuckDB **2.0 or newer** — the CLI and the Python package (`pip install "duckdb>=2.0"`) | The database for the whole course; keep one DuckDB version for both |
| Python **3.11+** with pandas, matplotlib, seaborn (week 2 EDA: openpyxl, scipy, plotly) | Notebooks and charts |
| Marimo | All course notebooks and the in-class lab notebooks |
| Tableau (Desktop / Public, free with a student license) | Dashboards from week 4 (the same charts in Python are accepted) |
| Respondus LockDown Browser ([SCU download](https://download.respondus.com/lockdown/download.php?ID=597745928)) | Midterm and Final Exam |
| *Optional:* MySQL; an OpenAI API key | MySQL reference examples; the optional bonus module |

**A laptop** with the software above, at every session — every session has an in-class lab.

---

## 6. Assessment and Grading

| Component | % of grade |
|---|---:|
| In-class labs — 20 labs (2 per week); the lowest 2 are dropped | 40 |
| Project | 30 |
| — Project documentation / exploratory data analysis | *10* |
| — Project implementation | *10* |
| — Project presentation | *10* |
| Midterm Exam | 10 |
| Final Exam | 20 |
| **Total** | **100** |
| Bonus — for exceptional work, extra credit added on top of the 100 | up to +2 |

### Labs

- 30 minutes each, done **in class**: a lab sheet and a Marimo notebook, released at
  the start of the session. Submit your work as instructed in class.
- The lowest 2 of the 20 lab scores are dropped.

### Project

In teams, students design, build and present a data warehouse on a dataset of their
choice; presentations are in week 10. Details:
[Project guidelines](../weeks/PROJECT/DW_Project_Guidelines.md).

### Exams

The midterm and final exams are **closed book, closed notes, closed software, closed
Internet, closed phone**, and taken in the **Respondus LockDown Browser**. No makeup
exams are given.

### Letter grades

Your course percentage (including any bonus, so at most 102%) is rounded to the
nearest tenth before this table is applied: 93.95 → 94.0 → A; 93.94 → 93.9 → A−.
Any percentage of 94 or higher, including above 100, is an A.

| Letter | Percentage | Letter | Percentage | Letter | Percentage |
|:---:|---|:---:|---|:---:|---|
| A | 94 and above | B− | 80 – 82.9 | D+ | 67 – 69.9 |
| A− | 90 – 93.9 | C+ | 77 – 79.9 | D | 63 – 66.9 |
| B+ | 87 – 89.9 | C | 73 – 76.9 | D− | 60 – 62.9 |
| B | 83 – 86.9 | C− | 70 – 72.9 | F | below 60 |

Full policy: [`grading_and_class_conduct.md`](grading_and_class_conduct.md).

---

## 7. Late Work

**No late labs or project deliverables are accepted**, under any circumstances.
Labs are done and submitted in class.

---

## 8. Attendance

Attendance is expected. Students are responsible for all missed work, notes and
materials, regardless of the reason for the absence. The in-class labs are done
during the session; the lowest 2 lab scores are dropped.

---

## 9. Accessibility and Accommodations

If you have a documented disability for which accommodations may be required in
this class, contact the **Office of Accessible Education (OAE)** —
<https://www.scu.edu/oae/> — as early as possible to arrange accommodations, and
share your accommodation letter with the instructor.

---

## 10. Academic Integrity and Conduct

- **Your own work.** You may get help from anyone and any resource to understand how
  to solve your work, but what you submit must be yours alone; copying a solution is
  plagiarism and will be reported. Exchanging ideas is fine; exchanging detailed
  solutions is not ([`academic_integrity.md`](academic_integrity.md),
  [`grading_and_class_conduct.md`](grading_and_class_conduct.md)).
- **SCU Academic Integrity:** <https://www.scu.edu/academic-integrity/>
- **Plagiarism:** [SCU library guide](https://libguides.scu.edu/plagiarism/conduct)
- **Discrimination, harassment, and sexual misconduct:** Santa Clara University does
  not tolerate them. Information, reporting options, and support:
  <https://www.scu.edu/title-ix/>.

---

## 11. Getting Help

| Need | Where |
|---|---|
| A question about course content | Ask in class, come to office hours, post on **Camino Discussions** (students, the TA, and the instructor respond), or [email the instructor](mailto:mparsian@scu.edu) |
| Installing the course software | [Week 0: software setup](../weeks/week00-outline-and-TOC/README.md) · [`required_software.md`](required_software.md) |
| SQL or Python refreshers | [`sql_tutorials.md`](sql_tutorials.md) · [`python_tutorials.md`](python_tutorials.md) · [`sql_style_guide.md`](sql_style_guide.md) |
| LockDown Browser or other SCU technology | SCU Technology Help: (408) 554-5700, or a [Computing Support Request](https://help.scu.edu/TDClient/111/Portal/Home/) |

---

## 12. Course Documents

| Document | Contents |
|---|---|
| [`course_info_and_desc.md`](course_info_and_desc.md) | Course information, description, learning outcomes |
| [`class_meeting_dates_hours.md`](class_meeting_dates_hours.md) | All quarter dates in one place |
| [`DOWNLOADING_COURSE_FILES.md`](DOWNLOADING_COURSE_FILES.md) | One ZIP per week, no git needed |
| [`grading_and_class_conduct.md`](grading_and_class_conduct.md) | Grading, letter grades, course policies |
| [`midterm_exam.md`](midterm_exam.md) · [`final_exam.md`](final_exam.md) | The exams |
| [`office_hours.md`](office_hours.md) | Office hours and how to ask questions |
| [`prerequisite.md`](prerequisite.md) | What you need to know before the course |
| [`required_books.md`](required_books.md) · [`required_software.md`](required_software.md) | Books and software |
| [`academic_integrity.md`](academic_integrity.md) | Academic integrity |
| [Weekly schedule](../weeks/README.md) | Week pages, slides, notebooks, labs |
| [Project guidelines](../weeks/PROJECT/DW_Project_Guidelines.md) | The team project |

---

*MSIS-2419 — Business Intelligence and Data Warehousing — Winter 2027*
