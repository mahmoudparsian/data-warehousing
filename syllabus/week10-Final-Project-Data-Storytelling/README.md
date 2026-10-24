# Week 10 — Final Project & Data Storytelling

**Block D · Wrap-up (weeks 9–10)**

A warehouse is only worth what it changes in a decision. This week we take the pizza shop's finished Gold layer
(weeks 6–9) and turn it into a **story**: KPIs defined precisely, fair (like-for-like) comparisons, growth broken into
drivers, numbers sanity-checked, an honest dashboard, and **one** recommendation. Then you do the same for your
own project in the **final presentations**.

## 🎯 Learning objectives

By the end of the week you can:

1. Write a KPI card (formula, grain, additivity) for every number you present.
2. Compare like with like (same scope, same periods) and separate new scope from growth.
3. Decompose a headline into drivers (e.g. orders × items per order × price per item).
4. Check surprising numbers against the raw distribution before presenting them.
5. Build a dashboard from a mart of additive parts, with ratios computed as ratios of sums.
6. Tell a one-slide Situation → Complication → Resolution story with caveats.

## 📅 Sessions

| Session | Topic | Material | Lab (30 min) |
|---|---|---|---|
| 1 | Why DW + Medallion, KPIs, storytelling · **final project presentations (part 1)** | [slides 1: KPIs & storytelling](week10_slides_1_kpis_and_storytelling.md) · [slides 2: story from Gold](week10_slides_2_story_from_gold.md) (Steps 1–4) | [Lab 10.1](labs/week_10_lab_01_student.md): the pizza shop's 2016 story · notebook [`week_10_lab_01_student.py`](labs/week_10_lab_01_student.py) |
| 2 | Honest dashboards, the one-slide story · **final project presentations (part 2)** | [slides 2](week10_slides_2_story_from_gold.md) (Steps 5–7 + checklist) · [project checklist (week 9)](../week09-End-to-End-Pipeline-and-Project-Workshop/project_workshop_checklist.md) | [Lab 10.2](labs/week_10_lab_02_student.md): KPI mart, Tableau, one slide · notebook [`week_10_lab_02_student.py`](labs/week_10_lab_02_student.py) |

## 📂 What's in this folder

| Folder / file | Contents |
|---|---|
| [`labs/`](labs/) | Labs 10.1 and 10.2 (sheet `.md` + Marimo notebook, released in class) · `week_10_lab_setup.sql` (builds the **final** pizza warehouse: both channels, 2015–2016, with week 9's June correction, plus the week-8 marts) |
| `week10_notebook_medallion.py` | A compact end-to-end example on messy insurance data: Bronze → Silver → Gold → KPI, then a Day-2 incremental run showing **KPI drift** (naive vs sliding window) |
| [`insurance_bronze_raw.csv`](insurance_bronze_raw.csv) · [metadata](insurance_bronze_raw.metadata.md) | The small messy dataset used by the notebook |
| [`insurance_infographic.jpg`](insurance_infographic.jpg) | An example of a one-page visual summary (infographic) |

## 🎤 Final project presentations

In **both** sessions of week 10, after the lab: **10 minutes + 3 minutes of questions** per team (teams are assigned to a session in class).

- Requirements and grading: [`../PROJECT/DW_Project_Guidelines.md`](../PROJECT/DW_Project_Guidelines.md)
- Before you present, go through the **final-presentation checklist** at the end of [slides 2](week10_slides_2_story_from_gold.md),
  and make sure every step of the [project checklist](../week09-End-to-End-Pipeline-and-Project-Workshop/project_workshop_checklist.md) is done.

## ⚙️ Setup

```bash
cd labs
duckdb pizza.duckdb < week_10_lab_setup.sql
```
Start with `SET TimeZone = 'UTC';`. Tableau Desktop/Public for Lab 10.2.
