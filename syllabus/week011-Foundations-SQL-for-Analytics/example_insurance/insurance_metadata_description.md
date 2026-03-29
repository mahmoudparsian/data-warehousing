# Insurance Dataset — Metadata Description

This dataset contains demographic and health-related attributes of individuals along with their medical insurance charges.

---

## Columns Description

- **age**
  - Type: INTEGER
  - Description: Age of the individual (in years)
  - Business Meaning: Helps analyze how healthcare costs vary across age groups

- **gender**
  - Type: VARCHAR
  - Description: Gender of the individual (male / female)
  - Business Meaning: Used to compare cost differences across genders

- **bmi**
  - Type: FLOAT
  - Description: Body Mass Index (BMI), a measure of body fat
  - Business Meaning: Key health indicator influencing insurance charges

- **children**
  - Type: INTEGER
  - Description: Number of children/dependents covered by insurance
  - Business Meaning: Indicates family size impact on healthcare cost

- **smoker**
  - Type: VARCHAR (yes / no)
  - Description: Whether the individual is a smoker
  - Business Meaning: Major risk factor — strongly affects insurance charges

- **region**
  - Type: VARCHAR
  - Description: Residential region (southwest, southeast, northwest, northeast)
  - Business Meaning: Enables geographic analysis of costs

- **charges**
  - Type: FLOAT
  - Description: Medical insurance cost billed to the individual
  - Business Meaning: Target variable — core metric for analysis

---

## Dataset Summary

- Rows: ~1338
- Columns: 7
- Granularity: One row per individual

---

## Key Business Questions

- How does smoking impact insurance cost?
- Does BMI correlate with higher charges?
- Which region has the highest healthcare expenses?
- Do families (children > 0) incur higher costs?

---
