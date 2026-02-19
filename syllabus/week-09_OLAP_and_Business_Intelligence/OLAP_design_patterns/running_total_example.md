# Running Total

Here’s a simple and clear example of using:

### SUM(...) OVER(...)

	SUM(amount) OVER(...): 
	Computes a window function, not a GROUP BY.

in MySQL (8.0+).

⸻

✅ Example: Running Total of Sales per Customer

1️⃣ Sample Table

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
);
```

Sample Data

```sql
INSERT INTO sales VALUES
(1, 101, '2025-01-01', 100.00),
(2, 101, '2025-01-05', 150.00),
(3, 101, '2025-01-10', 200.00),
(4, 102, '2025-01-02', 50.00),
(5, 102, '2025-01-07', 75.00);
```

⸻

2️⃣ Query: Running Total per Customer

```sql
SELECT
    customer_id,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY sale_date
    ) AS running_total
FROM sales
ORDER BY customer_id, sale_date;
```

⸻

🔎 What This Means

- PARTITION BY customer_id

- Resets the calculation for each customer.

- ORDER BY sale_date

- Ensures the sum is cumulative in date order.

- `SUM(amount) OVER(...)`: Computes a window function, not a GROUP BY.

⸻

📊 Output

```
customer_id sale_date  amount  running_total
101         2025-01-01	100.00  100.00
101         2025-01-05	150.00  250.00
101         2025-01-10	200.00  450.00
102         2025-01-02	50.00    50.00
102         2025-01-07	75.00   125.00
```

⸻

🎯 Why This Is Important

Unlike:

```sql
SELECT customer_id, SUM(amount)
FROM sales
GROUP BY customer_id;
```

Window functions:

	•	✅ Keep original rows
	•	✅ Add analytical columns
	•	✅ Enable running totals, moving averages, ranking

⸻

🧠 Bonus: Grand Total (No Partition)

If you remove PARTITION BY:

```sql
SELECT
    sale_id,
    amount,
    SUM(amount) OVER () AS grand_total
FROM sales;
```

This adds the total of all rows to each row.

⸻
