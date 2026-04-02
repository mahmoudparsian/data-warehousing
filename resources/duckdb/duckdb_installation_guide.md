---
marp: true
title: DuckDB Installation Guide (Mac & Windows)
paginate: true
theme: default
class: lead
---

# 🦆 DuckDB Installation Guide

## For MacBook & Windows (Step-by-Step)

---

# 🎯 What is DuckDB?

- Lightweight analytical database  
- Runs locally (no server needed)  
- Perfect for teaching SQL + analytics  
- Works with Python, Jupyter, CLI  

---

# 🧠 Installation Options

You can install DuckDB in 3 ways:

1. Python (recommended for class)  
2. Command Line (CLI)  
3. Jupyter Notebook integration  

---

# 🍎 Mac Installation (Python)

## Step 1 — Install Python (if needed)

Check:
```
python3 --version
```

If not installed:
👉 Install from https://www.python.org

---

# 🍎 Mac — Install DuckDB

```bash
pip3 install duckdb
```

Verify:
```bash
python3 -c "import duckdb; print(duckdb.__version__)"
```

---

# 🍎 Mac — Install Jupyter (optional)

```bash
pip3 install notebook jupysql
```

Start:
```bash
jupyter notebook
```

---

# 🍎 Mac — Test in Python

```python
import duckdb

con = duckdb.connect()
con.execute("SELECT 1").fetchall()
```

---

# 🪟 Windows Installation (Python)

## Step 1 — Install Python

- Download from https://www.python.org  
- IMPORTANT: check “Add Python to PATH”  

Verify:
```
python --version
```

---

# 🪟 Windows — Install DuckDB

```bash
pip install duckdb
```

Verify:
```bash
python -c "import duckdb; print(duckdb.__version__)"
```

---

# 🪟 Windows — Install Jupyter

```bash
pip install notebook jupysql
```

Run:
```bash
jupyter notebook
```

---

# 🪟 Windows — Test

```python
import duckdb

con = duckdb.connect()
con.execute("SELECT 42").fetchall()
```

---

# 💻 Using DuckDB in Jupyter

```python
%load_ext sql
%sql duckdb:///:memory:

%%sql
SELECT 1;
```

---

# ⚠️ Common Problems

### Problem 1 — pip not found
Fix:
```
python -m pip install duckdb
```

---

### Problem 2 — Permission error

Mac:
```
pip3 install --user duckdb
```

Windows:
Run terminal as Administrator

---

### Problem 3 — Wrong Python version

Use:
```
python3 -m pip install duckdb
```

---

# ⚠️ Jupyter Issues

- Use `%%sql` for multi-line SQL  
- Use `%sql` for single-line  
- Restart kernel if extension fails  

---

# 🧪 Quick Test Query

```python
import duckdb

con = duckdb.connect()
df = con.execute("SELECT 'Hello DuckDB'").fetchdf()
print(df)
```

---

# 🚀 Optional: DuckDB CLI

Mac:
```bash
brew install duckdb
```

Windows:
Download from duckdb.org

Run:
```bash
duckdb
```

---

# 📊 Why We Use DuckDB

- No setup (zero config)  
- Fast analytics  
- Works with CSV/Parquet  
- Perfect for teaching  

---

# 🎯 Final Checklist

- Python installed ✅  
- DuckDB installed ✅  
- Jupyter working ✅  
- Test query runs ✅  

---

# 💬 Final Thought

👉 If it runs `SELECT 1`, you’re ready!

---

# 🙌 Need Help?

- Check error message carefully  
- Restart environment  
- Reinstall if needed  
- Ask in class  

👉 Everyone gets it working 👍
