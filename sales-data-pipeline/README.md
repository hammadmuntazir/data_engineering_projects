# Sales Data Pipeline

A small end-to-end ETL practice project that reads sales data from CSV, reports data-quality checks, derives analytical fields with pandas, loads the result into SQLite, and runs revenue queries.

## Pipeline

```text
sample-sales.csv
      |
      v
Extract with pandas
      |
      v
Report data-quality checks
(missing values, duplicates, order IDs, total consistency)
      |
      v
Transform dates and classify order sizes
      |
      v
SQLite: sales table
      |
      v
SQL analysis: revenue by product, region, salesperson, and month
```

## Tools

- Python
- pandas and NumPy
- SQLite
- SQL
- pytest for automated tests

## Repository layout

```text
sales-data-pipeline/
├── data/
│   └── sample-sales.csv
├── database/
│   └── sales.db
├── sql/
│   └── analysis.sql
├── src/
│   └── pipeline.py
└── README.md

tests/
└── test_sales_pipeline.py
```

## Input columns

The sample CSV contains `order_id`, `date`, `product`, `quantity`, `unit_price`, `total`, `region`, and `salesperson`.

## What the pipeline does

1. Reads the CSV input.
2. Prints missing-value, duplicate-row, duplicate-order-ID, data-type, and calculated-total checks. These checks currently report results; they do not stop the pipeline on every issue.
3. Converts `date` to a datetime and derives `month` and `month_name`.
4. Adds an order-size category based on `total`: `Low` below 200, `Medium` below 500, and `High` otherwise.
5. Replaces the `sales` table in `database/sales.db`.
6. Prints revenue summaries. The same query examples are in [sql/analysis.sql](./sql/analysis.sql).

## Run

From the repository root:

```bash
python -m pip install -r sales-data-pipeline/requirements.txt
python sales-data-pipeline/src/pipeline.py
```

The script reads the sample file and writes the SQLite database relative to its own file location, so it does not depend on the terminal's current directory.

To run the analysis separately, open `sales-data-pipeline/database/sales.db` with a SQLite client and execute the queries in `sales-data-pipeline/sql/analysis.sql`.

## Run tests

Install the project dependencies and pytest, then run the test suite from the repository root:

```bash
python -m pip install -r sales-data-pipeline/requirements.txt pytest
python -m pytest -q tests/test_sales_pipeline.py
```

A GitHub Actions workflow runs these tests when relevant project files change. The tests cover transformation boundaries, input immutability, quality-check reporting, and SQLite loading.

## Scope and limitations

This is a local ETL learning project. It does not use a cloud scheduler or distributed compute. Data-quality checks are currently reported for inspection rather than enforcing a strict reject/quarantine policy. The automated tests cover core behavior but do not replace a full integration run in your local environment.
