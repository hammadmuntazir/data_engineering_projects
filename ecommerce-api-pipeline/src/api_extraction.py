
import json

import numpy as np
import pandas as pd
import psycopg2
import requests


# -------------------------
# 1. EXTRACT
# -------------------------

def extract():
    url = "https://fakestoreapi.com/products"

    response = requests.get(url)

    print("API status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    # Save raw API response
    with open("../data/raw_products.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Raw data saved successfully.")

    return data


# -------------------------
# 2. TRANSFORM & VALIDATE
# -------------------------

def transform(data):

    data_frame = pd.DataFrame(data)

    # Keep required columns
    data_frame = data_frame[
        ["id", "title", "price", "category"]
    ]

    # Validation
    print("\nMissing values:")
    print(data_frame.isnull().sum())

    print(
        "\nDuplicate IDs:",
        data_frame["id"].duplicated().sum()
    )

    print("\nData types:")
    print(data_frame.dtypes)

    print("\nMinimum price:", data_frame["price"].min())
    print("Maximum price:", data_frame["price"].max())

    print("\nCategories:")
    print(data_frame["category"].unique())

    # Create price category
    data_frame["price_category"] = np.select(
        [
            data_frame["price"] < 50,
            data_frame["price"] < 200,
            data_frame["price"] >= 200
        ],
        [
            "Budget",
            "Mid-range",
            "Premium"
        ],
        default="Unknown"
    )

    print("\nTransformation completed.")

    return data_frame


# -------------------------
# 3. LOAD
# -------------------------

def load(data_frame):

    connection = psycopg2.connect(
        host="localhost",
        database="ecommerce_db",
        user="postgres",
        password="your_password",
        port=5432
    )

    print("\nConnected to PostgreSQL.")

    cursor = connection.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT,
            price NUMERIC(10,2),
            category TEXT,
            price_category TEXT
        )
    """)

    # UPSERT
    sql = """
        INSERT INTO products
        (id, title, price, category, price_category)
        VALUES (%s, %s, %s, %s, %s)

        ON CONFLICT (id)
        DO UPDATE SET
            title = EXCLUDED.title,
            price = EXCLUDED.price,
            category = EXCLUDED.category,
            price_category = EXCLUDED.price_category
    """

    for index, row in data_frame.iterrows():

        cursor.execute(
            sql,
            (
                row["id"],
                row["title"],
                row["price"],
                row["category"],
                row["price_category"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print("Data loaded successfully.")


# -------------------------
# MAIN PIPELINE
# -------------------------

data = extract()

data_frame = transform(data)

load(data_frame)

print("\nPipeline completed successfully.")
