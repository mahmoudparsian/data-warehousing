
# 📚 Metadata Tutorial in SQL
## Data Warehousing & Relational Databases
Graduate-Level Lecture Slides (Markdown)

---

# Slide 1 — What Is Metadata?

**Metadata = Data about Data**

In SQL systems, metadata describes:

- Tables
- Columns
- Data types
- Constraints
- Indexes
- Relationships
- Statistics
- Security settings

Metadata describes structure — not business facts.

---

# Slide 2 — Data vs Metadata Example

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200),
    signup_date DATE
);
```

### Data (Actual Records)

```sql
SELECT * FROM customers;
```

| customer_id | name  | email        | signup_date |
|-------------|-------|-------------|-------------|
| 1           | Alice | a@email.com | 2023-01-10  |

### Metadata (Structure)

```sql
DESCRIBE customers;
```

---

# Slide 3 — Types of Metadata

1. Structural Metadata  
2. Constraint Metadata  
3. Index Metadata  
4. Statistical Metadata  
5. Security Metadata  
6. Business Metadata  

---

# Slide 4 — INFORMATION_SCHEMA

Standard SQL metadata repository:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'music_dw';
```

---

# Slide 5 — Column Metadata

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'plays';
```

---

# Slide 6 — Constraint Metadata

```sql
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'users';
```

---

# Slide 7 — Index Metadata

```sql
SHOW INDEX FROM plays;
```

Or:

```sql
SELECT index_name, column_name
FROM information_schema.statistics
WHERE table_name = 'plays';
```

---

# Slide 8 — Metadata in a Star Schema

Fact table metadata defines grain.  
Dimension metadata defines hierarchies.

Example SCD metadata:

- effective_date  
- expiry_date  
- is_current  

---

# Slide 9 — Metadata & Query Optimization

```sql
EXPLAIN 
SELECT * 
FROM plays 
WHERE user_key = 100;
```

Execution plans are metadata.

---

# Slide 10 — Metadata-Driven ETL

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'users';
```

Used for dynamic transformations.

---

# Slide 11 — Business vs Technical Metadata

Technical:

- Data types
- Keys
- Indexes

Business:

- Column meaning
- Data owner
- Sensitivity level

---

# Slide 12 — Creating Custom Metadata Table

```sql
CREATE TABLE data_dictionary (
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    description TEXT
);
```

---

# Slide 13 — Metadata in OLAP

Defines roll-up levels:

Year → Quarter → Month → Day

---

# Slide 14 — Metadata & Governance

Supports:

- Lineage
- Auditing
- Access control

---

# Slide 15 — Metadata & Data Quality

```sql
ALTER TABLE users
ADD CONSTRAINT chk_gender
CHECK (gender IN ('MALE','FEMALE'));
```

Constraints are metadata.

---

# Slide 16 — Practical Lab

1. List all tables  
2. List all columns in fact tables  
3. List primary keys  
4. List indexes  
5. Compare table_rows vs COUNT(*)  

---

# Slide 17 — Advanced Metadata Query

Find tables with more than 1M rows:

```sql
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'music_dw'
  AND table_rows > 1000000;
```

---

# Slide 18 — Metadata & Statistics

```sql
ANALYZE TABLE plays;
```

Updates optimizer statistics.

---

# Slide 19 — Metadata vs Master Data

Metadata describes structure.  
Master data describes core business entities.

---

# Slide 20 — Summary

Metadata in SQL:

- Drives database functionality
- Enables optimization
- Supports governance
- Enables automation
- Defines dimensional structure

Without metadata, SQL systems cannot operate.
