import pandas as pd
import numpy as np

np.random.seed(42)

N = 1_000_000

# -----------------------------
# Generate timestamps (3 years)
# -----------------------------
start = np.datetime64('2023-01-01')
end = np.datetime64('2025-12-31')

transaction_dates = start + (end - start) * np.random.rand(N)

df = pd.DataFrame({
    "transaction_id": np.arange(1, N + 1),
    "transaction_date": transaction_dates
})

# -----------------------------
# Products (skewed)
# -----------------------------
products = ["TV","RADIO","TABLE","COMPUTER","BIKE","LAPTOP","WATCH","IPAD","EBIKE"]
product_probs = [0.08, 0.05, 0.07, 0.15, 0.10, 0.25, 0.08, 0.15, 0.07]

df["product_name"] = np.random.choice(products, size=N, p=product_probs)

price_map = {
    "TV": 800,
    "RADIO": 100,
    "TABLE": 300,
    "COMPUTER": 1200,
    "BIKE": 500,
    "LAPTOP": 1500,
    "WATCH": 250,
    "IPAD": 900,
    "EBIKE": 2500
}

df["price"] = df["product_name"].map(price_map)

# -----------------------------
# Quantity (skewed)
# -----------------------------
df["quantity"] = np.random.choice(
    [1,2,3,4,5],
    size=N,
    p=[0.5, 0.25, 0.15, 0.07, 0.03]
)

# -----------------------------
# Discount (skewed low)
# -----------------------------
df["discount"] = np.round(np.random.beta(2, 8, size=N) * 0.3, 2)

# -----------------------------
# Gender (2:1 female)
# -----------------------------
df["gender"] = np.random.choice(
    ["FEMALE", "MALE"],
    size=N,
    p=[0.66, 0.34]
)

# -----------------------------
# Country (skewed)
# -----------------------------
countries = ["USA","CANADA","GERMANY","INDIA","CHINA","MEXICO","ITALY","FRANCE","SPAIN"]
country_probs = [0.40, 0.07, 0.08, 0.15, 0.15, 0.05, 0.04, 0.03, 0.03]

df["country"] = np.random.choice(countries, size=N, p=country_probs)

# -----------------------------
# Age
# -----------------------------
df["age"] = np.random.randint(18, 71, size=N)

# -----------------------------
# Sales Amount (derived)
# -----------------------------
df["sales_amount"] = df["price"] * df["quantity"] * (1 - df["discount"])

# -----------------------------
# Optional realism tweaks (VERY NICE TOUCH)
# -----------------------------

# Weekend boost (more sales on weekends)
weekday = pd.to_datetime(df["transaction_date"]).dt.dayofweek
weekend_boost = np.where(weekday >= 5, 1.2, 1.0)

df["sales_amount"] = df["sales_amount"] * weekend_boost

# High-income countries slightly higher spending
country_boost = {
    "USA": 1.2,
    "GERMANY": 1.1,
    "CANADA": 1.1
}

df["sales_amount"] = df.apply(
    lambda r: r["sales_amount"] * country_boost.get(r["country"], 1.0),
    axis=1
)

# -----------------------------
# Final cleanup
# -----------------------------
df["sales_amount"] = df["sales_amount"].round(2)

# -----------------------------
# Save
# -----------------------------
df.to_csv("sales.csv", index=False)

print("✅ sales.csv generated (Bronze-ready)")
