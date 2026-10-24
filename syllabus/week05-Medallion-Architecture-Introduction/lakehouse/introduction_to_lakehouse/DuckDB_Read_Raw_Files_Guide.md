# DuckDB: Reading Raw Files & <br> Creating Tables/Views Instantly

This guide shows how to read raw files in multiple formats using DuckDB
and instantly create views or tables.

------------------------------------------------------------------------

## 0) One-Time Setup

``` sql
CREATE OR REPLACE MACRO data_path() AS '/Users/max/data';
SELECT data_path();
```

------------------------------------------------------------------------

## 1) CSV → Instant View

``` sql
CREATE OR REPLACE VIEW v_airports AS
SELECT *
FROM read_csv_auto(data_path() || '/airport_lookup.csv');

SELECT COUNT(*) FROM v_airports;
SELECT * FROM v_airports LIMIT 5;
```

------------------------------------------------------------------------

## 2) Parquet → Instant View

``` sql
CREATE OR REPLACE VIEW v_flights_raw AS
SELECT *
FROM read_parquet(data_path() || '/flight_parquet/part-*.parquet');

SELECT COUNT(*) FROM v_flights_raw;
```

------------------------------------------------------------------------

## 3) JSON → Instant View

``` sql
CREATE OR REPLACE VIEW v_events AS
SELECT *
FROM read_json_auto(data_path() || '/events.jsonl');

SELECT * FROM v_events LIMIT 5;
```

------------------------------------------------------------------------

## 4) Excel (.xlsx)

``` sql
INSTALL excel;
LOAD excel;

CREATE OR REPLACE VIEW v_sheet AS
SELECT *
FROM read_xlsx(data_path() || '/workbook.xlsx', sheet = 'Sheet1');
```

------------------------------------------------------------------------

## 5) Multiple CSV Files as One Logical Table

``` sql
CREATE OR REPLACE VIEW v_trips AS
SELECT *
FROM read_csv_auto(
    data_path() || '/taxi_trips/*.csv',
    union_by_name = true,
    null_padding = true,
    files_to_sniff = -1
);
```

------------------------------------------------------------------------

## 6) Materializing Into a Table

``` sql
CREATE OR REPLACE TABLE t_flights_silver AS
SELECT
    CAST(Year AS INT) AS year,
    CAST(Month AS INT) AS month,
    CAST(FlightDate AS DATE) AS flight_date,
    IATA_CODE_Reporting_Airline AS carrier_code,
    CAST(DepDelayMinutes AS DOUBLE) AS dep_delay_min,
    CAST(ArrDelayMinutes AS DOUBLE) AS arr_delay_min
FROM read_parquet(data_path() || '/flight_parquet/part-*.parquet');
```

------------------------------------------------------------------------

## 7) Gold View

``` sql
CREATE OR REPLACE VIEW v_flights_gold AS
SELECT
    *,
    CASE WHEN dep_delay_min > 15 THEN 1 ELSE 0 END AS dep_delayed_15,
    CASE WHEN arr_delay_min > 15 THEN 1 ELSE 0 END AS arr_delayed_15
FROM t_flights_silver;
```

------------------------------------------------------------------------

## 8) Inspect Parquet Like `head`

``` sql
.mode line
.maxwidth 0
SELECT * 
FROM read_parquet(data_path() || '/flight_parquet/part-00000*.parquet') 
LIMIT 1;
```

------------------------------------------------------------------------

## 9) Startup Script Pattern

Create `00_build_views.sql`:

``` sql
CREATE OR REPLACE MACRO data_path() AS '/Users/max/data';

CREATE OR REPLACE VIEW flight_raw AS
SELECT * FROM read_parquet(data_path() || '/flight_parquet/part-*.parquet');

CREATE OR REPLACE VIEW airport_raw AS
SELECT * FROM read_csv_auto(data_path() || '/airport_lookup.csv');
```

Run:

``` bash
duckdb demo_lakehouse.duckdb
.read 00_build_views.sql
```

------------------------------------------------------------------------

## Summary

DuckDB allows:

-   Querying CSV, Parquet, JSON, Excel directly
-   Creating views instantly
-   Materializing tables when needed
-   Inspecting raw data without ETL

Ideal for teaching modern Lakehouse concepts.
