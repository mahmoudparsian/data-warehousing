# `LIMIT N` vs `rnk <= N`

## 1. create a simple jupyter/notebook/DuckDB. 

Create a sales table with 6 countries, like:

```
USA     800
CANADA  700
ITALY   700
GERMANY 700
MEXICO  500
FRANCE  400
```

Understand the clear difference between `LIMIT 2`
and `RANK()` with `rnk <= 2`.

## [View `limit_vs_rank.ipynb`](./limit_vs_rank.ipynb)

The notebook walks through the key insight step by step:

* **`LIMIT 2`** → returns exactly 2 rows. <br>
It picks USA (800) and *one* of the three countries 
tied at 700 — which one is arbitrary. The other 
two tied countries are silently dropped.

* **`RANK()` with `rnk <= 2`** → returns **4 rows**: <br>
USA at rank 1, plus all three of CANADA/ITALY/GERMANY 
sharing rank 2. No ties are lost.

