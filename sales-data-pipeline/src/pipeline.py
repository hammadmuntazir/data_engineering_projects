from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "sample-sales.csv"
DATABASE_PATH = PROJECT_DIR / "database" / "sales.db"


def extract_data():
    """Read the sample sales CSV."""
    return pd.read_csv(DATA_PATH)


def validate_data(data):
    """Print basic quality checks and return the original columns."""
    print("Missing values:")
    print(data.isnull().sum())

    print("\nDuplicate rows:", data.duplicated().sum())
    print("Duplicate order IDs:", data["order_id"].duplicated().sum())
    print("\nData types:")
    print(data.dtypes)

    calculated_total = (data["quantity"] * data["unit_price"]).round(2)
    incorrect_totals = (data["total"].round(2) != calculated_total).sum()
    print("\nIncorrect totals:", incorrect_totals)

    return data


def transform_data(data):
    """Add month fields and a simple order-size category."""
    data = data.copy()
    data["date"] = pd.to_datetime(data["date"])
    data["month"] = data["date"].dt.month
    data["month_name"] = data["date"].dt.month_name()
    data["size"] = np.select(
        [data["total"] < 200, data["total"] < 500],
        ["Low", "Medium"],
        default="High",
    )
    return data


def load_data(data):
    """Replace the SQLite sales table with the transformed dataset."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        data.to_sql("sales", connection, if_exists="replace", index=False)
        queries = {
            "Sample rows": "SELECT * FROM sales LIMIT 5",
            "Total revenue": "SELECT SUM(total) AS total_revenue FROM sales",
            "Revenue by product": (
                "SELECT product, SUM(total) AS total_revenue FROM sales "
                "GROUP BY product ORDER BY total_revenue DESC"
            ),
            "Revenue by region": (
                "SELECT region, SUM(total) AS revenue FROM sales "
                "GROUP BY region ORDER BY revenue DESC"
            ),
            "Revenue by salesperson": (
                "SELECT salesperson, SUM(total) AS revenue FROM sales "
                "GROUP BY salesperson ORDER BY revenue DESC"
            ),
            "Monthly revenue": (
                "SELECT month, month_name, SUM(total) AS revenue FROM sales "
                "GROUP BY month, month_name ORDER BY month"
            ),
        }
        for title, query in queries.items():
            print(f"\n{title}:")
            print(pd.read_sql_query(query, connection))


def main():
    data = extract_data()
    data = validate_data(data)
    data = transform_data(data)
    load_data(data)


if __name__ == "__main__":
    main()
