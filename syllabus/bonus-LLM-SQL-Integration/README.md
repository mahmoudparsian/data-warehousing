# Bonus (optional): LLM + SQL Integration

> **Optional module, not part of the 10 weeks.** It shows how a Large Language Model (LLM) can turn a
> question in plain English into SQL, and turn query results back into plain English.
> The examples use **MySQL** and the **OpenAI** API (reference code). The ideas work the same with DuckDB and other LLM providers.

## ⚠️ Before you run anything

- You need an **OpenAI API key** (paid usage), Python packages `openai` and `mysql-connector-python`, and a MySQL server with
  the sample data in [`db_schema/`](db_schema/) (`mysql_sample_schema.sql` + the CSV files).
- **Never put your API key in a file.** Set it in your shell; the `progs/example_*.py` scripts read it from there:
  `export OPENAI_API_KEY="sk-..."` (macOS/Linux) · `setx OPENAI_API_KEY "sk-..."` (Windows).
  `.env` files and `.streamlit/secrets.toml` are git-ignored.
- `progs/example_1…3_*.py` use the current OpenAI Python client (`openai >= 1.0`).
  The two old Streamlit apps (retired OpenAI API) were archived; a working Streamlit app is in Part 2 of the walkthrough below.
- LLM-generated SQL can be wrong. **Always read the SQL before running it**, and use a read-only database user.

## Where to start

1. [`docs/LLM_MySQL_Integration_example.md`](docs/LLM_MySQL_Integration_example.md): walkthrough with code (NL → SQL, SQL → NL, LangChain)
2. `progs/example_1_NL_to_SQL.py` → `example_2_NL_to_SQL.py` → `example_3_Reverse_Mapping_SQL_to_Natural_Language.py`
3. [`progs/new_examples/3_examples.md`](progs/new_examples/3_examples.md) and `mysql_openai_integration.py`: query summarization and a chat-to-insights example
4. `MySQL_LLM_Integration_Slides.pptx` and [`docs/LLM_MySQL_Integration_with_LangChain.pdf`](docs/LLM_MySQL_Integration_with_LangChain.pdf)

---

# MySQL and LLM Integration?

# 1. Files in this folder:

| File / folder | Description |
|---|---|
| `db_schema` | Sample database schema |
| `docs`      | Basic documentation and references|
|`MySQL_LLM_Integration_Slides.pptx` | PowerPoint Slides |
| `progs` | Sample integration programs|
| `README.md` | Landing Page |

# 2. What is MySQL and LLM Integration?

	MySQL and Large Language Model (LLM) integration 
	refers to the process of connecting and leveraging 
	LLMs with MySQL databases to enhance data interaction, 
	analysis, and application development. This integration 
	primarily focuses on enabling LLMs to understand and 
	interact with structured data stored in MySQL, often 
	in a natural language format.

# 3. Key aspects of MySQL and LLM Integration

### Natural Language to SQL Generation:
	LLMs can be used to translate natural language 
	queries from users into executable SQL queries 
	for MySQL. This allows non-technical users to 
	retrieve and analyze data without needing SQL 
	knowledge.

### Data Retrieval and Summarization:
	LLMs can query the MySQL database, retrieve 
	relevant information, and then summarize or 
	present it in a human-readable format, making 
	data insights more accessible.

### Contextual Understanding:
	LLMs can be provided with the schema of MySQL 
	tables, allowing them to understand the database 
	structure and generate more accurate and contextually 
	relevant SQL queries.

### Enhanced Chatbots and Applications:
	Integrating LLMs with MySQL enables the creation 
	of more intelligent chatbots and applications that 
	can answer questions and perform actions based on 
	the data stored in the database.

### Vector Search and Embeddings:
	For advanced use cases like semantic search, vector 
	embeddings of data can be stored in MySQL (or compatible 
	databases like TiDB) and queried using vector search 
	techniques, allowing LLMs to retrieve data based on 
	semantic similarity.

### Secure Data Access:
	Integration often involves establishing secure, 
	read-only access for LLMs to MySQL databases, 
	ensuring data integrity and preventing 
	unintended modifications.

# 4. Common use cases for this integration include:

### AI-powered analytics assistants:
	LLMs can help users analyze data in MySQL by 
	generating queries and interpreting results.

### Database-driven chatbots:
	Chatbots can answer user questions by retrieving 
	information directly from a MySQL database.

### Automated report generation:
	LLMs can generate reports by querying and summarizing 
	data from MySQL.

### Semantic search for data:
	LLMs can facilitate searching for data based on 
	its meaning rather than just keywords.
