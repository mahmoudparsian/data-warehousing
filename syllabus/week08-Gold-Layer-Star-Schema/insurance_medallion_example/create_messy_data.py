import pandas as pd
import numpy as np
import random
import os

# -------------------------------
# CONFIG
# -------------------------------
INPUT_DIR = "data"
OUTPUT_DIR = "data_messy"

os.makedirs(OUTPUT_DIR, exist_ok=True)

FILES = [
    "insurance.2021.csv",
    "insurance.2022.csv",
    "insurance.2023.csv",
    "insurance.2024.csv"
]

# corruption probabilities
P_SINGLE_ERROR = 0.15
P_MULTI_ERROR = 0.08
P_DUPLICATE = 0.05

# -------------------------------
# HELPERS
# -------------------------------
def corrupt_age():
    return random.choice([-10, 150, None])

def corrupt_bmi():
    return random.choice([5, 80, None])

def corrupt_children():
    return random.choice([-2, 15, None])

def corrupt_charges():
    return random.choice([-100, None])

def corrupt_gender():
    return random.choice(["unknown", "M", "", None])

def corrupt_smoker():
    return random.choice(["maybe", "occasionally", "", None])

def corrupt_region():
    return random.choice([
        "mars", "moon", "unknown",
        "north east", "south west",
        "north-east", "south-west",
        " NORTHEAST ", " SOUTHWEST "
    ])

def apply_corruption(row, num_issues):
    cols = ["age", "bmi", "children", "charges", "gender", "smoker", "region"]
    bad_cols = random.sample(cols, num_issues)

    for col in bad_cols:
        if col == "age":
            row["age"] = corrupt_age()
        elif col == "bmi":
            row["bmi"] = corrupt_bmi()
        elif col == "children":
            row["children"] = corrupt_children()
        elif col == "charges":
            row["charges"] = corrupt_charges()
        elif col == "gender":
            row["gender"] = corrupt_gender()
        elif col == "smoker":
            row["smoker"] = corrupt_smoker()
        elif col == "region":
            row["region"] = corrupt_region()

    return row

# -------------------------------
# MAIN PROCESS
# -------------------------------
for file in FILES:
    print(f"Processing {file}...")

    df = pd.read_csv(os.path.join(INPUT_DIR, file))

    new_rows = []

    for _, row in df.iterrows():
        row = row.copy()

        r = random.random()

        # ---------------------------
        # SINGLE COLUMN CORRUPTION
        # ---------------------------
        if r < P_SINGLE_ERROR:
            row = apply_corruption(row, num_issues=1)

        # ---------------------------
        # MULTI COLUMN CORRUPTION
        # ---------------------------
        elif r < P_SINGLE_ERROR + P_MULTI_ERROR:
            num_issues = random.choice([2, 3])
            row = apply_corruption(row, num_issues=num_issues)

        new_rows.append(row)

        # ---------------------------
        # DUPLICATE ROW INJECTION
        # ---------------------------
        if random.random() < P_DUPLICATE:
            dup = row.copy()
            new_rows.append(dup)

    df_messy = pd.DataFrame(new_rows)

    # shuffle to simulate ingestion randomness
    df_messy = df_messy.sample(frac=1, random_state=42).reset_index(drop=True)

    out_file = file.replace(".csv", ".messy.csv")
    df_messy.to_csv(os.path.join(OUTPUT_DIR, out_file), index=False)

    print(f"Saved: {out_file} | Rows: {len(df_messy)}")

print("\n✅ Messy data generation complete!")
