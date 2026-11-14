# Data warehousing KPIs (Key Performance Indicators) 

	Data warehousing KPIs (Key Performance Indicators) 
	measure the efficiency, accuracy, and value of a 
	data warehouse system to the business. 
	
	Key metrics focus on data quality (accuracy, 
	consistency), system performance (latency, uptime), 
	and business value (user adoption, report accuracy) 
	to ensure data-driven decision-making.

# Practical KPI examples

	Here are practical KPI examples you can use in a 
	data warehousing / analytics context—these map 
	nicely to fact tables, dimensions, and typical 
	SQL exercises.
	
# 🧠 Teaching Insight (very important)

KPIs in DW typically follow:

		AGGREGATE (fact)
			+ GROUP BY (dimension)

👉 Examples:

| KPI        | Fact            | Dimension  |
|------------|-----------------|------------|
| Revenue    | sales_amount    | time       |
| Visits     | count(*)        | year/month |
| Customers  | distinct count  | region     |

⸻

🎓 Golden takeaway for students

A KPI is just:

Aggregation + Business Meaning


⸻

## 📊 1. Sales / Revenue KPIs

💰 Total Revenue

	•	Definition: Total sales amount over a period
	•	DW mapping: SUM(sales_amount) from fact table

```sql
SELECT SUM(sales_amount) AS total_revenue
FROM fact_sales;
```

⸻

## 📈 2. Revenue Growth Rate

	•	Definition: % change compared to previous period

```sql
SELECT 
  year,
  SUM(sales_amount) AS revenue,
  LAG(SUM(sales_amount)) OVER (ORDER BY year) AS prev_revenue,
  (SUM(sales_amount) - LAG(SUM(sales_amount)) OVER (ORDER BY year))
  / LAG(SUM(sales_amount)) OVER (ORDER BY year) AS growth_rate
FROM fact_sales
GROUP BY year;
```

⸻

## 🛒 3. Customer KPIs

👤 Customer Count

	•	Definition: Number of unique customers

```sql
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM fact_sales;
```

⸻

## 🔁 4. Customer Retention Rate

	•	Definition: Customers who return in next period

👉 Conceptually:

Returning Customers / Total Customers


⸻

## 📦 5. Order KPIs

📦 Total Orders

```sql
SELECT COUNT(*) AS total_orders
FROM fact_orders;
```

⸻

## 💵 6. Average Order Value (AOV)

	•	Definition: Revenue per order

```sql
SELECT 
  SUM(order_amount) / COUNT(*) AS avg_order_value
FROM fact_orders;
```

⸻

## 🌍 7. Dimensional KPIs (Slice & Dice)

🌎 Revenue by Region

```sql
SELECT region, 
       SUM(sales_amount) AS revenue
FROM fact_sales
GROUP BY region;
```

⸻

## 🗓️ 8. Monthly Visits (your dataset!)

```sql
SELECT year, month, 
       COUNT(*) AS visits
FROM gold.visits
GROUP BY year, month
ORDER BY year, month;
```

⸻

## 🏛️ 9. White House Dataset KPIs (your project)

👥 Top Visitors

```sql
SELECT visitor_name, 
       COUNT(*) AS visits
FROM gold.visits
GROUP BY visitor_name
ORDER BY visits DESC
LIMIT 10;
```

⸻

## 🏢 10. Visits by Location

```sql
SELECT meeting_loc, 
       COUNT(*) AS visits
FROM gold.visits
GROUP BY meeting_loc
ORDER BY visits DESC;
```

⸻

## 🎯 11. Time-Based KPI (very important)

⏱️ Visits Trend

```sql
SELECT year, 
       COUNT(*) AS visits
FROM gold.visits
GROUP BY year
ORDER BY year;
```

