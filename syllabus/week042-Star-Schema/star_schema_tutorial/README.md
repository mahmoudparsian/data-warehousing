# Star Schema End-to-End Teaching Bundle

Generated on: 2026-02-12

## Contents
- 01_oltp_100k_data_generator_mysql.sql
- 02_dw_star_schema_mysql.sql
- 03_etl_oltp_to_dw_mysql.sql
- 04_olap_queries_star_schema.sql
- 05_student_lab_workbook_exercises_solutions.md
- 05b_lab_workbook_only_exercises_solutions.md
- 06_star_schema_teaching_slides.pptx
- 07_star_schema_textbook.pdf

## Run Order (Recommended)
1) Run `01_oltp_100k_data_generator_mysql.sql` (creates & populates `oltp_demo`)
2) Run `02_dw_star_schema_mysql.sql` (creates `dw_demo`)
3) Run `03_etl_oltp_to_dw_mysql.sql` (loads dims + fact into `dw_demo`)
4) Run `04_olap_queries_star_schema.sql` (analysis practice)

## Tip
For classroom use, remove “Solutions” sections from lab files to create a student-only version.
