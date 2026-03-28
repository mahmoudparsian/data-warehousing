## Data Warehousing & BI
### Slowly Changing Dimensions (SCD) – Type 2


---

## Slide 1 – What Is a Slowly Changing Dimension (SCD)?

A **Slowly Changing Dimension (SCD)** is a dimension table 
where **attribute values change over time**, but not frequently.

**Examples:**

- Customer changes address
- Employee changes department
- Product changes category

**Key question:**
> Do we need to keep historical values when dimension data changes?

---

## Slide 2 – Why Do Dimension Changes Matter?

Business analytics often asks **historical questions**:

- What were sales **when the customer lived in Boston**?
- How much revenue did a product generate **before reclassification**?

❌ If we overwrite dimension values, **history is lost**.

---

## Slide 3 – What Is SCD Type 2?

**Slowly Changing Dimension Type 2**:

- Preserves **full historical changes**
- Inserts a **new row** when a change occurs
- Assigns a **new surrogate key**
- Keeps old records unchanged

➡️ This is the **most commonly used SCD type** in data warehouses.

---

## Slide 4 – Core Idea of SCD Type 2

> **One business entity → multiple dimension rows over time**

Each row represents the state of the entity during a specific time period.

✔ Facts always point to the **correct historical version**

---

## Slide 5 – Customer Example (Before Change)

**dim_customer**

| customer_key | customer_id | name  | city   |
|-------------|-------------|-------|--------|
| 101         | C123        | Alice | Boston |

- `customer_id` → Natural key
- `customer_key` → Surrogate key

---

## Slide 6 – Customer Example (After Change – Type 2)

Customer moves from **Boston → Seattle**

**dim_customer**

| customer_key | customer_id | name  | city    | start_date | end_date   | is_current |
|-------------|-------------|-------|---------|------------|------------|------------|
| 101         | C123        | Alice | Boston  | 2020-01-01 | 2023-06-30 | N |
| 205         | C123        | Alice | Seattle | 2023-07-01 | NULL       | Y |

✔ Same natural key
✔ New surrogate key
✔ Full history preserved

---

## Slide 7 – How the Fact Table Uses SCD Type 2

**fact_sales**

| sale_id | customer_key | sales_amount |
|--------|--------------|--------------|
| 1      | 101          | 200.00 |
| 2      | 205          | 350.00 |

- Sale 1 → Customer in **Boston**
- Sale 2 → Customer in **Seattle**

✔ No updates needed to fact table

---

## Slide 8 – Key Characteristics of SCD Type 2

- New row created on change
- New surrogate key assigned
- Old rows remain unchanged
- History fully preserved
- Fact table integrity maintained

---

## Slide 9 – Typical Columns in Type 2 Dimensions

Most Type 2 dimension tables include:
- `surrogate_key`
- `natural_key`
- `start_date`
- `end_date`
- `is_current` flag (optional)

These help track **validity periods**.

---

## Slide 10 – SCD Types Comparison 


| Type | Description | History |
|----|------------|--------|
| Type 0 | Ignore changes | ❌ |
| Type 1 | Overwrite values | ❌ |
| Type 2 | Insert new row | ✅ |
| Type 3 | Limited history | ⚠️ |

---

## Slide 11 – When Should You Use SCD Type 2?

Use Type 2 when:
- Historical accuracy matters
- Business reporting depends on past states
- Compliance or auditing is required

Examples:
- Customer address
- Employee role
- Product category

---

## Slide 12 – One-Line Answer

> **SCD Type 2 preserves full history by inserting a new row with a new surrogate key whenever a dimension attribute changes.**

---

## Slide 13 – Key Takeaway

> **If history matters → use SCD Type 2**

---

## End of Slides

