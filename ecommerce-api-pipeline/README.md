````markdown
# E-Commerce API Data Pipeline

A beginner Data Engineering project that extracts product data from a public API, validates and transforms the data using Python and Pandas, and loads it into PostgreSQL for SQL analytics.

## Project Architecture

Fake Store API
        ↓
Python Requests
        ↓
Raw JSON
        ↓
Pandas DataFrame
        ↓
Validation
        ↓
Transformation
        ↓
PostgreSQL
        ↓
SQL Analytics


## Technologies

- Python
- Requests
- Pandas
- NumPy
- PostgreSQL
- psycopg2
- SQL
- Git / GitHub


## Data Source

The project uses the Fake Store API:

https://fakestoreapi.com/products

The API provides product information including:

- Product ID
- Product title
- Price
- Category
- Description
- Image
- Rating


## Pipeline Steps

### 1. Extract

Python Requests sends a GET request to the Fake Store API.

The raw API response is saved as:

`data/raw_products.json`

### 2. Validate

The pipeline checks:

- Missing values
- Duplicate product IDs
- Data types
- Minimum price
- Maximum price
- Product categories

### 3. Transform

Only the required columns are selected:

- id
- title
- price
- category

A new `price_category` column is created:

- Budget: price < 50
- Mid-range: price < 200
- Premium: price >= 200

### 4. Load

The transformed data is loaded into a PostgreSQL database named:

`ecommerce_db`

The table is:

`products`

The pipeline uses PostgreSQL UPSERT logic so that running the pipeline multiple times does not create duplicate products.

### 5. Analytics

SQL queries are used to analyze:

- Total number of products
- Average price by category
- Most expensive products
- Product counts by price category
- Average price by price category
- Products above a specific price
- Categories with average price above 100


## Database Table

The `products` table contains:

| Column | Type |
|---|---|
| id | INTEGER |
| title | TEXT |
| price | NUMERIC |
| category | TEXT |
| price_category | TEXT |


## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
````

Make sure PostgreSQL is installed and the database exists:

`ecommerce_db`

Update the PostgreSQL password in:

`src/pipeline.py`

Then run:

```bash
python src/pipeline.py
```

The pipeline will:

1. Extract data from the API
2. Save the raw JSON
3. Validate the data
4. Transform the data
5. Load the data into PostgreSQL
6. Complete the pipeline

## Learning Goals

This project was built to practice fundamental Data Engineering concepts:

* API data extraction
* JSON handling
* Data validation
* Data transformation
* ETL pipelines
* PostgreSQL
* Database loading
* UPSERT
* SQL analytics

```
```
