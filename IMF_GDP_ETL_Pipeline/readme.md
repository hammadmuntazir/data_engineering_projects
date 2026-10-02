# 🌍 IMF GDP Data ETL Pipeline

An automated ETL (Extract, Transform, Load) pipeline that extracts country GDP data from the International Monetary Fund (IMF) via Wikipedia, transforms it into billion USD, and loads it into multiple formats for business use.

---

## 🎯 **Project Scenario**

> *An international firm expanding across countries needs an automated script to extract GDP data (in billion USD, rounded to 2 decimals) as updated by the IMF twice a year. The output must be available as JSON, CSV, and a database table, with a query to filter high-economy countries (>100B USD).*

---

## 🔧 **Tech Stack**

| Category | Tools |
|----------|-------|
| Language | Python |
| Web Scraping | Requests, BeautifulSoup |
| Data Processing | Pandas |
| Database | SQLite3 |
| Output Formats | CSV, JSON, SQLite |
| Logging | Custom log file with timestamps |

---

## 📁 **Output Files**

| File | Description |
|------|-------------|
| `Countries_by_GDP.csv` | CSV file with Country and GDP_USD_Billion |
| `Countries_by_GDP.json` | JSON file with same data |
| `World_Economies.db` | SQLite database with table `Countries_by_GDP` |
| `countries_above_100b.csv` | Query result (GDP > 100B USD) |
| `etl_project_log.txt` | Execution log with timestamps |

---

## 🚀 **How to Run**

```bash
# 1. Install dependencies
pip install requests beautifulsoup4 pandas

# 2. Run the script
python etl_project_gdp.py
