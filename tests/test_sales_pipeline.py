from pathlib import Path
import sqlite3
import sys

import pandas as pd

# Make the project's src directory importable when pytest runs from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "sales-data-pipeline" / "src"))

import pipeline  # noqa: E402


def sample_sales_data():
    return pd.DataFrame(
        {
            "order_id": ["SO-1", "SO-2", "SO-3", "SO-4"],
            "date": ["2026-01-03", "2026-02-04", "2026-03-05", "2026-04-06"],
            "product": ["Keyboard", "Mouse", "Monitor", "Desk"],
            "quantity": [1, 2, 1, 1],
            "unit_price": [199.99, 100.00, 499.99, 500.00],
            "total": [199.99, 200.00, 499.99, 500.00],
            "region": ["North", "South", "East", "West"],
            "salesperson": ["A", "B", "C", "D"],
        }
    )


def test_transform_data_adds_month_fields_and_expected_size_bands():
    transformed = pipeline.transform_data(sample_sales_data())

    assert transformed["month"].tolist() == [1, 2, 3, 4]
    assert transformed["month_name"].tolist() == [
        "January",
        "February",
        "March",
        "April",
    ]
    assert transformed["size"].tolist() == ["Low", "Medium", "Medium", "High"]


def test_transform_data_does_not_mutate_input():
    source = sample_sales_data()
    original_columns = source.columns.tolist()

    pipeline.transform_data(source)

    assert source.columns.tolist() == original_columns
    assert "month" not in source.columns
    assert not pd.api.types.is_datetime64_any_dtype(source["date"])


def test_validate_data_reports_consistent_totals(capsys):
    data = sample_sales_data()
    pipeline.validate_data(data)

    output = capsys.readouterr().out
    assert "Duplicate order IDs: 0" in output
    assert "Incorrect totals: 0" in output


def test_load_data_creates_sales_table_and_revenue_summary(tmp_path, monkeypatch, capsys):
    database_path = tmp_path / "nested" / "sales.db"
    monkeypatch.setattr(pipeline, "DATABASE_PATH", database_path)

    transformed = pipeline.transform_data(sample_sales_data())
    pipeline.load_data(transformed)

    assert database_path.exists()
    with sqlite3.connect(database_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        total_revenue = connection.execute(
            "SELECT ROUND(SUM(total), 2) FROM sales"
        ).fetchone()[0]

    assert count == 4
    assert total_revenue == 1399.98
    assert "Total revenue" in capsys.readouterr().out
