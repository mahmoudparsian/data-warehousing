Excellent — this is where everything comes together 🔥
Below are 10 advanced OLAP queries + clean plotting code (ready for your notebook & dashboard teaching).

All queries use your Gold star schema.

⸻

📊 Setup (run once)

import matplotlib.pyplot as plt

⸻

1️⃣ Revenue by Month (Trend)

df = con.execute("""
SELECT
    d.year_month,
    ROUND(SUM(f.final_sale_price), 2) AS revenue
FROM gold.fact_sales f
JOIN gold.dim_date d ON f.date_key = d.date_key
GROUP BY d.year_month
ORDER BY d.year_month;
""").df()
plt.figure(figsize=(8,4))
plt.plot(df["year_month"], df["revenue"], marker='o')
plt.title("Revenue Trend by Month")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

⸻

2️⃣ Top 10 Customers by Profit

df = con.execute("""
SELECT
    c.customer_name,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM gold.fact_sales f
JOIN gold.dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_name
ORDER BY total_profit DESC
LIMIT 10;
""").df()
plt.figure(figsize=(8,4))
plt.barh(df["customer_name"], df["total_profit"])
plt.title("Top 10 Customers by Profit")
plt.xlabel("Profit")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

⸻

3️⃣ Revenue by Product Category (Pie Chart)

df = con.execute("""
SELECT
    p.product_category,
    ROUND(SUM(f.final_sale_price), 2) AS revenue
FROM gold.fact_sales f
JOIN gold.dim_product p ON f.product_key = p.product_key
GROUP BY p.product_category
ORDER BY revenue DESC;
""").df()
plt.figure()
plt.pie(df["revenue"], labels=df["product_category"], autopct='%1.1f%%')
plt.title("Revenue by Product Category")
plt.show()

⸻

4️⃣ Profit by Store Location

df = con.execute("""
SELECT
    s.store_location,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM gold.fact_sales f
JOIN gold.dim_store s ON f.store_key = s.store_key
GROUP BY s.store_location
ORDER BY total_profit DESC;
""").df()
plt.figure(figsize=(6,4))
plt.bar(df["store_location"], df["total_profit"])
plt.title("Profit by Store Location")
plt.xlabel("Store")
plt.ylabel("Profit")
plt.tight_layout()
plt.show()

⸻

5️⃣ Sales Channel Distribution

df = con.execute("""
SELECT
    sales_channel,
    COUNT(*) AS transactions
FROM gold.fact_sales
GROUP BY sales_channel;
""").df()
plt.figure()
plt.pie(df["transactions"], labels=df["sales_channel"], autopct='%1.1f%%')
plt.title("Sales Channel Distribution")
plt.show()

⸻

6️⃣ Weekend vs Weekday Revenue

df = con.execute("""
SELECT
    d.day_type,
    ROUND(SUM(f.final_sale_price), 2) AS revenue
FROM gold.fact_sales f
JOIN gold.dim_date d ON f.date_key = d.date_key
GROUP BY d.day_type;
""").df()
plt.figure(figsize=(5,4))
plt.bar(df["day_type"], df["revenue"])
plt.title("Weekend vs Weekday Revenue")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

⸻

7️⃣ Top 5 Products by Revenue

df = con.execute("""
SELECT
    p.product_name,
    ROUND(SUM(f.final_sale_price), 2) AS revenue
FROM gold.fact_sales f
JOIN gold.dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;
""").df()
plt.figure(figsize=(6,4))
plt.bar(df["product_name"], df["revenue"])
plt.title("Top 5 Products by Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

⸻

8️⃣ Monthly Profit Trend by Store (Grouped Bars)

df = con.execute("""
SELECT
    d.year_month,
    s.store_location,
    ROUND(SUM(f.profit), 2) AS profit
FROM gold.fact_sales f
JOIN gold.dim_date d ON f.date_key = d.date_key
JOIN gold.dim_store s ON f.store_key = s.store_key
GROUP BY d.year_month, s.store_location
ORDER BY d.year_month;
""").df()
pivot = df.pivot(index="year_month", columns="store_location", values="profit")
pivot.plot(kind="bar", figsize=(10,4))
plt.title("Monthly Profit by Store")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

⸻

9️⃣ Discount Impact Analysis

df = con.execute("""
SELECT
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount < 50 THEN 'Low Discount'
        ELSE 'High Discount'
    END AS discount_bucket,
    ROUND(AVG(profit), 2) AS avg_profit
FROM gold.fact_sales
GROUP BY discount_bucket;
""").df()
plt.figure(figsize=(6,4))
plt.bar(df["discount_bucket"], df["avg_profit"])
plt.title("Discount Impact on Profit")
plt.ylabel("Avg Profit")
plt.tight_layout()
plt.show()

⸻

🔟 Customer Segment Revenue

df = con.execute("""
SELECT
    c.customer_segment,
    ROUND(SUM(f.final_sale_price), 2) AS revenue
FROM gold.fact_sales f
JOIN gold.dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_segment;
""").df()
plt.figure(figsize=(6,4))
plt.bar(df["customer_segment"], df["revenue"])
plt.title("Revenue by Customer Segment")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

⸻

🧠 Teaching Value (what students learn)

These queries cover:

* ✔ aggregation (SUM, AVG, COUNT)
* ✔ grouping (GROUP BY)
* ✔ joins across star schema
* ✔ time-series analysis
* ✔ segmentation
* ✔ top-N analytics
* ✔ business insight generation

⸻

🚀 If you want next level

I can upgrade this to:

* 📊 Executive dashboard layout (one page)
* 📈 KPI tiles + charts
* 🧠 Business insights written for each query
* 🎓 Student vs Instructor versions

Just say 👍
