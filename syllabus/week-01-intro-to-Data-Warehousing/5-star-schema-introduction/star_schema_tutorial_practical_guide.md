# Star Schema Tutorial (Practical, Hands-On Guide)

## 1. What Is a Star Schema?

A **star schema** is a data warehouse modeling technique where:

- One central table (**fact table**) stores business measurements
- Multiple surrounding tables (**dimension tables**) store descriptive context
- The structure visually resembles a ⭐ star

The design is optimized for **analytics, reporting, and BI tools**.

---

## 2. Core Concept (Very Important)

> **Facts = measurements (numbers)**  
> **Dimensions = context (who, what, when, where, how)**

If you remember only one rule:

| Question | Table Type |
|--------|------------|
| How much? | Fact |
| How many? | Fact |
| Who? | Dimension |
| When? | Dimension |
| Where? | Dimension |
| What kind? | Dimension |

---

## 3. Fact Tables vs Dimension Tables

### Fact Table Characteristics

- Very large (millions or billions of rows)
- Contains **numeric measures**
- Contains **foreign keys** to dimensions
- Changes frequently
- Used for aggregations (SUM, COUNT, AVG)

### Dimension Table Characteristics

- Smaller tables
- Mostly descriptive columns (text, categories)
- Contains attributes used for filtering and grouping
- Changes slowly
- Reused across many fact tables

---

## 4. Practical Example: Retail Sales

### Business Questions

- Total sales per country per year
- Top 5 products per category
- Monthly revenue by store
- Quarterly revenue by store
- Top-10 customers year by year

These questions drive the schema design.

---

## 5. Dimension Tables

### 5.1 Date Dimension

```sql
CREATE TABLE dim_date (
  date_id        INT PRIMARY KEY,
  full_date      DATE,
  day            INT,
  month          INT,
  month_name     VARCHAR(20),
  quarter        INT,
  year           INT,
  is_weekend     BOOLEAN
);
```

**Why this exists:**
- Used in nearly every query
- Avoids repeated date calculations
- One row per calendar date

---

### 5.2 Product Dimension

```sql
CREATE TABLE dim_product (
  product_id     INT PRIMARY KEY,
  product_name   VARCHAR(100),
  category       VARCHAR(50),
  brand          VARCHAR(50)
);
```

**Describes:** what was sold

---

### 5.3 Customer Dimension

```sql
CREATE TABLE dim_customer (
  customer_id    INT PRIMARY KEY,
  customer_name  VARCHAR(100),
  gender         VARCHAR(10),
  age_group      VARCHAR(20),
  country        VARCHAR(50),
  city           VARCHAR(50)
);
```

**Describes:** who bought

---

### 5.4 Store Dimension

```sql
CREATE TABLE dim_store (
  store_id       INT PRIMARY KEY,
  store_name     VARCHAR(100),
  store_type     VARCHAR(20),
  country        VARCHAR(50),
  region         VARCHAR(50)
);
```

**Describes:** where the sale occurred

---

## 6. Fact Table

### Sales Fact Table

```sql
CREATE TABLE fact_sales (
  sales_id       BIGINT PRIMARY KEY,
  date_id        INT,
  product_id     INT,
  customer_id    INT,
  store_id       INT,

  quantity       INT,
  unit_price     DECIMAL(10,2),
  total_amount   DECIMAL(12,2),

  FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
  FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);
```

**Why this is a fact table:**
- One row = one business event (a sale)
- Contains measurable values
- Contains only keys to descriptive tables

---

## 7. Query Examples (This Is the Payoff)

### 7.1 Total Sales by Country and Year

```sql
SELECT
  c.country,
  d.year,
  SUM(f.total_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY c.country, d.year;
```

---

### 7.2 Top Products per Category

```sql
SELECT
  p.category,
  p.product_name,
  SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category, p.product_name
ORDER BY revenue DESC
LIMIT 5;
```

---

## 8. Why Not One Big Table?

### Bad Design (Single Wide Table)

```text
sales_id, date, year, month, product_name, category,
customer_name, country, store_name, quantity, price, amount
```

### Problems

- Massive data duplication
- Hard to maintain
- Slow queries
- Difficult to handle changes

---

## 9. Advantages of Star Schema

| Benefit | Explanation |
|-------|------------|
| Fast queries | Simple joins |
| Less storage | Dimension reuse |
| Clean design | Clear separation of concerns |
| BI friendly | Works well with Tableau, Power BI |
| Scalable | Handles very large fact tables |

---

## 10. Another Example: Credit Card Transactions

### Fact Table

```sql
fact_transactions(
  transaction_id,
  date_id,
  card_id,
  merchant_id,
  amount,
  transaction_count
)
```

### Dimensions

- dim_date
- dim_cardholder
- dim_merchant
- dim_location

Same pattern, different business.

---

## 11. Common Beginner Mistakes

- Putting customer names in fact tables
- Storing year/month as strings in fact tables
- Mixing descriptive text with numeric measures
- Creating one giant dimension table

---

## 12. Final Mental Checklist

Before creating a table, ask:

1. Is this a number to aggregate? → FACT
2. Is this descriptive text? → DIMENSION
3. Does it answer who/when/where/what? → DIMENSION
4. Does it change often? → FACT
5. Does it change slowly? → DIMENSION

---

## 13. Summary

- Fact tables store measurements
- Dimension tables store descriptive context
- Star schema is simple, fast, and scalable
- Design always starts from business questions

---

**End of tutorial**

