import sqlite3

import pandas as pd
import pytest

from etl_project_gdp import extract, load_to_csv, load_to_database, query_database, transform


def test_transform_converts_millions_to_billions_and_rounds():
    source = pd.DataFrame(
        {"Country": ["A", "B"], "GDP_USD_Million": [123456.0, 999.0]}
    )

    result = transform(source)

    assert result.to_dict("records") == [
        {"Country": "A", "GDP_USD_Billion": 123.46},
        {"Country": "B", "GDP_USD_Billion": 1.0},
    ]
    assert list(source.columns) == ["Country", "GDP_USD_Million"]


def test_transform_rejects_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        transform(pd.DataFrame({"Country": ["A"]}))


def test_extract_parses_values_and_skips_unavailable_gdp(monkeypatch):
    html = """
    <table><tbody><tr><td>ignore</td></tr></tbody></table>
    <table><tbody><tr><td>ignore</td></tr></tbody></table>
    <table><tbody>
      <tr><td>header</td></tr>
      <tr><td>header</td></tr>
      <tr><td>header</td></tr>
      <tr><td><a href="/wiki/Example">Example</a></td><td>x</td><td>1,234.5</td></tr>
      <tr><td><a href="/wiki/NoGDP">No GDP</a></td><td>x</td><td>—</td></tr>
      <tr><td>Without link</td><td>x</td><td>2,000</td></tr>
    </tbody></table>
    """

    class Response:
        text = html

        def raise_for_status(self):
            return None

    def fake_get(url, timeout):
        assert url == "https://example.test/gdp"
        assert timeout == 30
        return Response()

    monkeypatch.setattr("etl_project_gdp.requests.get", fake_get)
    result = extract("https://example.test/gdp")

    assert result.to_dict("records") == [
        {"Country": "Example", "GDP_USD_Million": 1234.5},
        {"Country": "Without link", "GDP_USD_Million": 2000.0},
    ]


def test_extract_raises_when_expected_table_is_missing(monkeypatch):
    class Response:
        text = "<html><body>No tables</body></html>"

        def raise_for_status(self):
            return None

    monkeypatch.setattr("etl_project_gdp.requests.get", lambda *args, **kwargs: Response())
    with pytest.raises(ValueError, match="Expected GDP table"):
        extract()


def test_database_load_and_threshold_query(tmp_path):
    database = tmp_path / "economies.db"
    output = tmp_path / "above_100b.csv"
    data = pd.DataFrame(
        {
            "Country": ["Large", "Boundary", "Small"],
            "GDP_USD_Billion": [150.0, 100.0, 25.0],
        }
    )

    load_to_database(data, database)
    result = query_database(database, output)

    assert result.to_dict("records") == [{"Country": "Large", "GDP_USD_Billion": 150.0}]
    assert pd.read_csv(output).to_dict("records") == [
        {"Country": "Large", "GDP_USD_Billion": 150.0}
    ]
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM Countries_by_GDP").fetchone()[0] == 3
