
-- 1. View sample records
SELECT *
FROM sales
LIMIT 5;


-- 2. Total revenue
SELECT SUM(total) AS total_revenue
FROM sales;


-- 3. Revenue by product
SELECT
    product,
    SUM(total) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;


-- 4. Revenue by region
SELECT
    region,
    SUM(total) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;


-- 5. Revenue by salesperson
SELECT
    salesperson,
    SUM(total) AS revenue
FROM sales
GROUP BY salesperson
ORDER BY revenue DESC;


-- 6. Monthly revenue
SELECT
    month,
    month_name,
    SUM(total) AS revenue
FROM sales
GROUP BY month, month_name
ORDER BY month;
