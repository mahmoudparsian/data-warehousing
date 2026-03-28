# From Transactional Database to Star Schema

## Including SCD Type 2 Implementation

### Complete Teaching Guide (Retail Example)

### Topics:

	 1. Full OLTP → Star schema steps
	 2. Proper grain definition
	 3. Dimension modeling
	 4. Fact table design
	 5. Complete SCD Type 2 implementation
	 6. Expire/Insert logic
	 7. Date-range fact joins
	 8. Historical accuracy explanation
	 9. OLAP example queries
	10. Teaching checklist
------------------------------------------------------------------------

# 1️⃣ Business Scenario

We begin with a transactional retail system that captures:

-   Customers
-   Products
-   Stores
-   Orders
-   Order Items

Goal: Build a **Star Schema** optimized for analytics and implement
**Slowly Changing Dimension (SCD) Type 2** for historical tracking.

------------------------------------------------------------------------

# 2️⃣ Original OLTP Schema (Normalized)

## customers

``` sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    created_at DATETIME
);
```

------------------------------------------------------------------------

## products

``` sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2)
);
```

------------------------------------------------------------------------

## stores

``` sql
CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);
```

------------------------------------------------------------------------

## orders

``` sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    store_id INT,
    order_date DATETIME,
    channel VARCHAR(20)
);
```

------------------------------------------------------------------------

## order_items

``` sql
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2)
);
```

------------------------------------------------------------------------

# 3️⃣ Define the Grain (Critical Step)

🎯 Grain = **One row per order line item**

This ensures: 

- Maximum analytical flexibility 
- No double counting 
- Proper aggregation

------------------------------------------------------------------------

# 4️⃣ Identify Measures

From `order_items`:

-   `quantity`
-   `unit_price`
-   `sales_amount` = `quantity × unit_price`

------------------------------------------------------------------------

# 5️⃣ Identify Dimensions

-   `dim_customer`
-   `dim_product`
-   `dim_store`
-   `dim_date`
-   `dim_channel`

------------------------------------------------------------------------

# 6️⃣ Star Schema Design

## ⭐ fact_sales

``` sql
CREATE TABLE fact_sales (
    sales_key BIGINT PRIMARY KEY AUTO_INCREMENT,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    channel_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    sales_amount DECIMAL(12,2)
);
```

------------------------------------------------------------------------

# 7️⃣ Implementing SCD Type 2 for dim_customer

## Why SCD Type 2?

We want to preserve history when customer attributes change.

Example: Customer moves from CA → TX.

**We MUST:**

- Keep old record (CA) 
- Insert new record (TX) 
- Mark old record as expired

------------------------------------------------------------------------

## dim_customer (SCD Type 2 Structure)

``` sql
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    effective_date DATE,
    expiry_date DATE,
    is_current CHAR(1)
);
```

------------------------------------------------------------------------

## Sample Initial Load

| customer_key | customer_id | state | effective_date | expiry_date | is_current |
|--------------|------------|-------|----------------|------------|------------|
| 1            | 1          | CA    | 2024-01-01     | 9999-12-31 | Y          |


## Customer Moves to TX (SCD Type 2 Process)

### Step 1: Expire old record

``` sql
UPDATE dim_customer
SET expiry_date = '2025-03-01',
    is_current = 'N'
WHERE customer_id = 1
  AND is_current = 'Y';
```

### Step 2: Insert new version

``` sql
INSERT INTO dim_customer (
    customer_id,
    first_name,
    last_name,
    city,
    state,
    country,
    effective_date,
    expiry_date,
    is_current
)
VALUES (
    1,
    'Alice',
    'Kim',
    'Dallas',
    'TX',
    'USA',
    '2025-03-01',
    '9999-12-31',
    'Y'
);
```

## After SCD Type 2 Process Update:

#### Before:

| customer_key | customer_id | state | effective_date | expiry_date | is_current |
|--------------|------------|-------|----------------|------------|------------|
| 1            | 1          | CA    | 2024-01-01     | 9999-12-31 | Y          |


#### After:


| customer_key | customer_id | state | effective_date | expiry_date | is_current |
|--------------|-------------|-------|----------------|-------------|------------|
| 1            | 1           | CA    | 2024-01-01     | 2025-03-01  | N          |
| 2            | 1           | TX    | 2025-03-01     | 9999-12-31  | Y          |




------------------------------------------------------------------------

# 8️⃣ ETL Logic with SCD Type 2

Fact table must join to correct dimension version:

``` sql
JOIN dim_customer dc
  ON dc.customer_id = o.customer_id
 AND o.order_date BETWEEN dc.effective_date AND dc.expiry_date
```

This ensures historical accuracy.

------------------------------------------------------------------------

# 9️⃣ Why SCD Type 2 Matters

Without SCD Type 2:

All historical sales would show customer as TX (incorrect).

With SCD Type 2:

```
    Sales before move → CA
    Sales after move → TX
```
Historical integrity preserved.

------------------------------------------------------------------------

# 🔟 Example OLAP Query

``` sql
SELECT
    d.year,
    dc.state,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_customer dc ON f.customer_key = dc.customer_key
GROUP BY d.year, dc.state
ORDER BY d.year, total_sales DESC;
```

# Slowly Changing Dimensions (SCD)

	Slowly Changing Dimensions (SCD) are
	data warehousing techniques used to 
	manage changes in dimension attributes 
	over time. 
	
	Key methods include Type 0 (Fixed), 
	Type 1 (Overwrite), and Type 2 (Full History). 
	Others like Type 3-7 are hybrids used for 
	specialized tracking needs, such as combining 
	current/historical views. 

## SCD Types Explained

### Type 0: Fixed Dimension

        Description: The value never changes, 
        even if the source changes. Ideal for 
        "original" attributes.
        
        Example: 
        				Original_BirthDate,
        				Original_Customer_Acquisition_Date
        				
### Type 1: Overwrite
        
        Description: Replaces old data with new data. 
        No history is kept.
        
        Example: Correcting a misspelled customer name
        (e.g., "Jhon" to "John").
        
### Type 2: Add New Row

        Description: Creates a new row for every change,
        using `Start_Date` and `End_Date` to track validity.
        
        Example: 
        	A customer moves from New York to California; 
        	a new row is added, keeping the old record for
        	past sales.
        	
### Type 3: Add New Column
        
        Description: Tracks changes by adding a 
        "previous" column, keeping only limited 
        history.
        
        Example: `Current_Region` and `Previous_Region` 
        in the same row.
        
### Type 4: History Table

        Description: Maintains a separate table to 
        store all historical changes, while the main 
        table holds the current value.
        
        Example: 
        		`Employee_Data` (current) and 
        		`Employee_History` (full audit trail).

### Type 5: Hybrid (4 + 1)
        Description: Uses Type 4 (separate table) 
        but adds a column in the main table to link 
        to the history, often using a surrogate key 
        to enable Type 1 updates.

### Type 6: Hybrid (2 + 1 + 3)

        Description: Combines Types 2, 3, and 1. 
        It provides a full history (Type 2) while 
        allowing current values to be reflected 
        on historical rows (Type 1) using a 
        `Current_Value` column.

### Type 7: Dual Surrogate/Natural Key

        Description: Similar to Type 2, but the 
        fact table uses both the natural key (for 
        easy querying of current data) and the 
        surrogate key (for historical tracking). 

## Real-World Application Example

Imagine a company tracking employee roles:

    Type 1: Update "Analyst" to "Senior Analyst." 
    Past reports now show "Senior Analyst" for last year.
    
    Type 2: Keep "Analyst" row (active 2023-2024) and 
    add new "Senior Analyst" row (active 2025). 
    Last year's sales are correctly tied to "Analyst."
    
    Type 3: Add `Previous_Role` column. 
    When role changes, Role becomes "Senior Analyst,"
    `Previous_Role` becomes "Analyst." 

------

# 1️⃣1️⃣ Design Checklist

1.  Define grain
2.  Identify measures
3.  Identify dimensions
4.  Create surrogate keys
5.  Implement SCD Type 2 for changing dimensions
6.  Use effective/expiry dates
7.  Join fact using date-range logic
8.  Validate historical reports

------------------------------------------------------------------------

# 🎓 Teaching Notes

-   Grain must be defined first.
-   Surrogate keys are mandatory for SCD Type 2.
-   Never overwrite historical dimension data.
-   Always join fact to dimension using effective dates.
-   Validate with before/after change examples.

------------------------------------------------------------------------

End of Document
