# Online Sales Star Schema <br> Data Story (DuckDB Teaching Dataset)

## Key Takeaways

Definition: 

	A Star Schema is a dimensional modeling technique 
	that separates data into Fact Tables (metrics) and 
	Dimension Tables (context).

Performance: 

	It is optimized for OLAP (Online Analytical Processing) 
	and read-heavy workloads, significantly speeding up 
	reporting compared to normalized schemas.

Structure: 

	The design resembles a star, with one central table 
	connected to multiple radiating dimension tables, 
	minimizing complex join paths.

Modern Use: 

	While created decades ago, Star Schemas remain highly 
	effective in modern columnar databases like MotherDuck 
	and DuckDB due to efficient join processing.

## This document

This document defines **business semantics**, **grain**, 
and **data-generation rules** for a small but realistic 
DuckDB star-schema dataset.

## Goals

- Build a **small, laptop-friendly** OLAP dataset in DuckDB.
- Enable OLAP teaching: GROUP BY, window functions, and later **ROLLUP / CUBE**.
- Ensure data is **not symmetric** (realistic skew across time, products, customers).

## Schema Overview

**Dimensions**

- `dates` — one row per date (2023-01-01 to 2025-12-30)
- `customers` — 5,000 customers
- `products` — 200 products
- `stores` — 10 physical stores + 1 “Online” store row

**Fact**
- `sales` — 1,000,000 sales line-items


## Star Schema Structure <br> Fact and Dimension Tables

Let's look at a concrete example that's familiar for 
many businesses: online sales data.

### The Fact Table: FactSales
This table records each sales line item:

Purpose: 

	Capture quantitative data about each sale Grain: 
	One row per product line item per sales transaction Columns:

```
date_key (FK to dates)
customer_key (FK to customers)
product_key (FK to products)
store_key (FK to stores)
quantity (Measure)
unit_price (Measure)
total_amount (Measure)
```

### The Dimension Tables
These provide the rich context around each sale:

DIM dates

```
Purpose: Slice sales by time periods
Primary Key: date_key (often an integer like YYYYMMDD)
Attributes: full_date, day_of_week, month_name, quarter, year, is_weekend
```

DIM customers

```
Purpose: Describe who made the purchase
Primary Key: customer_key
Attributes: customer_name, email, city, state, country, segment, join_date
```

DIM products

```
Purpose: Describe what was purchased
Primary Key: product_key
Attributes: product_name, SKU, category, sub_category, brand, color, size
```

DIM stores

```
Purpose: Describe where the sale occurred
Primary Key: store_key
Attributes: store_name, city, state, country, region, store_type
```

## Fact Grain

**One row in `sales` represents one line-item purchase**:
> A customer buys a quantity of one product on one date at one store with a unit price.

Measures:

- `quantity`
- `unit_price`
- `total_amount = quantity * unit_price`

## Key Strategy

- Surrogate keys:
  - `customers.customer_key` (1..5000)
  - `products.product_key` (1..200)
  - `stores.store_key` (1..11; 11th row is Online)
- Date key:
  - `dates.date_key = YYYYMMDD` (e.g., 20240424)

## Row Counts
- `customers`: 5000
- `products`: 200
- `stores`: 10 physical + 1 Online (total 11)
- `dates`: 1095
- `sales`: 1000000

## Non-Symmetric Distributions (Skew Rules)
### 1) Time skew (year distribution)
- 2023: ~30%
- 2024: ~50%
- 2025: ~20%
Seasonality: Q4 has higher volume than Q1.

### 2) Product popularity (long tail)
Top ~10% products receive a large share of sales (Zipf-like distribution).

### 3) Customer activity (heavy buyers)
- Heavy (10% customers): ~60% of sales
- Medium (30% customers): ~30% of sales
- Light (60% customers): ~10% of sales

### 4) Store/channel skew
- Online ~55%
- Physical stores collectively ~45% (uneven across stores)

### 5) Pricing & quantities
- Quantity usually 1–2, occasionally 3–5
- Unit price derived from product cost (margin + noise)
- Total amount computed: `quantity * unit_price`

## Data Quality Rules
- All fact foreign keys match dimension keys
- `customers.gender` constrained to MALE/FEMALE
- `dates` attributes computed deterministically

**Seed:** 42 (deterministic generation)
