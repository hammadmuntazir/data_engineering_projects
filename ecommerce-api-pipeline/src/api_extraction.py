import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import psycopg2
import requests


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw_products.json"


def extract():
    """Fetch product data and save an unchanged copy of the raw JSON response."""
    url = "https://fakestoreapi.com/products"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RAW_DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved raw API response to {RAW_DATA_PATH}")
    return data


def transform(data):
    """Select fields, report basic quality checks, and derive a price band."""
    data_frame = pd.DataFrame(data)[["id", "title", "price", "category"]].copy()

    print("\nMissing values:")
    print(data_frame.isnull().sum())
    print("\nDuplicate IDs:", data_frame["id"].duplicated().sum())
    print("\nData types:")
    print(data_frame.dtypes)
    print("\nMinimum price:", data_frame["price"].min())
    print("Maximum price:", data_frame["price"].max())
    print("\nCategories:")
    print(data_frame["category"].unique())

    data_frame["price_category"] = np.select(
        [
            data_frame["price"] < 50,
            data_frame["price"] < 200,
            data_frame["price"] >= 200,
        ],
        ["Budget", "Mid-range", "Premium"],
        default="Unknown",
    )

    return data_frame


def load(data_frame):
    """Upsert transformed products into a local PostgreSQL database."""
    password = os.getenv("PGPASSWORD")
    if not password:
        raise RuntimeError(
            "Set the PGPASSWORD environment variable before running the pipeline."
        )

    connection = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        database=os.getenv("PGDATABASE", "ecommerce_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=password,
        port=int(os.getenv("PGPORT", "5432")),
    )

    upsert_sql = """
        INSERT INTO products
            (id, title, price, category, price_category)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            price = EXCLUDED.price,
            category = EXCLUDED.category,
            price_category = EXCLUDED.price_category
    """

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        price NUMERIC(10, 2),
                        category TEXT,
                        price_category TEXT
                    )
                    """
                )
                rows = data_frame[
                    ["id", "title", "price", "category", "price_category"]
                ].itertuples(index=False, name=None)
                cursor.executemany(upsert_sql, list(rows))
        print("Data loaded successfully.")
    finally:
        connection.close()


def main():
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
