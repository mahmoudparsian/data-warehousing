#!/usr/bin/env python3

"""
ETL: Build a simple star schema 
     from two CSV files: 
     
         1. customers.csv
         2. orders.csv

Inputs:
  - customers.csv
  - orders.csv
  
Outputs:
  - dim_customers.csv
  - dim_dates.csv
  - fact_orders.csv

Also includes optional SQL load helpers (MySQL) 
if you want to load into a DB.
"""

import argparse
import pandas as pd

TAX_RATE = 0.07

def build_date_dim(orders: pd.DataFrame) -> pd.DataFrame:
    dates = pd.DataFrame({"date": pd.to_datetime(sorted(pd.to_datetime(orders["order_date"]).dt.date.unique()))})
    dates["year"] = dates["date"].dt.year
    dates["month"] = dates["date"].dt.month
    dates["day"] = dates["date"].dt.day
    dates["quarter"] = dates["date"].dt.quarter
    dates["date_id"] = dates["date"].dt.strftime("%Y%m%d").astype(int)
    return dates[["date_id", "date", "year", "month", "day", "quarter"]]

def build_fact_orders(orders: pd.DataFrame, date_dim: pd.DataFrame) -> pd.DataFrame:
    o = orders.copy()
    o["order_date"] = pd.to_datetime(o["order_date"])
    fact = o.merge(date_dim[["date_id", "date"]], left_on="order_date", right_on="date", how="left")
    fact.drop(columns=["date"], inplace=True)
    fact["tax"] = (fact["order_amount"] * TAX_RATE).round(2)
    return fact[["order_id", "customer_id", "date_id", "order_date", "channel", "order_amount", "tax"]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--customers", default="customers.csv", help="Path to customers.csv")
    ap.add_argument("--orders", default="orders.csv", help="Path to orders.csv")
    ap.add_argument("--outdir", default="out", help="Output directory")
    args = ap.parse_args()

    # Read 2 CSV files: orders.csv and customers.csv
    customers = pd.read_csv(args.customers)
    orders = pd.read_csv(args.orders)

    # Basic sanity checks
    missing = set(orders["customer_id"]) - set(customers["customer_id"])
    if missing:
        raise ValueError(f"Orders contain customer_ids not found in customers: e.g. {list(sorted(missing))[:10]}")

    date_dim = build_date_dim(orders)
    fact_orders = build_fact_orders(orders, date_dim)

    import os
    os.makedirs(args.outdir, exist_ok=True)

    customers.to_csv(os.path.join(args.outdir, "dim_customers.csv"), index=False)
    date_dim.to_csv(os.path.join(args.outdir, "dim_dates.csv"), index=False)
    fact_orders.to_csv(os.path.join(args.outdir, "fact_orders.csv"), index=False)

    print("Wrote:")
    print(" - dim_customers.csv")
    print(" - dim_dates.csv")
    print(" - fact_orders.csv")

if __name__ == "__main__":
    main()
