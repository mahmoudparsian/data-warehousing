# DuckDB String & Date Functions <br> Used in Case Study

---

### 1. `UPPER(string)`

What: Converts all characters in a string to uppercase.

Example: `SELECT UPPER('sale'); → 'SALE'`

---

### 2. `LOWER(string)`

What: Converts all characters in a string to lowercase.

Example: `SELECT LOWER('DuckDB'); → 'duckdb'`

---

### 3. `TRIM(string)`

What: Removes leading and trailing whitespace.

Example: `SELECT TRIM(' data '); → 'data'`

---

### 4. `NULLIF(a, b)`

What: Returns NULL if `a` equals `b`; otherwise returns a. 
Often used to turn empty strings (`''`) into NULL.

Example: `SELECT NULLIF('', ''); → NULL`

---

### 5. `TRY_CAST(value AS type)`

What: Attempts to convert a value to a new type. 
Returns NULL instead of crashing if the conversion fails.

Example: `SELECT TRY_CAST('123' AS INTEGER); → 123`

Example (Fail): `SELECT TRY_CAST('abc' AS INTEGER); → NULL`

---

### 6. `EXTRACT(PART FROM date)`

What: Pulls a specific numeric part (Year, Month, Day) 
from a date or timestamp.

Example:

```sql
SELECT 
  EXTRACT(YEAR FROM DATE '2024-05-20') AS the_year,  
  -- 2024
    
  EXTRACT(MONTH FROM DATE '2024-05-20') AS the_month, 
  -- 5
    
  EXTRACT(DAY FROM DATE '2024-05-20') AS the_day;     
  -- 20
...
```

---

### 7. `STRFTIME(date, format)`

What: Converts a date/timestamp to a formatted string.

Example: 

```sql
SELECT STRFTIME(DATE '2024-05-20', '%d/%m/%Y'); 
-- → '20/05/2024'
```




