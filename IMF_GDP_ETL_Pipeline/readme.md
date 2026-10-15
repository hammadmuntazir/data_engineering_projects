# Country GDP ETL Pipeline

A small Python ETL project that scrapes a historical Wikipedia page whose GDP estimates are attributed to IMF publications, converts GDP values from USD millions to USD billions, and writes CSV, JSON, and SQLite outputs.

> **Source limitation:** this project scrapes an archived Wikipedia page. It does not call an official IMF API, and the archived snapshot is historical rather than a live twice-yearly feed.

## Pipeline

1. **Extract:** fetch the archived page with a timeout and HTTP status check, then parse country GDP values.
2. **Transform:** convert USD millions to USD billions and round to two decimal places.
3. **Load:** write CSV and JSON files and replace the SQLite `Countries_by_GDP` table.
4. **Query:** export up to 100 countries with GDP strictly greater than USD 100 billion, sorted by GDP descending.
5. **Logging:** record successful completion or the exception in the output directory's log file.

## Tech stack

Python, Requests, BeautifulSoup, pandas, SQLite, pytest, and GitHub Actions.

## Run locally

From this directory:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python etl_project_gdp.py
```

Outputs are written to `Output/`: `Countries_by_GDP.csv`, `Countries_by_GDP.json`, `World_Economies.db`, `countries_above_100b.csv`, and `etl_project_log.txt`.

## Run tests

```bash
pytest -q
```

Tests mock the source HTML and do not depend on a live website or an external database.

## Scope and limitations

- The source HTML structure can change, so extraction may need maintenance.
- The archived page represents a historical snapshot; the outputs should not be presented as current GDP figures.
- The pipeline uses SQLite and local files for a learning/demo workflow, not a production data platform.
