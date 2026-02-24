On a MacBook (latest macOS), DuckDB is extremely easy to install. 

The “best” method depends on how you want to use it for teaching.

Since you are teaching SQL / OLAP, I recommend:

✅ Primary: DuckDB CLI + Jupyter Notebook

✅ Optional: VS Code extension

✅ Lightweight: Pure CLI only

Below are the best options ranked for you.

⸻

🥇 Option 1 — Install DuckDB via Homebrew (Best for CLI Teaching)

Step 1: Install via Homebrew

brew install duckdb

Step 2: Verify

duckdb --version

Step 3: Launch DuckDB

duckdb

You’ll get:

D select 42;

You can create persistent DB file:

duckdb my_olap.db


⸻

Why This Is Good for You
	•	Lightweight
	•	Perfect for SQL teaching
	•	Zero server setup
	•	Students can reproduce easily
	•	Works great for ROLLUP/CUBE demos

⸻

🥈 Option 2 — DuckDB + Jupyter Notebook (Excellent for Teaching)

If you already use Python (which you do):

Step 1: Install Python Package

pip install duckdb

or

pip3 install duckdb

Step 2: In Jupyter Notebook

import duckdb

con = duckdb.connect("music_olap.db")
con.execute("SELECT 1").fetchall()

Example:

con.execute("""
SELECT product, quarter, region, SUM(sales)
FROM sales
GROUP BY CUBE(product, quarter, region)
""").df()


⸻

Why This Is Powerful for You
	•	SQL + visualization
	•	Pandas integration
	•	Very strong for OLAP labs
	•	No server needed
	•	Fast (vectorized engine)

⸻

🥉 Option 3 — VS Code DuckDB Extension (Very Clean UI)

If you use VS Code:
	1.	Install DuckDB via Homebrew
	2.	Install “DuckDB” extension in VS Code
	3.	Open .duckdb file
	4.	Write SQL with syntax highlighting

Very nice for live demos.

⸻

🚀 Option 4 — DuckDB UI (Optional)

They also provide:

duckdb -ui

Launches browser UI.

Not necessary, but useful for demos.

⸻

🧠 My Recommendation for You

Given your workflow:

Use Case	Recommendation
Pure SQL demo	CLI
Teaching OLAP	Jupyter + DuckDB
Student labs	CLI + Python
BI experiments	Jupyter


⸻

⚡ Why DuckDB Is Perfect for Your Curriculum
	•	CUBE support
	•	GROUPING SETS
	•	Window functions
	•	Columnar execution
	•	Runs locally
	•	No server overhead
	•	Students don’t need admin privileges

For OLAP teaching, DuckDB is dramatically cleaner than MySQL.

⸻

💡 Bonus: Performance Tip on Mac

If you have Apple Silicon (M1/M2/M3):

DuckDB is already optimized for ARM and very fast.

You don’t need Docker.
You don’t need server tuning.
It just works.

⸻

🎯 My Suggestion

Install:

brew install duckdb
pip install duckdb jupyter pandas matplotlib

Then build:
	•	A DuckDB OLAP notebook
	•	CUBE demos
	•	Performance comparisons

If you’d like, I can next:
	•	Create a ready-to-run DuckDB OLAP notebook for your class
	•	Create a semester-ready DuckDB lab
	•	Create comparison module: MySQL vs DuckDB OLAP

