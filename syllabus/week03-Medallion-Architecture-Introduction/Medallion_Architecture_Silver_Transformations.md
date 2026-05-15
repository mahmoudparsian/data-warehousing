# Common Design Patterns <br> in the Medallion Architecture

* SQL Examples are in [DuckDB](https://duckdb.org)

* `% duckdb --version` <br> 
`v1.5.2 (Variegata)`

* Last Updated at: `2026-05-15`

```
   The  Medallion  Data  Architecture  is  a  design
   pattern  used  to  logically  organize  data in a
   Lakehouse, with the primary goal of incrementally
   improving data quality and  structure as it moves
   through various stages. 
      
   This  architecture  is often called a "multi-hop"
   pattern  because data "hops" from raw to  refined
   states  across three main layers: Bronze, Silver,
   and Gold. 
   
          🟫 Bronze  →  ⚪  Silver  →  🟡  Gold

```

![](./images/building-data-pipelines-with-delta-lake.png)
## The Three Core Layers

Common design patterns within each layer focus 
on specific transformation and storage goals.

### Bronze Layer (Raw Ingestion):

* **Immutability:** <br>
Stores data exactly as it was received from 
source systems to provide an audit trail and 
enable reprocessing.

* **Append-Only:** <br>
New data is typically appended incrementally 
rather than overwriting existing records.

* **Schema Flexibility:** <br>
Minimal validation is performed; fields are 
often stored as flexible types (like `STRING` 
or `VARIANT`) to prevent ingestion failures 
due to source schema changes.

### Silver Layer (Cleansed and Enriched):

* **Standardization & Cleaning:** <br>
This is where data is deduplicated, null 
values are handled, and data types are 
standardized (e.g., converting strings to dates).

* **Normalization:** <br>
Data from different sources may be joined 
and normalized into shared, domain-agnostic 
building blocks. If a company doing sales
in many countries (USA, Europe, China, ...), 
then you convert the `sale_price` to a normalized
value.

* **Data Modeling (Data Vault/Core):** <br>
Some organizations implement [Data Vault](https://www.clarifai.com/blog/medallion-architecture/) 
or similar modeling techniques here to maintain 
historical changes while creating a "single version 
of truth".

### Gold Layer (Curated for Consumption):

* **Dimensional Modeling:** <br>
Data is often organized into Kimball-style 
Star Schemas (Fact and Dimension tables) 
optimized for BI tools.

* **Business Aggregates:** <br>
Contains pre-calculated KPIs and summaries 
(e.g., "daily sales per region") to improve 
query performance for end-users.

* **Project-Specific Views:** <br>
Instead of a single "Gold" database, 
organizations may create multiple gold 
datasets tailored to specific departments 
like HR, Finance, or Marketing.  

## Common Supplementary Patterns
Modern implementations often include additional 
patterns to handle advanced needs: 

### Optional Layers:

* Pre-Bronze/Staging: A temporary landing zone for high-velocity IoT or clickstream data before it is normalized into the formal Bronze layer.
   * Platinum Layer: A specialized layer used for real-time analytics and serving AI/ML models.

### Hybrid Architectures:
* Federated Medallion (Data Mesh): Each business domain (e.g., Marketing, Sales) manages its own internal Bronze-Silver-Gold layers, while central governance connects them as part of a [Data Mesh](https://www.databricks.com/blog/what-is-medallion-architecture).
   * Lambda Pattern: Integrating both batch and streaming ingestion to provide real-time updates through the medallion layers.

### Operational Patterns:
* Data Contracts: Formal agreements between data producers and consumers to enforce schema and quality expectations before data enters the pipeline.
   * Quarantine/Error Handling: Records that fail Silver-layer quality checks are moved to separate "error tables" for investigation rather than stopping the entire pipeline.  

## Silver Layer Transformations

Let's say that we have ingested raw data 
(Bronze layer) as a `sales_raw` table: to 
move into a sliver layer, what are the 
concrete common examples of SQL operations 
to move to silver layer?

* Moving from the Bronze to the Silver layer is 
where you transition from **"data as it is"** 
to **"data as it should be."** 

* This phase focuses on cleaning, standardizing, 
and deduplicating records to ensure high data 
quality for downstream use. 

The following `SQL` operations are common patterns 
for transforming a `sales_raw` table into a 
`sales_silver` table:

## 1. Data Type Casting and Standardization
Raw ingestion often treats everything as 
`STRING` or `VARIANT` to avoid load failures. 
In Silver, you enforce strict schemas. 

* Operations: Casting strings to `DATE` or 
`TIMESTAMP`, and ensuring numeric values 
like price or tax are stored as DECIMAL.

* Example:

```sql
SELECT 
    
    -- Convert order_id into BIGINT 
    -- for numeric consistency
    order_id::BIGINT AS order_id,

    -- Parse text date using YYYY-MM-DD format 
    -- and convert to DATE type
    strptime(order_date, '%Y-%m-%d')::DATE AS order_date,

    -- Remove extra spaces and standardize 
    -- currency codes to uppercase
    UPPER(TRIM(currency_code)) AS currency_code,

    -- Convert total_amount into a financial decimal 
    -- format with 2 decimal places
    total_amount::DECIMAL(18,2) AS total_amount

FROM sales_raw;
```


## 2. Deduplication (Window Functions)
Raw sales data often contains duplicates due 
to retries or late-arriving records.

* Operations: Use `ROW_NUMBER()` over a unique 
business key (e.g., `order_id`) to pick the most 
recent version based on an ingestion timestamp.

* Example:

```sql
SELECT *
FROM sales_raw
QUALIFY ROW_NUMBER() OVER(
   PARTITION BY order_id 
   ORDER BY _ingested_at DESC
) = 1;
```

OR

```
WITH deduped_sales AS (
    SELECT 
        *, 
        ROW_NUMBER() OVER(
            PARTITION BY order_id 
            ORDER BY _ingested_at DESC
        ) as rn
    FROM sales_raw
)
SELECT 
    * EXCLUDE (rn)  
    -- DuckDB specific: 
    -- removes the 'rn' column automatically
FROM deduped_sales 
WHERE rn = 1;
```

## 3. Handling Nulls and Missing Values

Decide how to handle missing data—either 
by dropping invalid records or filling 
them with defaults. 

* Operations: `COALESCE` for default values 
or `WHERE` clauses to filter out "trash" data.

* Example:

```sql
SELECT 
    order_id,
    
    -- Ensure customer_id is cast to 
    -- BIGINT to handle the -1 safely
    COALESCE(customer_id::BIGINT, -1) as customer_id, 
    
    -- Ensure region is trimmed of 
    -- whitespace before defaulting
    COALESCE(NULLIF(TRIM(region), ''), 'UNKNOWN') as region
    
FROM sales_raw
WHERE order_id IS NOT NULL;
```


## 4. Enrichment with Reference Tables
While Gold handles complex business logic, 
the Silver layer often adds simple context 
like looking up a product name from a 
master SKU list.

* Operations: LEFT JOIN with reference tables 
to add basic descriptions or categories.

* Example:

```sql
SELECT s.*, 
       p.product_name, 
       p.category
FROM sales_raw s
LEFT JOIN product_reference p ON s.sku = p.sku;
```

## 5. Incremental Upserts (MERGE)
To keep the Silver layer updated without 
re-processing the entire dataset, a MERGE 
statement is used to update existing 
records and insert new ones. 

* Operations: MERGE INTO the target silver 
table using a unique identifier.

* Example:

```sql
MERGE INTO sales_silver AS target
USING cleaned_sales_stream AS source
    ON target.order_id = source.order_id
WHEN MATCHED THEN
    UPDATE SET 
        amount = source.amount, 
        status = source.status
WHEN NOT MATCHED THEN
    INSERT (order_id, amount, status) 
    VALUES (source.order_id, 
            source.amount, 
            source.status);
```

What this code means

* This statement performs an upsert (Update + Insert), 
which synchronizes the `sales_silver` table with the `cleaned_sales_stream` source in a single atomic transaction. 

* `MERGE INTO sales_silver AS target`: Sets `sales_silver` 
as the table to be modified.

* `USING cleaned_sales_stream AS source`: Identifies 
the incoming data source.

* `ON target.order_id = source.order_id`: The join 
condition. It looks for matching `order_id` values 
in both tables.

* `WHEN MATCHED THEN UPDATE SET` ...: If an `order_id` 
already exists in the target, it updates that record's 
amount and status with the new values from the source.

* `WHEN NOT MATCHED THEN INSERT` ...: If the `order_id` 
does not exist in the target, it creates a new record 
using the source data. 



Why this is powerful in a Silver Layer:

* **Atomicity**: The entire operation happens 
in a single transaction. You won't end up with 
a table that is partially updated if the power 
goes out or the script fails.

* **Efficiency**: DuckDB uses its storage engine 
to identify which blocks need updating, making 
it much faster than a manual DELETE followed 
by an INSERT.

* **Handling Late Arrivals**: If a record for 
`order_id: 101` was already in Silver but the 
source system sends an updated price, the 
`WHEN MATCHED` clause ensures the Silver layer 
reflects the most recent truth.


####  Pro-Tip: Adding a "Last Updated" Column
In the Silver layer, it is a best practice to 
track when a record was last modified by the 
pipeline. You can add this directly to your 
`MERGE` statement:

```sql
MERGE INTO sales_silver AS target
USING cleaned_sales_stream AS source
    ON target.order_id = source.order_id
WHEN MATCHED THEN
    UPDATE SET 
        amount = source.amount, 
        status = source.status,
        updated_at = CURRENT_TIMESTAMP  -- Track the change
WHEN NOT MATCHED THEN
    INSERT (order_id, amount, status, updated_at) 
    VALUES (source.order_id, 
            source.amount, 
            source.status, 
            CURRENT_TIMESTAMP);
```

# Common Design Patterns for Silver Layer 

Moving from Bronze to Silver is all about 
**integrity** and **usability**. 

Here are 10 real-world SQL patterns used to turn 
raw sales "dump" data into a reliable source of truth:

## 1. Data Type Enforcement (Casting)

* Raw data often arrives as strings. 
* Silver must enforce the correct types for calculation.

```sql
SELECT 
    
    -- Convert sale_id into INTEGER type
    sale_id::INT AS sale_id,

    -- Convert price into DECIMAL format 
    -- with 2 decimal places
    price::DECIMAL(10,2) AS unit_price,

    -- Convert is_returned values into 
    -- TRUE/FALSE boolean values
    is_returned::BOOLEAN AS is_returned

FROM sales_raw;
```

## 2. Temporal Normalization (Timezones)
Sales happen globally. Silver should normalize 
all timestamps to a single standard (usually UTC) 
to allow for global reporting.

In DuckDB, timezone handling is performed using 
the `AT TIME ZONE` syntax, which is standard in 
`PostgreSQL-style` dialects. DuckDB does not use 
the specific `FROM_UTC_TIMESTAMP` function names 
found in Spark or Hive, but achieves the same 
result more flexibly.

```sql
SELECT 
    sale_id,
    -- Convert UTC to a specific local timezone
    raw_timestamp AT TIME ZONE 'UTC' 
                  AT TIME ZONE 'America/New_York' AS local_time,
    
    -- Ensure the timestamp is explicitly cast/treated as UTC
    raw_timestamp AT TIME ZONE 'UTC' AS event_utc_time
FROM sales_raw;
```

## 3. String Grooming (Trim & Case)
Raw input from manual entry or legacy systems 
often has messy spacing or inconsistent casing.

```sql
SELECT 
    -- ' blackfriday ' -> 'BLACKFRIDAY'
    UPPER(TRIM(promo_code)) AS promo_code,   
    
    -- 'john DOE'      -> 'John Doe'  
    INITCAP(TRIM(customer_name)) AS customer_name 
FROM sales_raw;
```

* Pro-Tips for DuckDB Silver Layers:

Handle Nulls first: If `promo_code` is NULL, 
the result will be NULL. If you want an empty 
string instead of NULL, use COALESCE:

`UPPER(TRIM(COALESCE(promo_code, '')))`

Cleanup Hidden Characters: If your raw data comes 
from web scrapers or Excel, it might have non-breaking 
spaces or tabs. You can use DuckDB's regex support to 
strip all whitespace characters:

`UPPER(regexp_replace(promo_code, '\s+', '', 'g'))`

Performance: DuckDB's string operations are highly 
optimized and vectorized, meaning it processes these 
transformations on thousands of rows at once rather 
than one-by-one.



## 4. Deduplication (Record Versioning)
If a sale is updated (e.g., status change from 
`'pending'` to `'shipped'`), you only want the 
latest version in Silver.

```sql
SELECT *
FROM sales_raw
QUALIFY ROW_NUMBER() OVER(
     PARTITION BY sale_id 
     ORDER BY source_updated_at DESC
   ) = 1;
```

The Standard CTE Way:

If you want to keep the structure clear for a 
multi-step Silver transformation pipeline, using 
a CTE with DuckDB's `EXCLUDE` keyword is the "pro" 
move. This keeps your final table clean by 
automatically dropping the rank helper column.


```sql
WITH ranked_sales AS (
    SELECT *, 
           ROW_NUMBER() OVER(
              PARTITION BY sale_id 
              ORDER BY source_updated_at DESC
           ) as rank
    FROM sales_raw
)
SELECT * EXCLUDE (rank)
FROM ranked_sales 
WHERE rank = 1;
```

* Why use QUALIFY in DuckDB?

Less Code: You avoid the "wrapper" subquery or CTE.

Performance: DuckDB's optimizer is specifically 
designed to handle `QUALIFY` by pushing the filter 
as close to the data scan as possible.

Standardization: It matches the syntax used 
in other modern warehouses like Snowflake 
and BigQuery.

* The DuckDB Shorthand

```sql
SELECT DISTINCT ON (sale_id) *
FROM sales_raw
ORDER BY sale_id, source_updated_at DESC;
```

How it works:

`DISTINCT ON (sale_id)`: Tells DuckDB to keep only the 
first row it encounters for each unique sale_id.

`ORDER BY sale_id, ..`.: You must order by the column 
inside the parentheses first.

`source_updated_at DESC`: This secondary sort ensures that 
the "first" row DuckDB sees for each ID is the one with the 
latest timestamp.


Why this is the "Silver Layer" winner:

* No Helper Columns: <br>
Unlike `ROW_NUMBER()`, this doesn't 
create a `rank` or `rn` column that 
you have to manually drop later.

* Readability: <br> 
It’s very clear that your intent 
is "one row per `sale_id`."

* Performance: <br>
DuckDB’s engine is highly optimized 
for this pattern, as it can stop 
looking for a specific ID once it 
finds the first match in a sorted 
stream.



## 5. Categorical Mapping (CASE Statements)
Standardizing "shorthand" source codes into 
readable, business-friendly categories.

In DuckDB, your CASE statement works perfectly 
as written. DuckDB follows standard SQL for 
conditional logic, making it highly compatible 
with this pattern. 

```sql
SELECT 
    CASE 
        WHEN channel_id IN ('WEB', 'APP') THEN 'Digital'
        WHEN channel_id IN ('STR', 'KIOSK') THEN 'Physical'
        ELSE 'Other' 
    END AS sales_channel_group
FROM sales_raw;
```

* Pro-Tip: DuckDB's DECODE for Simpler Mapping <br>
If you are doing simple "A to B" mapping without 
complex inequalities, DuckDB provides a decode 
function which is even more concise: 

```sql
SELECT 
    decode(channel_id, 
        'WEB', 'Digital', 
        'APP', 'Digital', 
        'STR', 'Physical', 
        'KIOSK', 'Physical', 
        'Other'
    ) AS sales_channel_group
FROM sales_raw;
```

* Why this is a Silver Layer staple:

* Standardization: <br>
Raw sources often use cryptic codes 
(e.g., `CH_01`, `CH_02`). Converting 
these to human-readable strings in Silver 
ensures all downstream "Gold" reports 
speak the same business language.

* Performance: <br>
DuckDB evaluates CASE and decode in a 
vectorized manner, so even if you have 
100 million rows, the classification 
happens almost instantly. 

#### for that query, use DuckDB's Enum types
In DuckDB, Enums are great for 
the Silver layer because they 
store categories as small integers 
internally while displaying them 
as strings. This saves memory and 
prevents "garbage" values from 
entering your categorized columns.  

Here is how you implement that 
channel grouping using Enums:


1. Create the Enum Type <br>
First, define the allowed "Gold-standard" categories.

```sql
CREATE TYPE channel_group 
   AS ENUM ('Digital', 'Physical', 'Other');
```

2. Use it in your Transformation <br>
You can now cast the result of your `CASE` 
statement directly to this type.

```sql
SELECT 
    CASE 
        WHEN channel_id IN ('WEB', 'APP') THEN 'Digital'
        WHEN channel_id IN ('STR', 'KIOSK') THEN 'Physical'
        ELSE 'Other' 
    END::channel_group AS sales_channel_group
FROM sales_raw;
```

Why use Enums in the Silver Layer?

* Storage Efficiency: <br>
DuckDB stores 'Digital' as 0, 'Physical' as 1, 
etc. This makes your Silver tables much smaller 
than using raw VARCHAR.

* Data Integrity: <br>
If you try to insert a value not in the `Enum` 
(like 'Unknown'), DuckDB will throw an error, 
acting as a "quality gate" for your Silver layer.

* Faster Joins: <br>
Joining on Enums is significantly faster than 
joining on long string columns.

Note: In DuckDB, `Enums` are case-sensitive. 
If you define `'Digital'`, you must output 
`'Digital'` in your CASE statement.



## 6. Handling Nulls (Defaulting)
Replacing NULL values with meaningful defaults 
so downstream calculations don't break.

In DuckDB, your query works perfectly as written. 
To make it "Silver-standard," it is recommended 
to add explicit type casting. This ensures that 
if the raw data is mixed (e.g., a string in a 
numeric column), the pipeline doesn't crash.


```sql
SELECT 
  sale_id,
    
  -- Defaulting to 0.00 and ensuring it's a Decimal
  COALESCE(discount_amount::DECIMAL(18,2), 0.00) 
    AS discount_amount,
    
  -- Defaulting to -1 and ensuring it's an Integer
  COALESCE(store_id::INTEGER, -1) 
    AS store_id
    
FROM sales_raw;
```

Pro-Tips for DuckDB Null Handling:

Strict Casting: Using `::INTEGER` or `::DECIMAL` 
ensures the `COALESCE` types match. If you try 
to coalesce a string with `-1` without casting, 
some SQL engines might complain; DuckDB is flexible, 
but explicit casting is safer for data integrity. 

Handling Empty Strings: In raw CSV or JSON "dumps," 
sometimes a field isn't `NULL`, but is an empty 
string (''). To treat those as `NULL` so the 
default kicks in, use NULLIF:

```sql
COALESCE(NULLIF(TRIM(store_id), '')::INTEGER, -1)
```

The `IFNULL` Alias: DuckDB also supports 
`IFNULL(column, default)`, which is a 
shorter alias for `COALESCE` when you 
only have two arguments.


## 7. Flattening Semi-Structured Data (JSON/Arrays)

Raw sales often store line items or tags as JSON. 
Silver flattens these into a relational format.

In DuckDB, you don't need the `LATERAL VIEW EXPLODE` 
syntax used in Spark/Hive. Instead, you use the 
`UNNEST` function. DuckDB treats JSON arrays as 
native lists, making this much more concise.

The DuckDB Version

```sql
SELECT 
    sale_id,
    -- Extract the 'items' array, then 
    -- 'unnest' it into individual rows
    unnest(raw_payload->'$.items')->>'$.product_id' 
       AS product_id,
    (unnest(raw_payload->'$.items')->>'$.quantity')::INT 
       AS quantity
FROM sales_raw;
```

### Complete Working Example

Here is a full script you can run in DuckDB 
to see it in action. It creates a "Bronze" 
table with a JSON blob and transforms it 
into a relational  "Silver" format.

#### Step-1. Create a Bronze Layer with semi-structured JSON
```sql
CREATE TABLE sales_raw (
    sale_id INT,
    raw_payload JSON
);

INSERT INTO sales_raw VALUES 
(101, '{"items": [{"product_id": "A1", "quantity": 2}, {"product_id": "B2", "quantity": 1}]}'),
(102, '{"items": [{"product_id": "C3", "quantity": 5}]}');

memory D select * from sales_raw;
┌─────────┬───────────────────────────────────────────────────────────────────────────────────────┐
│ sale_id │                                      raw_payload                                      │
│  int32  │                                         json                                          │
├─────────┼───────────────────────────────────────────────────────────────────────────────────────┤
│     101 │ {"items": [{"product_id": "A1", "quantity": 2}, {"product_id": "B2", "quantity": 1}]} │
│     102 │ {"items": [{"product_id": "C3", "quantity": 5}]}                                      │
└─────────┴───────────────────────────────────────────────────────────────────────────────────────┘
memory D
```

#### Step-2. Transform to Silver Layer by flattening (unnesting)
```sql
sql
CREATE OR REPLACE TABLE sales_silver AS
SELECT 
    sale_id,
    -- Cast the JSON fragment to a native DuckDB LIST of JSON objects
    unnest((raw_payload->'$.items')::JSON[]) AS item_node
FROM sales_raw;

memory D select * from sales_silver;
┌─────────┬──────────────────────────────────┐
│ sale_id │            item_node             │
│  int32  │               json               │
├─────────┼──────────────────────────────────┤
│     101 │ {"product_id":"A1","quantity":2} │
│     101 │ {"product_id":"B2","quantity":1} │
│     102 │ {"product_id":"C3","quantity":5} │
└─────────┴──────────────────────────────────┘
memory D
```

#### Step-3. Final Select to extract specific fields from the unnested nodes
```sql
SELECT 
    sale_id,
    item_node->>'$.product_id' AS product_id,
    (item_node->>'$.quantity')::INT AS quantity
FROM sales_silver;

┌─────────┬────────────┬──────────┐
│ sale_id │ product_id │ quantity │
│  int32  │  varchar   │  int32   │
├─────────┼────────────┼──────────┤
│     101 │ A1         │        2 │
│     101 │ B2         │        1 │
│     102 │ C3         │        5 │
└─────────┴────────────┴──────────┘
```

Why this is better in DuckDB:

* JSON Pathing: <br>
The `->` operator returns a JSON object, 
while `->>` returns the value as a string 
(ready for casting).

* Vectorized Unnest: <br>
DuckDB is extremely fast at unnesting; 
it doesn't "loop" through the array but 
expands it using a vectorized approach.

* No Subqueries: <br>
You can often perform the unnest and 
the attribute extraction in a single 
`SELECT` statement.



## 8. Basic Validation Filtering (Quarantine)
Removing "impossible" data, like negative prices 
or future sale dates, to keep the Silver layer clean.

In DuckDB, your query works exactly as written, as 
DuckDB supports both the CURRENT_DATE keyword and 
standard comparison operators. 

The DuckDB Version

```sql
-- Filters for valid, non-future sales 
-- records in the Silver layer
SELECT * 
FROM sales_raw
WHERE unit_price > 0 
  AND sale_date <= CURRENT_DATE;
```

Business Insight: Data Quality & Integrity

Filtering your Bronze data during the move 
to Silver provides critical business value 
by acting as a "quality gate": 

Financial Accuracy: Removing records where 
`unit_price <= 0` eliminates "garbage" entries, 
test transactions, or corrupted data that would 
otherwise skew revenue metrics and average 
order value (AOV) calculations.

Temporal Reliability: Filtering out future 
`sale_date` values ensures your reporting 
doesn't include "phantom" sales or anomalous 
forward-dated entries that undermine 
stakeholder trust in your dashboards.

Ready for Analytics: By enforcing these basic 
business rules in the Silver layer, you create 
a validated, high-quality foundation for 
self-service BI and machine learning. 

Pro-Tip: In a production DuckDB pipeline, 
you might use `today()` as a slightly more 
concise alias for `CURRENT_DATE`. 


## 9. Business Key Generation (Hashing)
Creating a unique "Surrogate Key" by hashing 
multiple columns to track records across systems.

In DuckDB, the `MD5` and `CONCAT` functions work 
perfectly, but for data engineering, we usually 
prefer the `md5_number` or the `hash()` function 
for performance, or `concat_ws` to handle nulls 
safely.  Here is the robust DuckDB version and a 
detailed breakdown of the logic.

## The DuckDB SQL

```
SELECT
    *, 
    -- Use concat_ws (concat with separator) 
    -- to safely handle NULL values
    md5(concat_ws('|', source_system_id, raw_order_number)) 
      AS silver_sale_key
FROM sales_raw;
```

## What is happening? (Detailed Breakdown)

> A "surrogate key" is a unique, system-generated 
> identifier added to a database table that has 
> no intrinsic meaning or relationship to the 
> actual business data. Unlike a natural key 
> (e.g., email or SSN), a surrogate key is usually 
> a simple, sequential integer or UUID created 
> solely to uniquely identify records and improve 
> database performance.

In a Medallion Architecture, creating a 
"Surrogate Key" in the Silver layer is a 
critical step for "Data Integration." Here 
is why this specific SQL works:

## 1. Concatenation (CONCAT_WS)

* The Problem: If you simply add columns together 
`(A + B)`, you might get "collisions." For example, 
ID: 10 and Num: 1 looks the same as ID: 1 and Num: 01. 
Both become 101.

* The Fix: We use a separator (the pipe `|`). 
This turns them into `10|1` vs `1|01`, making 
them distinct.

* The Null Trap: In standard SQL, `CONCAT('A', NULL)` 
returns NULL. `CONCAT_WS` (Concat With Separator) is 
smarter—it skips nulls, ensuring your key doesn't 
vanish just because one source field was empty.

## 2. Hashing (MD5)

* Deterministic Output: <br>
No matter how many times you run this, the same 
input always yields the same 32-character hex 
string. This allows you to re-run your pipeline 
and always match the same records.

* Fixed Width: <br>
Even if your source IDs are 100 characters long, 
the MD5 hash is always the same length. This makes 
indexing and joining in the Gold layer much faster.

* Universal Linkage: <br>
By hashing, you create a "Global ID" that can link 
a sale in your Salesforce system to a record in your 
Shopify system, even if they have different internal 
ID formats.

## 3. The "Silver" Layer Goal

* Tracking across systems: <br>
In the Bronze layer, data is messy and siloed. 
In the Silver layer, the Surrogate Key acts as 
the "Join Key." It allows you to track a single 
business entity (like a Sale) as it moves through 
your ecosystem, regardless of where it started.

## Pro-Tip: The "Collision" Safety
While `MD5` is standard, DuckDB also supports 
`SHA256(column)`, which is mathematically much 
less likely to have a "collision" (two different 
inputs producing the same key) for extremely large 
datasets (billions of rows).


## 10. Flagging High-Value/Anomalous Transactions
Adding "helper flags" that aren't complex metrics 
but help analysts filter the data quickly.

In DuckDB, your query works exactly as written using 
standard SQL syntax. However, to make it even more 
"DuckDB-idiomatic" and efficient for a Silver layer, 
you can use Boolean types instead of integers (1/0). 

```sql
SELECT 
    *,
    CASE WHEN total_amount > 10000 
             THEN 1 
             ELSE 0 
    END AS is_bulk_order,
         
    CASE WHEN email_address LIKE '%@test.com' 
            THEN 1 
            ELSE 0 
    END AS is_test_record
FROM sales_raw;
```

Here is the clean DuckDB version:

The "DuckDB Way" (Using Booleans): In DuckDB, 
the result of a comparison is a BOOLEAN (True/False). 
This is more memory-efficient and clearer for 
downstream analytics. 

```sql
SELECT 
    *,
    (total_amount > 10000) AS is_bulk_order,
    (email_address LIKE '%@test.com') AS is_test_record
FROM sales_raw;
```

The Standard Version (Using 1/0):

If your downstream tool (like an older BI dashboard) 
specifically requires a `1` or `0`, your original CASE 
statement is perfectly valid:

```sql
SELECT 
    *,
    CASE WHEN total_amount > 10000 
             THEN 1 
             ELSE 0 
    END AS is_bulk_order,
    
    CASE WHEN email_address LIKE '%@test.com' 
             THEN 1 
             ELSE 0 
    END AS is_test_record
FROM sales_raw;
```

Why this is a Silver Layer Pattern:

Business Intelligence Acceleration: 

	By adding these "helper flags" in Silver, you 
	save your Gold-layer users from having to remember 
	the logic for a "bulk order." They can just filter 
	where `is_bulk_order = True`.

Noise Reduction: 

	Flagging @test.com records allows you to exclude 
	them from high-level revenue KPIs in the Gold layer 
	without deleting the data (maintaining auditability 
	in Silver).

Regex Alternative: 

	If you have many test domains, DuckDB’s regex is faster:
	
	regexp_matches(email_address, '@(test|example|internal)\.com$') 
	   AS is_test_record


---

# 10  SQL patterns that transition <br> data from a raw dump to a < br> production-ready Silver layer.

## 11. Currency Standardization (Normalizing FX)
In global sales, the raw table often has mixed 
currencies. Silver converts them to a corporate 
base currency (e.g., USD) using a lookup.

In the context of your SQL and data pipeline code, 

		FX stands for Foreign Exchange.
		
"Normalizing FX" means converting different 
currencies into a single, consistent base currency 
(like USD) so you can accurately compare or sum 
up sales data.

In your specific Silver Transformation script, 
this part of the code was doing exactly that:

```sql
CAST(TRY_CAST(price AS DECIMAL(12,2)) * 
    CASE 
        WHEN currency = 'EUR' 
           THEN 1.10 
           ELSE 1.0 
    END AS DECIMAL(12,2)) AS amount_usd
```

## Why it's called "Normalizing":
If you have one sale for `100 USD` and another 
for `100 EUR`, you can't simply add them together 
to get "200" because they have different values. 
By "Normalizing FX," you convert the EUR to USD 
first (e.g., `$110`), giving you a normalized total 
of `$210 USD`.

In DuckDB, this transformation is highly efficient. 
To make it "Silver-layer ready," we should use 
explicit joins and ensure data types are aligned 
to prevent precision loss during the multiplication.

The DuckDB Version

```sql
SELECT 
    s.sale_id,
    -- Ensure decimal precision during currency conversion
    (s.amount::DECIMAL(18,2) * 
    (r.exchange_rate::DECIMAL(18,6))::DECIMAL(18,2))
       AS amount_usd,
    'USD' AS base_currency
FROM sales_raw AS s
INNER JOIN exchange_rates AS r 
    ON s.currency = r.currency_code 
   AND s.sale_date = r.rate_date;
```

#### Why this is a "Silver" Standard:

   1. Inner Join vs. Left Join: <br>
   By using an `INNER JOIN`, you ensure that only 
   sales with a valid exchange rate move into the 
   Silver layer. If an exchange rate is missing, 
   the record won't appear, preventing "NULL" 
   revenue in your reports.
   
   2. Decimal Precision: <br> 
   Raw data often comes in as floats or strings. 
   By casting to `DECIMAL(18,2)` (for money) and 
   `DECIMAL(18,6)` (for rates), you avoid the 
   rounding errors common with the FLOAT type.
   
   3. Temporal Join: <br>
   Matching on `s.sale_date = r.rate_date` is a 
   classic Medallion pattern. It ensures the 
   conversion uses the "Truth" of the market at 
   the exact time the sale occurred.

#### Pro-Tip: The ASOF Join
If your exchange_rates table doesn't have a record 
for every single day, but you want to use the most 
recent available rate, DuckDB has a "killer feature" 
called the ASOF JOIN:

```sql
SELECT 
    s.sale_id,
    s.amount * r.exchange_rate AS amount_usd
FROM sales_raw s
ASOF JOIN exchange_rates r 
    ON s.currency = r.currency_code 
    AND s.sale_date >= r.rate_date; 
   -- Grabs the latest rate available UP TO the sale date
```
    
An `ASOF JOIN` (As-Of Join) is a specialized join 
designed for time-series data where timestamps rarely 
match exactly. It allows you to link a specific event 
(like a trade) with the most recent prior value from 
another table (like a price update). 

## The Concept
In a standard JOIN, you need an exact match 
(e.g., `10:00:00 == 10:00:00`). An `ASOF JOIN` 
uses an inequality (typically `>=`) to find the 
"latest record as of this time". 

## Simple Example
Imagine you have a table of Trades and a 
table of Prices. Prices change frequently, 
but not necessarily at the exact second a 
trade occurs. 

1. Create Tables

```sql
CREATE TABLE trades 
(ticker VARCHAR, time TIMESTAMP, quantity INT);

CREATE TABLE prices 
(ticker VARCHAR, time TIMESTAMP, price DOUBLE);

INSERT INTO prices VALUES 
('AAPL', '10:00:00', 150.00), 
('AAPL', '10:05:00', 155.00);

INSERT INTO trades VALUES ('AAPL', '10:02:00', 10);
```

2. The ASOF JOIN

To find what the price was when the `10:02:00` 
trade happened, use `ASOF JOIN`. It will ignore 
the future `10:05:00` price and grab the `10:00:00` 
price. 

```sql
SELECT 
    t.ticker, t.time, t.quantity, p.price
FROM trades t
ASOF JOIN prices p 
    ON t.ticker = p.ticker   -- Exact match key
    AND t.time >= p.time;    -- The "As-Of" condition
```

Result:

| ticker | time | quantity | price |
|---|---|---|---|
| AAPL | 10:02:00 | 10 | 150.00 |

## Key Rules

* Exact Match First: <br>
You must include at least one 
equality condition (like ticker).

* Inequality Second: <br>
You must include exactly one inequality 
condition (usually `t.time >= p.time`).

* Single Match: <br>
Unlike a regular join, `ASOF` only returns 
one row from the right side—the closest one 
that satisfies the condition. 

This is a powerful tool for **FX normalization**, 
stock market analysis, or IoT sensor data where 
you need the last known state at a specific moment. 
 

## 12. Address Parsing & Standardization
Raw logs often capture "Ship To" info as one 
messy string. Silver splits these into structured 
columns for regional analysis.

In DuckDB, the `SPLIT_PART` function works exactly 
like it does in PostgreSQL, making this transformation 
very straightforward. 

The DuckDB SQL

```sql
SELECT 
    sale_id,
    -- Part 1: Everything before the first comma
    split_part(raw_address, ',', 1) AS street_address,
    
    -- Part 2: Everything between the first and second comma
    trim(split_part(raw_address, ',', 2)) AS city,
    
    -- Part 3: Everything between the second and third comma, cleaned up
    upper(trim(split_part(raw_address, ',', 3))) AS state_code
FROM sales_raw;
```

What is happening? (Detailed Breakdown)

In a Medallion Architecture, moving from a 
single "blob" string to structured columns 
is a core Silver Layer task. It enables 
regional filtering and shipping analysis 
that isn't possible in the Bronze "dump."

#### 1. `split_part(string, delimiter, index)`
The Logic: This function looks for your 
delimiter (the comma ,) and splits the 
string into a list. The index tells 
DuckDB which piece to grab. 

Note: Unlike many programming languages 
where lists start at 0, SQL `split_part` 
starts at 1.

Safety: If the comma doesn't exist at that index 
(e.g., the address only has one comma), DuckDB 
returns an empty string instead of crashing. 

#### 2. `trim(...)`
The Problem: When addresses are typed like 
`"123 Main St, New York, NY"`, there is usually 
a space after the comma. `split_part` captures 
that space, resulting in " New York".
The Fix: trim strips leading and trailing 
whitespace to give you a clean "New York".

#### 3. `upper(...)`
The Goal: Standardizing categorical data. By 
forcing the state to uppercase (e.g., `ny NY`), 
you ensure that when you group by state in the 
Gold Layer, you don't get two separate rows for 
the same state.

Pro-Tip: Dealing with Inconsistent Addresses
If your raw data is extra messy (e.g., some have 
2 commas, some have 3), you can use DuckDB's 
list-based splitting for more control:

```sql
-- Split the whole string into a list first
WITH address_list AS (
    SELECT sale_id, 
           string_split(raw_address, ',') as parts
    FROM sales_raw
)
SELECT 
    sale_id,
    parts[1] AS street,
    -- Grabs the last element of the list, 
    -- regardless of how many commas exist
    upper(trim(parts[-1])) AS state_code 
FROM address_list;
```


## 13. Late-Arriving Dimension Handling
If a sale references a `customer_id` that 
hasn't been synced to the Customer table yet, 
Silver ensures the record isn't lost.

In DuckDB, this is a classic Silver-to-Silver 
join or Bronze-to-Silver lookup. To make it 
"nice" and production-ready, it is best practice 
to explicitly cast your joining keys to ensure 
the hash-join is as fast as possible.

The DuckDB Version

```sql
SELECT 
    s.*,
    -- Default 'Pending Sync' for late-arriving dimension records
    COALESCE(c.customer_name, 'Pending Sync') AS customer_name
FROM sales_raw AS s
LEFT JOIN customer_silver AS c 
  ON s.customer_id::BIGINT = c.customer_id::BIGINT;
```

Why this is a Medallion Pattern:

* Late-Arriving Dimensions: <br>
In distributed systems, a sale (fact) might 
arrive before the customer record (dimension). 
Using COALESCE with "Pending Sync" prevents 
your Silver layer from showing confusing NULL 
values and signals to the business that the 
data is still being processed.

* Left Join: <br>
In the Silver layer, we use `LEFT JOIN` to ensure 
we don't lose sales records just because the 
customer data is missing. An `INNER JOIN` would 
discard the sale entirely.

* Performance: <br>
DuckDB is highly optimized for Hash Joins. 
By casting the IDs (e.g., `::BIGINT`), you 
ensure DuckDB isn't trying to join a `"string 101"` 
to an `"integer 101,"` which would slow down 
the transformation. 

Pro-Tip: The `USING` Keyword

If both tables have the exact same column name 
for the ID, you can make the SQL even cleaner: 

```sql
SELECT 
    s.*,
    COALESCE(c.customer_name, 'Pending Sync') AS customer_name
FROM sales_raw s
LEFT JOIN customer_silver c USING (customer_id);
```


## 14. Calculating "Tax-Exclusive" Amounts
Raw data often provides a "Grand Total" but 
not the breakdown. Silver reverses the math 
to isolate the net revenue.

In DuckDB, the most efficient and readable 
way to write this is to use a CTE or `LATERAL` 
join. This prevents you from having to write 
the math for net_revenue twice, which makes 
the code easier to maintain and reduces the 
chance of calculation errors. 

The DuckDB Version (Cleanest)

```sql
SELECT 
    total_paid,
    net_revenue,
    (total_paid - net_revenue)::DECIMAL(18,2) AS tax_collected
FROM (
    SELECT 
        *,
        ROUND(total_paid / (1 + tax_rate), 2) AS net_revenue
    FROM sales_raw
);
```

Why this is a "Silver" Standard:

* Precision Casting: <br>
In DuckDB, it is a best practice to cast financial 
results to `DECIMAL(18,2)`. This prevents "Floating 
Point Math" errors where `0.1 + 0.2` might result 
in `0.30000000000000004`.

* DRY (Don't Repeat Yourself): <br>
By calculating `net_revenue` in a subquery or CTE, 
you ensure that `tax_collected` is always exactly 
the difference. If you change the rounding logic 
later, you only have to change it in one place.

* Vectorized Execution: <br>
DuckDB performs these divisions and subtractions 
across thousands of rows simultaneously using 
SIMD instructions, making this transformation 
nearly instantaneous even on millions of records.

Pro-Tip: The `COLUMNS` helper

If you want to apply a specific rounding or casting 
rule to every numeric column in your Silver layer, 
DuckDB has a "power user" feature called `COLUMNS` 
expressions:

```sql
-- Rounds every column that contains 
-- 'amount' or 'paid' in its name
SELECT 
    ROUND(COLUMNS('(?i)amount|paid'), 2) 
FROM sales_raw;
```

## 15. Masking PII (Data Privacy)
To comply with GDPR/CCPA, Silver often hashes or 
masks sensitive data (like emails or credit cards) 
before it reaches the Gold layer.

```sql
SELECT 
    sale_id,
    
    SHA2(customer_email, 256) 
       AS anonymized_email,
    
    CONCAT('XXXX-XXXX-XXXX-', RIGHT(credit_card_last4, 4)) 
       AS masked_card
       
FROM sales_raw;
```

## 16. Record Linkage (UUID Generation)
When merging sales from two different systems 
(e.g., Shopify and an In-Store POS), you create 
a unified ID.

In DuckDB, if you are building a Medallion 
architecture, you usually want a deterministic 
ID. A standard uuid() generates a new random 
value every time you run the script, which would 
break your joins later.

The "nice" way to do this in DuckDB is to use 
`md5()` to create a stable, universal key based 
on your source data.

The DuckDB Version (Stable & Clean)

```sql
SELECT 
    -- Deterministic Hash: 
    -- Always produces the same ID for the same record
    md5(concat_ws('|', 'SHOPIFY', raw_id)) AS silver_universal_id, 
    'SHOPIFY' AS source_system,
    raw_id AS source_system_id
FROM sales_raw_shopify;
```

Why this is the "Silver" Standard:

* Idempotency: <br>
If you re-run this script tomorrow, the 
`silver_universal_id` will be exactly the same. 
If you used `uuid()`, every re-run would generate 
new IDs, causing duplicate data in your Gold layer.

* Collision Prevention: <br>
By including the string `'SHOPIFY'` in the hash, 
you ensure that if another system (like `'AMAZON'`) 
has the same `raw_id`, they will still result in 
two different universal IDs.

* `concat_ws`: <br>
Using "Concat With Separator" (`|`) prevents 
"ID bleeding." For example, `System A ID 12` 
and `System A1 ID 2` both become `A12` without 
a separator. With a separator, they stay unique: 
`A|12` vs `A1|2`.

If you absolutely need a random UUID:
If your use case requires a standard 
version-4 random UUID for a one-time 
ingestion, use the `gen_random_uuid()` 
function."


```sql
SELECT 
    gen_random_uuid() AS silver_universal_id,
    'SHOPIFY' AS source_system,
    raw_id AS source_system_id
FROM sales_raw_shopify;
```

## 17. Flagging Internal/Employee Sales
Internal sales can skew KPIs. Silver flags these 
so they can be easily filtered out in Gold.

In DuckDB, the most idiomatic and "clean" way 
to write this is to skip the CASE statement entirely. 
Since a comparison in DuckDB naturally returns a 
BOOLEAN type, you can simply write the logic as a 
direct expression. 

#### The DuckDB Version (Cleanest)

```sql
SELECT 
    *,
    -- Comparison expressions naturally 
    -- return BOOLEAN (True/False)
    ( 
      (email_domain = 'company.com') 
      OR 
      (customer_group = 'EMPLOYEE')
    ) AS is_internal_transaction
FROM sales_raw;
```

#### The Standard SQL Version
If you prefer the explicit CASE syntax for 
clarity or cross-engine compatibility, here 
is the formatted version:

```sql
SELECT 
    *,
    CASE 
        WHEN (email_domain = 'company.com') OR 
             (customer_group = 'EMPLOYEE')
            THEN TRUE 
            ELSE FALSE 
    END AS is_internal_transaction
FROM sales_raw;
```

#### Why this is a Silver Layer staple:

* KPI Integrity: <br>
In the Gold layer, you often want to report 
on "Real Customer Revenue." By flagging internal 
transactions in Silver, your Gold views can simply 
include `WHERE NOT is_internal_transaction`.

* Performance: <br>
DuckDB's vectorized engine evaluates these boolean 
logic gates across millions of rows at once.

* Schema Simplicity: <br>
Using a true `BOOLEAN` type (rather than a `1/0` 
integer or `'Y/N'` string) makes your data much 
easier to use in BI tools like PowerBI, Tableau, 
or Evidence, which automatically recognize 
checkboxes/filters for booleans. 

Pro-Tip: If your `email_domain` column is messy 
(mixed casing), use `lower()` to ensure you don't 
miss `Company.com`:

```sql
(
  lower(email_domain) = 'company.com' 
  OR 
  customer_group = 'EMPLOYEE'
) 
AS is_internal_transaction
```

## 18. Sessionization / Source Tracking
Parsing UTM parameters from a raw URL 
string to attribute the sale to a specific 
marketing channel.

In DuckDB, the regexp_extract function is 
highly efficient and uses RE2 syntax. A 
"nice" format for this often includes 
handling the case where a URL might be NULL 
or missing the parameters entirely, as well 
as providing clean aliases.

## The DuckDB Version

```sql
SELECT 
    sale_id,
    -- Extract utm_source: looks for 'utm_source=' 
    -- and captures until '&' or end
    regexp_extract(referral_url, 'utm_source=([^&]+)', 1) 
      AS utm_source,
    
    -- Extract utm_medium: looks for 'utm_medium=' 
    -- and captures until '&' or end
    regexp_extract(referral_url, 'utm_medium=([^&]+)', 1) 
      AS utm_medium
FROM sales_raw;
```

## Why this is a "Silver" Standard:

* Parsing Logic: <br>
In the Bronze layer, the `referral_url` is just a 
long string. By extracting UTM parameters into 
their own columns in Silver, you allow the Gold 
layer to perform instant marketing attribution 
(e.g., "Total sales from Google"). 

* Capture Groups: <br>
The `([^&]+)` part of the regex is a "capture group." 
The `1` at the end tells DuckDB to return the first 
group (the text inside the parentheses), excluding 
the `"utm_source="` prefix itself. 

* Handling Missing Data: <br>
If the regex doesn't find a match (e.g., the user 
came directly to the site), DuckDB returns an empty 
string or NULL depending on your settings, which is 
exactly what you want for clean reporting. 

## Pro-Tip: Using `url_decode`
Oftentimes, UTM parameters in the URL are "encoded" 
(e.g., `google%20ads` instead of `google ads`). To make 
your Silver layer truly clean, wrap the extraction in 
`url_decode`:

```sql
SELECT 
    sale_id,
    url_decode(regexp_extract(referral_url, 'utm_source=([^&]+)', 1)) 
      AS utm_source
FROM sales_raw;
```


## 19. Schema Evolution Guarding
When the source adds random new columns, 
Silver uses "Safe" selection to ensure the 
downstream pipeline doesn't crash.

In DuckDB, `TRY_CAST` is the gold standard 
for "defensive" data engineering. It ensures 
that your Silver layer remains resilient even 
when the Bronze layer (the raw files/tables) 
contains corrupted data or unexpected schema 
changes.

#### The DuckDB Version

```sql
SELECT 
    -- If 'quantity' contains "10", 
    -- it becomes 10 (INT)
    --
    -- If 'quantity' contains "abc", 
    -- it becomes NULL (instead of crashing)
    TRY_CAST(quantity AS INTEGER) AS quantity
FROM sales_raw;
```

#### Why this is critical for Schema Evolution:

   1. Pipeline Stability: <br> 
      In many SQL engines, a single "bad" row 
      (like a string in an integer column) will 
      fail a million-row ingestion. `TRY_CAST` 
      allows the pipeline to finish successfully, 
      letting you handle the NULL values later.
   
   2. Schema Drift: <br> 
      If a source system changes a column from 
      `INT` to `VARCHAR` without telling you, 
      your Silver layer query won't break; it 
      will simply attempt to convert the new 
      strings back to integers.
   
   3. Data Quality Monitoring: <br> 
      You can easily find rows that failed the 
      schema guard by checking for NULLs where 
      the raw data was not null:
   

* Find "corrupted" rows that failed the cast
   
```sql
SELECT * 
FROM sales_silver 
WHERE quantity IS NULL AND 
      raw_quantity_string IS NOT NULL;
```
   
   
#### Pro-Tip: DuckDB's COLUMNS for Bulk Guarding
If you have `50` columns and want to safely cast 
all of them that have `"qty"` in the name, DuckDB 
allows you to do this in one line:

```sql
SELECT 
    TRY_CAST(COLUMNS('(?i).*qty.*') AS INTEGER)
FROM sales_raw;
```

#### Business Insight: The "Soft Fail"
By using `TRY_CAST`, you move from a Hard Fail 
architecture (everything stops) to a Soft Fail 
architecture (data flows, but bad values are 
flagged as NULL). This ensures that your business 
users still get `99%` of their data on time while 
you fix the `1%` of corrupted records.



## 20. Change Data Capture (CDC) Flagging
Silver identifies if a record is a 

* New Insert (I), 
* an Update (U), or 
* a Hard Delete (D) 

from the source system.

In DuckDB, your CASE statement is perfectly valid, 
but we can make it more efficient and "clean" for 
a Silver layer. In a real-world CDC (Change Data 
Capture) pipeline, you often want to simplify these 
codes into a unified status that downstream Gold-layer 
models can easily filter.

#### The DuckDB Version

```sql
SELECT 
    *,
    -- Mapping raw CDC codes to business-friendly statuses
    CASE _change_oper
        WHEN 'INSERT' THEN 'NEW'
        WHEN 'UPDATE' THEN 'MODIFIED'
        WHEN 'DELETE' THEN 'DELETED'
        ELSE 'UNKNOWN' 
    END AS operational_status
FROM sales_raw;
```

#### Why this is a "Silver" Standard:

* Auditability: <br>
In the Bronze layer, the data is just a stream 
of changes. In Silver, adding an `operational_status` 
column makes it immediately clear to a data analyst 
what happened to that specific row.

* Standardization: <br> 
Different source systems use different codes 
(e.g., `I/U/D` vs `INSERT/UPDATE/DELETE`). 
Standardizing these in Silver ensures your entire 
Lakehouse uses the same vocabulary.

* Downstream Filtering: <br>
This allows your Gold layer to easily implement 
Soft Deletes. Instead of physically removing 
data, you can just filter for WHERE 
`operational_status != 'DELETED'`.


#### More Complex: CDC with Window Functions
In many CDC scenarios, you get multiple updates 
for the same record in a single batch. You only 
want the latest state.

Here is how you use a Window Function to pick the 
most recent operation for each ID, effectively 
"collapsing" the CDC history:

```sql
SELECT * EXCLUDE (row_num)
FROM (
    SELECT 
        *,
        -- Rank records for the same ID by their timestamp
        ROW_NUMBER() OVER (
            PARTITION BY sale_id 
            ORDER BY source_timestamp DESC
        ) AS row_num
    FROM sales_raw
)
-- Only keep the latest version of the record
WHERE row_num = 1 
  -- Optional: Skip records that were ultimately deleted
  AND _change_oper != 'DELETE';
```

## What's happening here?

   1. PARTITION BY `sale_id`: <br>
      Groups all changes for a specific sale together.
   
   2. `ORDER BY source_timestamp DESC`: <br> 
      Ensures the "Newest" change gets `row_num = 1`.
      
   3. `EXCLUDE (row_num)`: <br>
      A DuckDB helper that keeps your final table clean 
      by dropping the temporary ranking column.




# Concrete SQL examples based on DuckDB

Using DuckDB for these operations is highly 
efficient because it handles complex window 
functions and JSON parsing with a very clean 
syntax.

Here are concrete examples of Silver-layer 
transformations using DuckDB's specific 
features:

## 1. Handling "As-of" State (Latest Record)

DuckDB’s `QUALIFY` clause is the cleanest 
way to **deduplicate**. It allows you to 
filter the results of a window function 
without a subquery.

```sql
-- Picks the most recent version of every order
SELECT *
FROM sales_raw
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY order_id 
    ORDER BY ingestion_timestamp DESC
) = 1;
```

## 2. Time-Series Gap Filling
In sales reporting, missing dates are common. 
DuckDB can generate a date range and "backfill" 
missing sales dates with zeros.

```sql
-- Create a continuous timeline and 
-- join raw sales to find gaps
SELECT 
    range_date.date,
    COALESCE(SUM(s.amount), 0) as daily_revenue
FROM (
    SELECT CAST(range AS DATE) AS date 
    FROM range(DATE '2023-01-01', DATE '2024-01-01', INTERVAL 1 DAY)
) AS range_date
LEFT JOIN sales_raw s ON s.sale_date = range_date.date
GROUP BY 1;
```

## 3. Extracting JSON Attributes
Raw data often lands as a JSON blob. 
DuckDB uses a shorthand `->>` operator to extract values.

```sql
-- Extracting nested metadata from a raw JSON column
SELECT 
    order_id,
    raw_payload->>'$.customer.email' AS email,
    CAST(raw_payload->>'$.discount_code' AS VARCHAR) AS promo_code
FROM sales_raw;
```


## 4. Running Totals (Cume)
Calculating the lifetime value (LTV) of a customer 
as each sale "enters" the Silver layer.

```sql
SELECT 
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS running_ltv
FROM sales_raw;
```

## 5. Period-Over-Period Comparison
Calculating the difference in price between 
the current sale and the previous sale for 
that specific customer.

```sql
SELECT 
    customer_id,
    order_date,
    amount,
    amount - LAG(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS diff_from_last_purchase
FROM sales_raw;
```

## 6. Session Identification (The "Gap" Pattern)
If a customer places multiple orders within 
30 minutes, you might want to flag them as 
part of the same "buying session."

```sql
SELECT 
    *,
    CASE 
        WHEN order_timestamp - LAG(order_timestamp) OVER (
            PARTITION BY customer_id ORDER BY order_timestamp
        ) < INTERVAL '30 minutes' THEN 'Same Session'
        ELSE 'New Session'
    END AS session_flag
FROM sales_raw;
```

## 7. Pivot for One-Hot Encoding
Moving categorical data into columns 
(often needed if your Silver layer 
feeds an ML model).

```
-- Dynamically pivot sales by region
PIVOT sales_raw ON region USING SUM(amount) 
GROUP BY order_date;
```

## 8. Robust Date Parsing
DuckDB's `strptime` is excellent for 
Silver layers that receive inconsistent 
date formats from different sources.

```sql
SELECT 
    raw_date_string,
    strptime(raw_date_string, '%d/%m/%Y %H:%M:%S') AS
      standardized_timestamp
FROM sales_raw;
```

## 9. Outlier Detection (Z-Score)
Flagging transactions that are 3 standard 
deviations away from the mean price—useful 
for the "quarantine" pattern.

```sql
SELECT *,
    (amount - AVG(amount) OVER ()) / STDDEV(amount) OVER () as z_score
FROM sales_raw
QUALIFY ABS(z_score) > 3; -- Flags "weird" transactions
```

## 10. Sampling for Validation
Sometimes you want to move a clean `10%` 
sample of raw data into a "Silver Sandbox" 
for testing.

```sql
-- DuckDB native sampling
SELECT * 
FROM sales_raw 
USING SAMPLE 10 PERCENT (bernoulli);
```

## Combined SQL Pattern

In a [DuckDB](https://duckdb.org/docs/) environment, 
the Medallion Silver layer is typically implemented 
as a "Single Source of Truth" view or a table populated 
via a [CTAS (Create Table As Select)](https://duckdb.org/docs/sql/statements/create_table) statement.

Here is the combined SQL pattern that merges 
the core logic from the previous examples into 
a single pipeline.

## The Combined Silver Transformation SQL

-- This query transforms raw 'dump' data into a 
structured Silver record:

```sql
CREATE OR REPLACE TABLE sales_silver AS
WITH base_cleansing AS (
    SELECT
        -- 1. TYPE ENFORCEMENT & STRING GROOMING
        CAST(order_id AS BIGINT) AS order_id,
        UPPER(TRIM(status)) AS status,
        
        -- 2. ROBUST DATE PARSING & TIMEZONE NORMALIZATION
        -- Standardizes mixed or messy date strings to UTC
        strptime(raw_ts, '%Y-%m-%d %H:%M:%S')::TIMESTAMP 
          AT TIME ZONE 'UTC' AS event_ts_utc,

        -- 3. SEMI-STRUCTURED PARSING (JSON)
        -- Extracts customer info directly from raw JSON blobs
        raw_payload->>'$.customer.email' AS customer_email,
        (raw_payload->'$.items')::JSON AS line_items,

        -- 4. CURRENCY NORMALIZATION
        -- Joins or CASE logic to normalize to USD
        CAST(amount AS DECIMAL(18,2)) * CASE 
            WHEN currency = 'EUR' THEN 1.08 
            WHEN currency = 'GBP' THEN 1.27 
            ELSE 1.0 
        END AS amount_usd,

        -- 5. PII MASKING
        -- Hash emails for privacy compliance in lower environments
        md5(raw_payload->>'$.customer.email') AS hashed_email

    FROM sales_raw
    
    -- 6. BASIC VALIDATION FILTERING
    WHERE order_id IS NOT NULL 
      AND CAST(amount AS DECIMAL) >= 0
),
enriched_and_ranked AS (
    SELECT 
        *,
        -- 7. DEDUPLICATION (Window Function)
        -- Identify the latest version of an order if multiple exist
        ROW_NUMBER() OVER (
               PARTITION BY order_id 
               ORDER BY event_ts_utc DESC
        ) as latest_version,

        -- 8. ANALYTICAL WINDOWING (Running Totals)
        -- Calculate Customer Lifetime Value at the moment of this sale
        SUM(amount_usd) OVER (
                PARTITION BY hashed_email 
                ORDER BY event_ts_utc
        ) as cumulative_customer_ltv,

        -- 9. OUTLIER DETECTION (Z-Score)
        -- Flag values 3 standard deviations from the mean
        (amount_usd - AVG(amount_usd) OVER ()) / 
            NULLIF(STDDEV(amount_usd) OVER (), 0) as price_z_score
    FROM base_cleansing
) 
-- 10. FINAL SELECT WITH QUALIFY
-- Filters for deduplication and adds a final quarantine flag
SELECT 
    * EXCLUDE (latest_version),
    CASE WHEN ABS(price_z_score) > 3 THEN TRUE ELSE FALSE END 
      AS is_quarantined
FROM enriched_and_ranked
QUALIFY latest_version = 1;
```

## Explanation of the Integrated Patterns

   1. Strict Typing & Cleaning: <br>
      The first block ensures that downstream tools 
      don't have to deal with VARCHAR math or 
      leading/trailing spaces.
   
   2. JSON & JSON-Extract: <br>
      [DuckDB](https://duckdb.org/) treats JSON as a 
      first-class citizen using the ->> operator, 
      allowing you to move data from a "black box" 
      payload into queryable columns.
   
   3. Currency & Logic: <br> 
      By moving currency conversion into Silver, 
      you ensure that every "Gold" report uses 
      the exact same exchange rate logic.
   
   4. PIVOT & Hashing: <br>
      Privacy (Hashing) is handled early. 
      This allows analysts to join user 
      behavior without seeing the actual 
      email address.
   
   5. Window Functions (OVER): <br>

	* Deduplication: The PARTITION BY `order_id` 
    ensures you only ever have one unique row 
    per order.
	* LTV: Moving running totals into Silver saves 
	  massive amounts of compute time in the Gold layer.
      
   6. The QUALIFY Clause: <br>
      This is a DuckDB (and Snowflake) superpower. 
      It allows you to filter the results of your 
      `ROW_NUMBER()` without needing an extra nested 
      subquery, making the code much more readable.
   
   7. Quarantine Pattern: <br>
      Instead of deleting "bad" data (like the 
      `Z-score` outliers), we flag it as is_quarantined. 
      This allows the pipeline to finish while alerting 
      data engineers to investigate the high/low values.

## Zero-Copy Ingestion

DuckDB is particularly powerful because it can 
treat a folder of files or a remote bucket as a 
table without you having to "load" the data first. 
This is known as Zero-Copy Ingestion.

## Running the Silver Transformation Against Files
Here is how you execute the combined logic directly 
against a folder of Parquet or CSV files.

```sql
-- 1. Create a View or Table directly from files
-- Use 'data/sales/*.parquet' to scan an entire directory
CREATE OR REPLACE TABLE sales_silver AS
WITH base_cleansing AS (
    SELECT
        -- DuckDB automatically detects schemas from Parquet, 
        -- but we cast here to ensure Silver Layer consistency
        CAST(order_id AS BIGINT) AS order_id,
        UPPER(TRIM(status)) AS status,
        
        -- 'strptime' handles messy date formats found in raw files
        strptime(raw_ts, '%Y-%m-%d %H:%M:%S')::TIMESTAMP 
          AS event_ts_utc,

        -- Extracting from JSON stored in Parquet/CSV
        raw_payload->>'$.customer.email' AS customer_email,

        -- Currency Normalization
        CAST(amount AS DECIMAL(18,2)) * CASE 
            WHEN currency = 'EUR' THEN 1.08 
            WHEN currency = 'GBP' THEN 1.27 
            ELSE 1.0 
        END AS amount_usd

    -- READ_PARQUET can scan local paths, S3, or HTTPS URLs
    FROM read_parquet('data/sales_raw/*.parquet')
    
    WHERE order_id IS NOT NULL 
),
enriched_ranked AS (
    SELECT 
        *,
        -- Deduplication: Pick the latest file record per ID
        ROW_NUMBER() OVER (
               PARTITION BY order_id 
               ORDER BY event_ts_utc DESC
        ) as latest_v,
        
        -- Running Total: Calculate LTV across file partitions
        SUM(amount_usd) OVER (
             PARTITION BY customer_email 
             ORDER BY event_ts_utc
        ) as customer_ltv
    FROM base_cleansing
)
SELECT 
    * EXCLUDE (latest_v)
FROM enriched_ranked
QUALIFY latest_v = 1;
```

## Key Features Explained

* `read_parquet('path/*.parquet')`: <br>
This function performs globbing. It scans 
every file in the folder and treats them 
as a single unified table. It is significantly 
faster than traditional INSERT statements 
because it utilizes multi-threaded metadata 
scanning.

* Schema On-the-Fly: <br>
If you use 

		read_csv('data/*.csv', header=True, auto_detect=True)`

DuckDB will sample the files to guess the data types 
before running your Silver transformations.

* S3 Integration: <br>
By installing the httpfs extension, 
you can replace the local path with 
an S3 bucket:

```sql
INSTALL httpfs; 
LOAD httpfs;
SELECT * FROM read_parquet('s3://my-bucket/raw-sales/*.parquet');
```

* The `EXCLUDE` Keyword: <br>
A DuckDB-specific convenience. Instead of 
listing 50 columns just to remove one helper 
column (`latest_v`), you simply tell DuckDB 
to **"select everything except this one."**

## Why this is a "Medallion" Pattern

In a local or lightweight cloud setup, this approach 
allows your Bronze Layer to simply be a folder where 
your source system dumps files. Your Silver Layer script 
(above) acts as the bridge that cleanses that "lake" of 
files into a high-performance, queryable table.

---

## 20 Common SQL patterns for moving data <br> from Bronze to Silver using DuckDB. <br> Each includes a simple "Before" and "After" visualization.


## 1. Data Type Enforcement (Casting)

* Before: price is a string `"19.99"`.
* After: price is a numeric `19.99`.

```sql
SELECT CAST(price AS DECIMAL(10,2)) AS price 
FROM bronze_sales;
```

## 2. String Grooming (Trim & Case)

* Before: `" john DOE "`.
* After: `"John Doe"`.

```sql
SELECT INITCAP(TRIM(cust_name)) AS cust_name 
FROM bronze_sales;
```

## 3. Timezone Normalization

* Before: `2023-01-01 10:00 (Local)`.
* After: `2023-01-01 15:00 (UTC)`.

```sql
SELECT raw_ts::TIMESTAMP AT TIME ZONE 'EST' AS utc_ts 
FROM bronze_sales;
```

## 4. Deduplication (Latest Record)

* Before: Two rows for `order_1 (Pending, Shipped)`.
* After: One row for `order_1 (Shipped)`.

```sql
SELECT * FROM bronze_sales 
QUALIFY ROW_NUMBER() OVER(
            PARTITION BY order_id 
            ORDER BY updated_at DESC
        ) = 1;
```

## 5. Categorical Mapping

* Before: `status_code = 1`.
* After: `status_name = 'Active'`.

```sql
SELECT CASE status_code 
            WHEN 1 THEN 'Active' 
                   ELSE 'Inactive' 
       END AS status_name 
FROM bronze_sales;
```

## 6. Handling Nulls (Defaulting)

* Before: `discount = NULL`.
* After: `discount = 0.0`.

```sql
SELECT COALESCE(discount, 0.0) AS discount 
FROM bronze_sales;
```

## 7. Flattening JSON

* Before: `{"sku": "A1", "qty": 2}` (JSON string).
* After: `A1 (Column)`, `2 (Column)`.

```sql
SELECT payload->>'$.sku' AS sku, 
       (payload->>'$.qty')::INT AS qty 
FROM bronze_sales;
```

## 8. Basic Validation Filtering

* Before: A row with `price = -50.00`.
* After: Row is removed from the Silver table.

```sql
SELECT * 
FROM bronze_sales 
WHERE price > 0;
```

## 9. Surrogate Key Generation

* Before: `system_a, id_101`.
* After: `d41d8cd98f...` (Unique MD5 Hash).

```sql
SELECT md5(concat(source_sys, id)) AS silver_id 
FROM bronze_sales;
```

## 10. Boolean Flagging

* Before: `is_test_user = 'Y'`.
* After: `is_test_user = TRUE`.

```sql
SELECT (test_ind = 'Y') AS is_test_user 
FROM bronze_sales;
```

## 11. Currency Standardization

* Before: `100 (EUR)`.
* After: `108.50 (USD)`.

```sql
SELECT amount * 1.085 AS amount_usd 
FROM bronze_sales 
WHERE currency = 'EUR';
```

## 12. Address Parsing

* Before: `"New York, NY"`.
* After: 
	* `"New York" (City), 
	* "NY" (State)`.

```sql
SELECT split_part(loc, ',', 1) AS city, 
       trim(split_part(loc, ',', 2)) AS state 
FROM bronze_sales;
```

## 13. Late-Arriving Dimension Handling

* Before: `cust_id = 99` (Not in master list yet).
* After: `cust_name = 'Unknown'`.

```sql
SELECT s.*, 
       COALESCE(c.name, 'Unknown') 
       FROM bronze s 
LEFT JOIN customers c ON s.cust_id = c.cust_id;
```

## 14. Net Revenue Calculation

* Before: `Total: 110`, `TaxRate: 0.1`.
* After: `Net: 100`.

```sql
SELECT total / (1 + tax_rate) AS net_amount 
FROM bronze_sales;
```

## 15. PII Masking

* Before: `user@email.com`.
* After: `u***@email.com` or HASH.

```sql
SELECT md5(email) AS masked_email 
FROM bronze_users;
```

## 16. Record Linkage

* Before: `Shopify_123` and `POS_456`.
* After: Both assigned `global_order_id = 789`.

```sql
-- Using a mapping table logic
SELECT COALESCE(map.global_id, bronze.id) 
FROM bronze 
LEFT JOIN id_map map ON bronze.id = map.src_id;
```

## 17. Internal Sales Flagging

* Before: `email = boss@ourcompany.com`.
* After: `is_internal = TRUE`.

```sql
SELECT email, 
       (email LIKE '%@ourcompany.com') AS is_internal 
FROM bronze_sales;
```

## 18. URL Parameter Extraction
Before: `?utm_source=google`.
After: `google`.

```sql
SELECT regexp_extract(url, 'utm_source=([^&]+)', 1) AS source 
FROM bronze_traffic;
```

## 19. Schema Evolution Guarding (Try_Cast)

* Before: `"ABC"` in a numeric column.
* After: `NULL` (Instead of crashing the pipeline).

```sql
SELECT try_cast(qty AS INT) AS qty 
FROM bronze_sales;
```

## 20. Change Data Capture (CDC) Tags

* Before: Op code 'U'.
* After: `is_updated = TRUE`, `is_deleted = FALSE`.

```sql
SELECT *, 
       (op_code = 'U') AS is_updated 
FROM bronze_cdc;
```

##  DuckDB script that generates dummy data to test these 20 operations at once?

The best way to see these in action is to run 
a single "Master Transformation" script. Below 
is a DuckDB SQL script that implements all 20 
patterns simultaneously.

## The "All-in-One" Silver Transformation

This script assumes your raw data is in a table 
called `bronze_sales`.

```sql
CREATE OR REPLACE TABLE sales_silver AS
WITH base_transformation AS (
    SELECT
        -- 1. TYPE ENFORCEMENT & 19. SCHEMA GUARDING (TRY_CAST)
        TRY_CAST(order_id AS BIGINT) AS order_id,
        TRY_CAST(price AS DECIMAL(12,2)) AS raw_price,

        -- 2. STRING GROOMING
        INITCAP(TRIM(cust_name)) AS customer_name,

        -- 3. TIMEZONE NORMALIZATION (To UTC)
        raw_ts::TIMESTAMP AT TIME ZONE 'UTC' AS event_ts,

        -- 5. CATEGORICAL MAPPING
        CASE status_code 
            WHEN 1 THEN 'Pending' 
            WHEN 2 THEN 'Completed' 
            ELSE 'Unknown' 
        END AS order_status,

        -- 6. HANDLING NULLS
        COALESCE(discount, 0.0) AS discount_amt,

        -- 7. JSON FLATTENING
        payload->>'$.sku' AS product_sku,
        (payload->>'$.qty')::INT AS quantity,

        -- 9. SURROGATE KEY & 15. PII MASKING (MD5 Hash)
        md5(email) AS anonymous_user_id,

        -- 10. BOOLEAN FLAGGING & 17. INTERNAL SALES
        (email LIKE '%@ourcompany.com') AS is_internal_transaction,

        -- 11. CURRENCY STANDARDIZATION
        CASE 
            WHEN currency = 'EUR' THEN 1.08 -- Hardcoded FX for example
            WHEN currency = 'GBP' THEN 1.27 
            ELSE 1.0 
        END * TRY_CAST(price AS DECIMAL(12,2)) AS amount_usd,

        -- 12. ADDRESS PARSING
        split_part(location, ',', 1) AS city,
        trim(split_part(location, ',', 2)) AS state_code,

        -- 18. URL PARAMETER EXTRACTION (UTM)
        regexp_extract(url, 'utm_source=([^&]+)', 1) AS utm_source,

        -- 20. CDC TAGS
        (op_code = 'U') AS is_updated_record,

        -- Helper for Pattern 4 (Deduplication)
        raw_ts as _ingest_time
    FROM bronze_sales
    -- 8. VALIDATION FILTERING
    WHERE order_id IS NOT NULL 
      AND TRY_CAST(price AS DECIMAL) > 0
)
SELECT 
    * EXCLUDE (latest_rank, _ingest_time),
    -- 14. NET REVENUE CALCULATION
    (amount_usd - discount_amt) AS net_revenue
    FROM (
    SELECT *,
        -- 4. DEDUPLICATION (Pick latest based on TS)
        ROW_NUMBER() OVER(
                PARTITION BY order_id 
                ORDER BY _ingest_time DESC
        ) as latest_rank
FROM base_transformation
)
WHERE latest_rank = 1;
```

## Transformation Summary (Before vs. After)

| # | Pattern | Bronze Example (Before) | Silver Example (After) |
|---|---|---|---|
| 1/19 | Casting/Safety | `"19.99"` (String) | `19.99` (Decimal) |
| 2 | Grooming | `" john DOE "` | `"John Doe"` |
| 3 | Timezone | `2023-01-01 10:00` | `2023-01-01 10:00Z` |
| 4 | Deduplication | Two rows for ID 101 | One row (latest) |
| 5 | Mapping | status_code = 1 | "Pending" |
| 6 | Nulls | NULL | 0.0 |
| 7 | JSON | {"sku": "A1"} | "A1" |
| 8 | Validation | price = -5.00 | [Row Removed] |
| 9/15 | Hash/PII | `bob@email.com` | a102b3c4... |
| 10/17 | Flags | `admin@company.com` | `is_internal = TRUE` |
| 11 | Currency | `100 (EUR)` | `108.00 (USD)` |
| 12 | Parsing | `"Chicago, IL"` | `City: "Chicago"` |
| 14 | Revenue | `Price: 10, Disc: 2` | `Net: 8` |
| 18 | Regex | `?src=google` | `"google"` |
| 20 | CDC | `op_code = 'U'` | `is_updated = TRUE` |

Below, we wrap this SQL into a Python 
script that creates the local DuckDB 
database file automatically?

This Python script uses the duckdb 
library to create a local database, 
generate a "messy" Bronze table, and 
execute the 20-pattern Silver transformation.

## The Python Implementation

file: `test.py`

```python
import duckdb
import pandas as pd
import json

# 1. Connect to DuckDB
con = duckdb.connect('medallion_data.db')

# 2. Create the "Bronze" Layer
raw_data = [
    {
        "order_id": "101", "price": "100.00", 
        "cust_name": "  alice SMITH  ",
        "raw_ts": "2023-10-01 10:00:00", 
        "status_code": 1, "discount": 10.0,
        "payload": json.dumps({"sku": "PROD-A", "qty": 2}), 
        "email": "alice@gmail.com",
        "currency": "USD", "location": "New York, NY", 
        "url": "https://shop.com?utm_source=google",
        "op_code": "I"
    },
    {
        "order_id": "101", "price": "100.00", 
        "cust_name": "  alice SMITH  ",
        "raw_ts": "2023-10-01 10:05:00", 
        "status_code": 2, "discount": 10.0,
        "payload": json.dumps({"sku": "PROD-A", "qty": 2}), 
        "email": "alice@gmail.com",
        "currency": "USD", "location": "New York, NY", 
        "url": "https://shop.com?utm_source=google",
        "op_code": "U"
    },
    {
        "order_id": "102", "price": "Invalid", 
        "cust_name": "BOB", 
        "raw_ts": "2023-10-01 11:00:00", 
        "status_code": 1, "discount": None,
        "payload": json.dumps({"sku": "PROD-B", "qty": 1}), 
        "email": "bob@ourcompany.com",
        "currency": "EUR", "location": "Paris, FR", 
        "url": "https://shop.com",
        "op_code": "I"
    }
]

df = pd.DataFrame(raw_data)
con.execute("""
CREATE OR REPLACE TABLE bronze_sales AS 
SELECT * FROM df
""")

# 3. Execute the Master Silver Transformation
silver_sql = """
CREATE OR REPLACE TABLE sales_silver AS
WITH base_transformation AS (
    SELECT
        TRY_CAST(order_id AS BIGINT) AS order_id,
        TRY_CAST(price AS DECIMAL(12,2)) AS raw_price,
        
        -- Corrected string slicing using [start:end] syntax
        -- Format: Capitalize first letter (word[1])  
        -- and lowercase the rest (word[2:])
        (
         [upper(word[1]) || lower(word[2:]) 
          for word in string_split(trim(cust_name), ' ')]
        ).list_aggr('string_agg', ' ') AS customer_name,
        
        raw_ts::TIMESTAMP AS event_ts,
        CASE status_code 
            WHEN 1 THEN 'Pending' 
            WHEN 2 THEN 'Completed' 
            ELSE 'Unknown' 
        END AS order_status,
        COALESCE(discount, 0.0) AS discount_amt,
        payload->>'$.sku' AS product_sku,
        (payload->>'$.qty')::INT AS quantity,
        md5(email) AS anonymous_user_id,
        (email LIKE '%@ourcompany.com') AS is_internal_transaction,
        CASE 
            WHEN currency = 'EUR' THEN 1.10 
            ELSE 1.0 
        END * TRY_CAST(price AS DECIMAL(12,2)) AS amount_usd,
        split_part(location, ',', 1) AS city,
        regexp_extract(url, 'utm_source=([^&]+)', 1) AS utm_source,
        (op_code = 'U') AS is_updated_record,
        raw_ts as _ingest_time
    FROM bronze_sales
    WHERE order_id IS NOT NULL 
      AND TRY_CAST(price AS DECIMAL) > 0
)
SELECT 
    * EXCLUDE (latest_rank, _ingest_time),
    (amount_usd - discount_amt) AS net_revenue
FROM (
    SELECT 
        *, 
        ROW_NUMBER() OVER(
            PARTITION BY order_id 
            ORDER BY _ingest_time DESC
        ) as latest_rank
    FROM base_transformation
) 
WHERE latest_rank = 1;
"""

con.execute(silver_sql)

# 4. View Results
print("--- Silver Table Results ---")
# Ensure results is defined in the correct scope
results = con.execute("SELECT * FROM sales_silver").df()

# Print each record individually with its column names
for i, row in results.iterrows():
    print(f"\n--- Record {i+1} ---")
    for col in results.columns:
        print(f"{col}: {row[col]}")
```

## Output of Python Program

```
% python3 test.py
--- Silver Table Results ---

--- Record 1 ---
order_id: 101
raw_price: 100.0
customer_name: Alice Smith
event_ts: 2023-10-01 10:05:00
order_status: Completed
discount_amt: 10.0
product_sku: PROD-A
quantity: 2
anonymous_user_id: 0ce273d3249291c620af81403b14b3c1
is_internal_transaction: False
amount_usd: 100.0
city: New York
utm_source: google
is_updated_record: True
net_revenue: 90.0
```

## Why this works for Silver Layers

* Immutability: <br>
Your bronze_sales table remains untouched. 
If your logic changes, you just re-run the 
script to recreate `sales_silver`.

* Efficiency: <br>
DuckDB processes this entire pipeline 
in-memory, making it ideal for CI/CD tests 
or local development before pushing to 
a cloud Lakehouse.

* Auditability: <br>
Because you used `EXCLUDE` and `TRY_CAST`, 
the resulting table is clean but keeps enough 
metadata (like `is_updated_record`) for 
troubleshooting.
