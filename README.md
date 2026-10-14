# Python Data Engineering Portfolio

Hands-on projects focused on extracting data, validating and transforming it, loading it into databases, and writing SQL for analysis. These are learning projects; each README describes the scope and setup for that project.

## Projects in this repository

| Project | What it demonstrates | Main tools |
|---|---|---|
| [Sales Data Pipeline](./sales-data-pipeline/README.md) | Reads sales CSV data, reports data-quality checks, derives date and order-size fields, loads a SQLite table, and runs revenue queries | Python, pandas, NumPy, SQLite, SQL |
| [E-commerce API Pipeline](./ecommerce-api-pipeline/README.md) | Extracts product data from the Fake Store API, saves a raw JSON response, validates/transforms selected fields, and upserts records into PostgreSQL | Python, Requests, pandas, NumPy, PostgreSQL |
| [IMF GDP ETL Practice](./IMF_GDP_ETL_Pipeline/readme.md) | Parses a public archived GDP table, converts units, and exports CSV, JSON, and SQLite outputs | Python, Requests, BeautifulSoup, pandas, SQLite |

## Broader learning portfolio

- [SQL Data Engineering Projects](../SQL_Data_Engineering_Projects) — job-market SQL analysis, a dimensional model, and analytical data marts using DuckDB.
- [SQL Server Data Warehouse Practice](../sql-data-warehouse-projects) — SQL Server database/schema setup and Bronze-layer table scripts.
- [Python and pandas Projects](../Python_Pandas) — data cleaning, feature extraction, and analysis exercises.
- [PySpark Practice](../Pyspark) — notebooks covering Spark sessions, DataFrames, transformations, schemas, and data types.

## Current skill focus

- Python for extraction and transformation
- SQL for joins, aggregations, data models, and analytics
- Data-quality checks and repeatable ETL steps
- SQLite and PostgreSQL fundamentals
- PySpark fundamentals through notebook practice

## Running the projects

Open the README in each project folder for dependencies, database prerequisites, and run instructions. The API project needs network access and a locally available PostgreSQL database. The sales pipeline uses the sample CSV committed in its `data/` folder.

**Reproducibility note:** code and documentation changes should be run and checked in the target environment before treating them as verified. No claim of production deployment is made here.
