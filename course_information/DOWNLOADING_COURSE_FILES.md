# Downloading Course Files

[← Course home](../README.md) · **Course information**

## 📦 One ZIP File per Week — No Git Needed

You do **not** need git. Each week of the course is ready as **one ZIP file**: slides, notebooks, data, and — once they are
released in class — that week's labs. Click a link, unzip the file, and you have everything for that week, **including the
data from earlier weeks that its notebooks and labs read** (for example, weeks 7–10 include week 6's pizza-shop data).

## ⬇️ Weeks

| Week | Topic | Download |
|:---:|---|---|
| 0 | Course outline & software setup | [`week00-outline-and-TOC.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week00-outline-and-TOC.zip) |
| 1 | Foundations of SQL for Analytics | [`week01-Foundations-SQL-for-Analytics.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week01-Foundations-SQL-for-Analytics.zip) |
| 2 | SQL Analytical Thinking & Exploratory Data Analysis | [`week02-SQL-Analytical-Thinking-and-EDA.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week02-SQL-Analytical-Thinking-and-EDA.zip) |
| 3 | Classic Data Warehousing & ETL | [`week03-Classic-Data-Warehousing.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week03-Classic-Data-Warehousing.zip) |
| 4 | Star Schema in Depth & OLAP | [`week04-Star-Schema-and-OLAP.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week04-Star-Schema-and-OLAP.zip) |
| 5 | Medallion Architecture: Introduction | [`week05-Medallion-Architecture-Introduction.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week05-Medallion-Architecture-Introduction.zip) |
| 6 | Bronze in Depth & Silver Cleaning | [`week06-Bronze-and-Silver-Cleaning.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week06-Bronze-and-Silver-Cleaning.zip) |
| 7 | Silver: Conforming & Integrating Sources | [`week07-Silver-Layer-Cleaning-and-Conforming.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week07-Silver-Layer-Cleaning-and-Conforming.zip) |
| 8 | Gold Layer & Star Schema | [`week08-Gold-Layer-Star-Schema.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week08-Gold-Layer-Star-Schema.zip) |
| 9 | End-to-End Pipeline, Incremental Processing & Project Workshop | [`week09-End-to-End-Pipeline-and-Project-Workshop.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week09-End-to-End-Pipeline-and-Project-Workshop.zip) |
| 10 | Final Project & Data Storytelling | [`week10-Final-Project-Data-Storytelling.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/week10-Final-Project-Data-Storytelling.zip) |
| Project | Team project guidelines | [`PROJECT.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/PROJECT.zip) |
| Bonus | *Optional:* LLM + SQL Integration | [`bonus-LLM-SQL-Integration.zip`](https://github.com/mahmoudparsian/data-warehousing/releases/download/weekly-zips/bonus-LLM-SQL-Integration.zip) |

**Labs:** a week's labs are released in class, at the start of the session. About a minute later, that week's ZIP holds them
too (in its `labs/` folder). Download the ZIP again after the release.

## 🗂️ What Is Inside a ZIP File

Each ZIP file holds **one folder**, laid out exactly like the course repository, so every notebook finds its data:

```
week07-Silver-Layer-Cleaning-and-Conforming.zip
└── MSIS-2419-week07-Silver-Layer-Cleaning-and-Conforming/
    └── syllabus/
        ├── week07-Silver-Layer-Cleaning-and-Conforming/      ← the week: slides, notebook, labs/
        └── week06-Bronze-and-Silver-Cleaning/
            └── pizza_sales_medallion/data/                   ← week 6 data the labs read
```

Keep the folders exactly as they come out of the ZIP — don't move a notebook out of its folder, or it can't find its data.

## 🍎 On a MacBook

Example: week 7's first lab.

1. Click the link. The file goes to your **Downloads** folder.
2. Double-click the ZIP file. macOS creates the folder `MSIS-2419-week07-Silver-Layer-Cleaning-and-Conforming` next to it.
3. Open **Terminal** and go into the week's `labs/` folder:

   ```bash
   cd ~/Downloads/MSIS-2419-week07-Silver-Layer-Cleaning-and-Conforming/syllabus/week07-Silver-Layer-Cleaning-and-Conforming/labs
   ```

4. Open the lab notebook with Marimo:

   ```bash
   marimo edit week_07_lab_01_student.py
   ```

For the week's own notebook, `cd` into the week folder itself (one level up from `labs/`). Each week's `README.md` lists its
notebooks.

## 🪟 On Windows

Example: week 7's first lab.

1. Click the link. The file goes to your **Downloads** folder.
2. Right-click the ZIP file, choose **Extract All…**, then click **Extract**.

   > ⚠️ Do **not** just double-click the ZIP and open the notebooks from there. Windows only shows a preview, and the
   > notebooks cannot find their data. Always **Extract All** first.

3. Windows puts the files in a folder named after the ZIP file, so the path has one extra level. This is normal:

   ```
   Downloads\week07-Silver-Layer-Cleaning-and-Conforming\MSIS-2419-week07-Silver-Layer-Cleaning-and-Conforming\syllabus\week07-Silver-Layer-Cleaning-and-Conforming\labs
   ```

4. Open **PowerShell**, go into that folder (`cd` followed by the path above, starting with `$HOME\Downloads\…`), and run:

   ```powershell
   marimo edit week_07_lab_01_student.py
   ```

If `marimo` is "not recognized", see [Week 0: software setup](../syllabus/week00-outline-and-TOC/README.md).

## 🔄 Getting Updates

The ZIP files are **rebuilt automatically** about one minute after the course files change (for example, when a week's labs
are released). The link always gives the newest version.

If you download a ZIP again, **first save a copy of any file you changed** (for example your lab notebook) — on a Mac the new
download unzips into a new folder (e.g. `MSIS-2419-week07-… 2`); on Windows **Extract All** may ask to replace files.

When the files were last updated: the
[Releases page](https://github.com/mahmoudparsian/data-warehousing/releases/tag/weekly-zips), line **"Last updated"**.

## ❓ Common Questions

**What are "Source code (zip)" and "Source code (tar.gz)" on the Releases page?** GitHub adds these two files to every release.
They hold the **whole** course repository. Ignore them and download a `week…` ZIP instead.

**Can I download `course_information/`, `resources/`, or everything at once?** Not as these ZIPs. For the whole course, use the
green **Code** button on the [repository page](https://github.com/mahmoudparsian/data-warehousing) → **Download ZIP**.

**I already use git. Do I need these ZIPs?** No — `git pull` gives you the same files.

**A link says "Not Found."** Wait a minute and try again (the files are being replaced); if it still fails, tell the
instructor ([office hours](office_hours.md)).

---

*MSIS-2419 — Business Intelligence and Data Warehousing — Winter 2027*
