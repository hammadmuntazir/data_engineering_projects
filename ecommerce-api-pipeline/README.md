# E-commerce API Data Pipeline

A practical ETL learning project that extracts product data from the public Fake Store API, saves the raw response, validates and transforms selected fields, loads the result into PostgreSQL, and supports SQL analysis.

## Architecture

```text
Fake Store API
    |
    v
Python Requests -> raw_products.json
    |
    v
pandas validation and transformation
    |
    v
PostgreSQL products table (upsert by product ID)
    |
    v
SQL analytics
```

## Tech stack

Python, Requests, pandas, NumPy, PostgreSQL, psycopg2, and SQL.

## Data source

The pipeline requests product records from [Fake Store API](https://fakestoreapi.com/products). It retains `id`, `title`, `price`, and `category`, then derives `price_category`:

- `Budget`: price below 50
- `Mid-range`: price from 50 up to (but not including) 200
- `Premium`: price 200 or above

The script reports missing values, duplicate IDs, data types, price range, and categories. It writes the raw response to `data/raw_products.json` and upserts transformed rows into PostgreSQL table `products`.

## Repository layout

```text
ecommerce-api-pipeline/
├── data/
│   └── raw_products.json
├── sql/
│   └── analysis.sql
├── src/
│   └── api_extraction.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- A running local PostgreSQL server
- A PostgreSQL database named `ecommerce_db`
- Network access to the API

## Setup and run

From the repository root, install dependencies:

```bash
python -m pip install -r ecommerce-api-pipeline/requirements.txt
```

Create the database if it does not already exist:

```sql
CREATE DATABASE ecommerce_db;
```

Set the password as an environment variable rather than saving credentials in the source code.

PowerShell:

```powershell
$env:PGPASSWORD = "your-local-postgres-password"
python ecommerce-api-pipeline/src/api_extraction.py
```

macOS/Linux shell:

```bash
export PGPASSWORD="your-local-postgres-password"
python ecommerce-api-pipeline/src/api_extraction.py
```

Optional connection settings are read from `PGHOST` (default `localhost`), `PGPORT` (default `5432`), `PGDATABASE` (default `ecommerce_db`), and `PGUSER` (default `postgres`). Never commit a real password or token.

## SQL analysis

Run the queries in [sql/analysis.sql](./sql/analysis.sql) against the `ecommerce_db` database after the pipeline has loaded the `products` table. The queries cover product counts, category prices, price bands, and other basic summaries.

## Scope and limitations

This is a small, local ETL project—not a hosted service or production-grade pipeline. The script currently reports several quality checks for inspection; it does not implement a separate automated test suite.
