# Run the whole movies example with ONE DuckDB (the Python package):
#
#   step 1: CSV files          --> movies_db.duckdb  (transactional / OLTP)
#   step 2: movies_db.duckdb   --> movies_dw.duckdb  (star schema, via ETL)
#   step 3: movies_dw.duckdb   --> 20 OLAP queries
#
# Usage (from this folder):
#     pip install duckdb
#     python3 run_pipeline.py
#
# Why one program? A database file written by a NEWER DuckDB cannot be opened
# by an OLDER one. If your DuckDB CLI and your Python duckdb package have
# different versions, running some steps in each can fail. This script uses
# only the Python package, so all three steps use the same version.

import os
import subprocess
import sys
import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

SOURCE_DB = "movies_db.duckdb"
TARGET_DB = "movies_dw.duckdb"

print("DuckDB version:", duckdb.__version__)

# ---- step 1: build the transactional database --------------------------
print("\n=== step 1: build", SOURCE_DB)
for f in (SOURCE_DB, TARGET_DB):
    if os.path.exists(f):
        os.remove(f)
con = duckdb.connect(SOURCE_DB)
con.execute(open("step_1_build_transacational_db/build_transactional_db.sql").read())
for t in ("movies", "users", "ratings"):
    print(f"  {t:8} {con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>10,} rows")
con.close()

# ---- step 2: ETL into the star schema ---------------------------------
print("\n=== step 2: ETL", SOURCE_DB, "-->", TARGET_DB, flush=True)
rc = subprocess.call([sys.executable, "step_2_etl_to_star_schema/etl_duckdb.py", SOURCE_DB, TARGET_DB])
if rc != 0:
    sys.exit("ETL validation failed")

# ---- step 3: OLAP queries ----------------------------------------------
print("\n=== step 3: OLAP queries on", TARGET_DB)
con = duckdb.connect(TARGET_DB, read_only=True)
sql = open("step_3_OLAP_queries/OLAP_Queries_DuckDB.sql").read()
blocks = [b.strip() for b in sql.split("\n-- ") if b.strip() and "SELECT" in b.upper()]
for b in blocks:
    title, _, query = b.lstrip("- ").partition("\n")
    print(f"\n--- {title}")
    print(con.sql(query.rstrip().rstrip(";")).limit(5))
con.close()
print("\nDone. Explore the warehouse with:  duckdb", TARGET_DB, "  (or Python: duckdb.connect('movies_dw.duckdb'))")
