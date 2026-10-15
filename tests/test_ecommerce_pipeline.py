from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "ecommerce-api-pipeline" / "src"))

import api_extraction  # noqa: E402


def test_transform_assigns_price_categories_at_boundaries():
    products = [
        {"id": 1, "title": "Under 50", "price": 49.99, "category": "test"},
        {"id": 2, "title": "Exactly 50", "price": 50.00, "category": "test"},
        {"id": 3, "title": "Under 200", "price": 199.99, "category": "test"},
        {"id": 4, "title": "Exactly 200", "price": 200.00, "category": "test"},
    ]

    result = api_extraction.transform(products)

    assert result["price_category"].tolist() == [
        "Budget",
        "Mid-range",
        "Mid-range",
        "Premium",
    ]
    assert result["id"].tolist() == [1, 2, 3, 4]


def test_transform_selects_expected_columns_and_keeps_source_records():
    products = [
        {
            "id": 10,
            "title": "Keyboard",
            "price": 75.00,
            "category": "electronics",
            "description": "Extra field should not be loaded",
        }
    ]

    result = api_extraction.transform(products)

    assert result.columns.tolist() == [
        "id",
        "title",
        "price",
        "category",
        "price_category",
    ]
    assert products[0]["description"] == "Extra field should not be loaded"
    assert result.loc[0, "price_category"] == "Mid-range"


def test_transform_reports_duplicate_ids(capsys):
    products = [
        {"id": 1, "title": "First", "price": 10.0, "category": "test"},
        {"id": 1, "title": "Duplicate", "price": 20.0, "category": "test"},
    ]

    api_extraction.transform(products)

    assert "Duplicate IDs: 1" in capsys.readouterr().out
