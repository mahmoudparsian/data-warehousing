### **OLAP (Online Analytical Processing) Operations**  
OLAP operations are used in **data warehousing** and **business intelligence** to analyze large datasets efficiently. These operations allow users to **explore data at different levels of granularity** and across multiple dimensions.

---

## **1. Types of OLAP Operations**  
Here are the key OLAP operations:

### **1. Roll-Up (Aggregation)**
- Moves **from a lower level of detail to a higher level**.
- Aggregates data (e.g., **daily → monthly → yearly**).
- Uses **GROUP BY** in SQL with **SUM, AVG, COUNT, etc.**  
- **Example**:  
  ```sql
  SELECT d.year, SUM(s.sales_amount) AS total_sales
  FROM sales_fact s
  JOIN date_dim d ON s.date_id = d.date_id
  GROUP BY d.year;
  ```
  ✅ **Rolls up** sales from daily to yearly level.

---

### **2. Drill-Down (Roll-Down)**
- Moves **from a higher level of detail to a lower level**.
- Provides more **granular insights** (e.g., **yearly → quarterly → monthly**).  
- **Example**:  
  ```sql
  SELECT d.year, d.quarter, d.month, SUM(s.sales_amount) AS total_sales
  FROM sales_fact s
  JOIN date_dim d ON s.date_id = d.date_id
  GROUP BY d.year, d.quarter, d.month;
  ```
  ✅ **Drills down** sales from **year → quarter → month**.

---

### **3. Slice**
- **Filters** data for a specific value in one dimension while showing all others.  
- **Example**: **Sales in the Electronics category only**  
  ```sql
  SELECT p.category, d.year, SUM(s.sales_amount) AS total_sales
  FROM sales_fact s
  JOIN product_dim p ON s.product_id = p.product_id
  JOIN date_dim d ON s.date_id = d.date_id
  WHERE p.category = 'Electronics'
  GROUP BY d.year;
  ```
  ✅ **Slices the data to show only Electronics sales**.

---

### **4. Dice**
- **Filters multiple dimensions at the same time**.  
- **Example**: **Sales in Q1 of 2024 for Electronics & Home Appliances**  
  ```sql
  SELECT p.category, d.quarter, SUM(s.sales_amount) AS total_sales
  FROM sales_fact s
  JOIN product_dim p ON s.product_id = p.product_id
  JOIN date_dim d ON s.date_id = d.date_id
  WHERE d.year = 2024 AND d.quarter = 'Q1' 
        AND p.category IN ('Electronics', 'Home Appliances')
  GROUP BY p.category, d.quarter;
  ```
  ✅ **Dices the data to filter for Q1, Electronics & Home Appliances**.

---

### **5. Pivot (Rotation)**
- **Rearranges** data to provide different perspectives.  
- **Example**: Showing **years as columns** instead of rows.
  ```sql
  SELECT category,
         SUM(CASE WHEN year = 2022 THEN sales_amount ELSE 0 END) AS sales_2022,
         SUM(CASE WHEN year = 2023 THEN sales_amount ELSE 0 END) AS sales_2023,
         SUM(CASE WHEN year = 2024 THEN sales_amount ELSE 0 END) AS sales_2024
  FROM sales_fact s
  JOIN date_dim d ON s.date_id = d.date_id
  JOIN product_dim p ON s.product_id = p.product_id
  GROUP BY p.category;
  ```
  ✅ **Pivots sales data to compare across years**.

---

## **6. Drill-Through (Detail View)**
- **Retrieves raw transactional data** behind aggregated summaries.
- **Example**: Retrieve all sales transactions for **Q1 2024**.
  ```sql
  SELECT s.*, d.year, d.quarter, p.product_name, c.customer_name, st.store_name
  FROM sales_fact s
  JOIN date_dim d ON s.date_id = d.date_id
  JOIN product_dim p ON s.product_id = p.product_id
  JOIN customer_dim c ON s.customer_id = c.customer_id
  JOIN store_dim st ON s.store_id = st.store_id
  WHERE d.year = 2024 AND d.quarter = 'Q1';
  ```
  ✅ **Shows all sales details for Q1 2024**.

---

## **Summary of OLAP Operations**
| **Operation**   | **Purpose** | **Example** |
|----------------|------------|-------------|
| **Roll-Up**   | Aggregates data (e.g., daily → monthly) | Sales per year |
| **Drill-Down** | Increases detail (e.g., yearly → quarterly) | Sales per month |
| **Slice**     | Filters a single dimension | Only Electronics sales |
| **Dice**      | Filters multiple dimensions | Sales in Q1 for Electronics & Home Appliances |
| **Pivot**     | Rotates data structure | Years as columns instead of rows |
| **Drill-Through** | Retrieves detailed transactional data | All sales in Q1 2024 |

Would you like examples with a different dataset? 😊
