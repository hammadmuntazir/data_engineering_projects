"""Extract, transform, and load country GDP data from an archived Wikipedia page.

The source page presents GDP estimates sourced from IMF publications. This project
scrapes that page; it does not call an official IMF API.
"""
from __future__ import annotations

import logging
import re
import sqlite3
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = (
    "https://web.archive.org/web/20230902185326/"
    "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
)
TABLE_NAME = "Countries_by_GDP"
OUTPUT_DIR = Path(__file__).resolve().parent / "Output"
GDP_COLUMNS = ["Country", "GDP_USD_Million"]


def extract(url: str = URL) -> pd.DataFrame:
    """Fetch the source page and extract country GDP values in USD millions."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("tbody")
    if len(tables) <= 2:
        raise ValueError("Expected GDP table was not found in the source HTML.")

    records: list[dict[str, object]] = []
    for row in tables[2].find_all("tr")[3:]:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        link = cells[0].find("a")
        country = link.get_text(strip=True) if link else cells[0].get_text(strip=True)
        raw_gdp = cells[2].get_text(" ", strip=True).replace(",", "")
        match = re.search(r"\d+(?:\.\d+)?", raw_gdp)
        if not country or not match:
            continue

        records.append({"Country": country, "GDP_USD_Million": float(match.group())})

    return pd.DataFrame(records, columns=GDP_COLUMNS)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Convert GDP from USD millions to USD billions, rounded to 2 decimals."""
    missing = set(GDP_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    result = pd.DataFrame({"Country": df["Country"].copy()})
    result["GDP_USD_Billion"] = (pd.to_numeric(df["GDP_USD_Million"], errors="raise") / 1000).round(2)
    return result


def load_to_csv(target_file: str | Path, transformed_data: pd.DataFrame) -> None:
    Path(target_file).parent.mkdir(parents=True, exist_ok=True)
    transformed_data.to_csv(target_file, index=False)


def load_to_json(target_file: str | Path, transformed_data: pd.DataFrame) -> None:
    Path(target_file).parent.mkdir(parents=True, exist_ok=True)
    transformed_data.to_json(target_file, orient="records", indent=2)


def load_to_database(
    transformed_data: pd.DataFrame,
    database_name: str | Path,
    table_name: str = TABLE_NAME,
) -> None:
    Path(database_name).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_name) as connection:
        transformed_data.to_sql(table_name, connection, if_exists="replace", index=False)


def query_database(
    database_name: str | Path,
    output_file: str | Path,
    table_name: str = TABLE_NAME,
) -> pd.DataFrame:
    """Export countries with GDP above 100 billion USD and return the result."""
    # table_name is a project constant, not user input.
    query = (
        f'SELECT Country, GDP_USD_Billion FROM "{table_name}" '
        "WHERE GDP_USD_Billion > ? ORDER BY GDP_USD_Billion DESC LIMIT 100"
    )
    with sqlite3.connect(database_name) as connection:
        result = pd.read_sql_query(query, connection, params=(100,))
    load_to_csv(output_file, result)
    return result


def main(output_dir: str | Path = OUTPUT_DIR) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=output_dir / "etl_project_log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )
    try:
        logging.info("ETL process started")
        logging.info("Extracting source data")
        extracted = extract()
        if extracted.empty:
            raise ValueError("Extraction returned no country GDP records.")

        logging.info("Transforming %s records", len(extracted))
        transformed = transform(extracted)
        load_to_csv(output_dir / "Countries_by_GDP.csv", transformed)
        load_to_json(output_dir / "Countries_by_GDP.json", transformed)
        load_to_database(transformed, output_dir / "World_Economies.db")
        query_database(
            output_dir / "World_Economies.db",
            output_dir / "countries_above_100b.csv",
        )
        logging.info("ETL process completed successfully: %s records", len(transformed))
    except Exception:
        logging.exception("ETL process failed")
        raise


if __name__ == "__main__":
    main()
