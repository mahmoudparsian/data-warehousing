CREATE DATABASE IF NOT EXISTS call_center;
USE call_center;

CREATE TABLE calls (
	id VARCHAR(50),
	customer_name VARCHAR(50),
	sentiment VARCHAR(20),
	csat_score INT,
	call_timestamp VARCHAR(10),
	call_date DATE,              -- added
	quarter INT,                 -- added
	day_of_week VARCHAR(10),     -- added
	day_of_month INT,            -- added
	reason VARCHAR(20),
	city VARCHAR(50),
	state VARCHAR(20),
	channel VARCHAR(24),
	response_time VARCHAR(24),
	call_duration_minutes INT,   -- renamed
	call_center VARCHAR (20)
);



mysql> select * from calls limit 10;
+--------------------------+-----------------------+---------------+------------+----------------+------------+---------+-------------+--------------+------------------+----------------+----------------+-------------+---------------+-----------------------+----------------+
| id                       | customer_name         | sentiment     | csat_score | call_timestamp | call_date  | quarter | day_of_week | day_of_month | reason           | city           | state          | channel     | response_time | call_duration_minutes | call_center    |
+--------------------------+-----------------------+---------------+------------+----------------+------------+---------+-------------+--------------+------------------+----------------+----------------+-------------+---------------+-----------------------+----------------+
| DKK-57076809-w-055481-fU | Analise Gairdner      | Neutral       |          7 | 10/29/2020     | 2020-10-29 |       4 | Thursday    |           29 | Billing Question | Detroit        | Michigan       | Call-Center | Within SLA    |                    17 | Los Angeles/CA |
| QGK-72219678-w-102139-KY | Crichton Kidsley      | Very Positive |       NULL | 10/05/2020     | 2020-10-05 |       4 | Monday      |            5 | Service Outage   | Spartanburg    | South Carolina | Chatbot     | Within SLA    |                    23 | Baltimore/MD   |
| GYJ-30025932-A-023015-LD | Averill Brundrett     | Negative      |       NULL | 10/04/2020     | 2020-10-04 |       4 | Sunday      |            4 | Billing Question | Gainesville    | Florida        | Call-Center | Above SLA     |                    45 | Los Angeles/CA |
| ZJI-96807559-i-620008-m7 | Noreen Lafflina       | Very Negative |          1 | 10/17/2020     | 2020-10-17 |       4 | Saturday    |           17 | Billing Question | Portland       | Oregon         | Chatbot     | Within SLA    |                    12 | Los Angeles/CA |
| DDU-69451719-O-176482-Fm | Toma Van der Beken    | Very Positive |       NULL | 10/17/2020     | 2020-10-17 |       4 | Saturday    |           17 | Payments         | Fort Wayne     | Indiana        | Call-Center | Within SLA    |                    23 | Los Angeles/CA |
| JVI-79728660-U-224285-4a | Kaylyn Emlen          | Neutral       |          5 | 10/28/2020     | 2020-10-28 |       4 | Wednesday   |           28 | Billing Question | Salt Lake City | Utah           | Call-Center | Within SLA    |                    25 | Baltimore/MD   |
| AZI-95054097-e-185542-PT | Phillipe Bowring      | Neutral       |          8 | 10/16/2020     | 2020-10-16 |       4 | Friday      |           16 | Billing Question | Tyler          | Texas          | Chatbot     | Within SLA    |                    31 | Baltimore/MD   |
| TWX-27007918-I-608789-Xw | Krysta de Tocqueville | Positive      |       NULL | 10/21/2020     | 2020-10-21 |       4 | Wednesday   |           21 | Billing Question | New York City  | New York       | Chatbot     | Below SLA     |                    37 | Los Angeles/CA |
| XNG-44599118-P-344473-ZU | Oran Lifsey           | Very Negative |       NULL | 10/03/2020     | 2020-10-03 |       4 | Saturday    |            3 | Billing Question | Dallas         | Texas          | Email       | Below SLA     |                    37 | Baltimore/MD   |
| RLC-64108207-Z-285141-VS | Port Inggall          | Neutral       |       NULL | 10/07/2020     | 2020-10-07 |       4 | Wednesday   |            7 | Billing Question | Cincinnati     | Ohio           | Chatbot     | Within SLA    |                    12 | Baltimore/MD   |
+--------------------------+-----------------------+---------------+------------+----------------+------------+---------+-------------+--------------+------------------+----------------+----------------+-------------+---------------+-----------------------+----------------+
10 rows in set (0.00 sec)
