-- 1. Count products
SELECT COUNT(*) FROM products;
#20 

-- 2. Average price by category

SELECT category, AVG(price) AS Average_price
FROM products
GROUP BY category;

--      category     |    average_price     
-- ------------------+----------------------
--  women's clothing |  26.2866666666666667
--  men's clothing   |  51.0575000000000000
--  jewelery         | 220.9950000000000000
--  electronics      | 332.4983333333333333
-- (4 rows)

-- 3. Products from highest to lowest price

SELECT title, price
FROM products
ORDER BY price DESC;

--                                                title                                               | price  
-- ---------------------------------------------------------------------------------------------------+--------
--  Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor (LC49HG90DMNXZA) - Super Ultrawide Screen QLED  | 999.99
--  John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet                       | 695.00
--  Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin                                   | 599.00
--  Solid Gold Petite Micropave                                                                       | 168.00
--  WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive                         | 114.00
--  Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops                                             | 109.95
--  Silicon Power 256GB SSD 3D NAND A55 SLC Cache Performance Boost SATA III 2.5                      | 109.00
--  SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s                                               | 109.00
--  WD 2TB Elements Portable External Hard Drive - USB 3.0                                            |  64.00
--  BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats                                          |  56.99
--  Mens Cotton Jacket                                                                                |  55.99
--  Rain Jacket Women Windbreaker Striped Climbing Raincoats                                          |  39.99
--  Lock and Love Women's Removable Hooded Faux Leather Moto Biker Jacket                             |  29.95
--  Mens Casual Premium Slim Fit T-Shirts                                                             |  22.30
--  Mens Casual Slim Fit                                                                              |  15.99
--  DANVOUY Womens T Shirt Casual Cotton Short                                                        |  12.99
--  Pierced Owl Rose Gold Plated Stainless Steel Double                                               |  10.99
--  White Gold Plated Princess                                                                        |   9.99
--  MBJ Women's Solid Short Sleeve Boat Neck V                                                        |   9.85
--  Opna Women's Short Sleeve Moisture                                                                |   7.95
-- (20 rows)


-- 4.Budget vs Mid-range vs Premium counts
SELECT price_category, COUNT(*)
FROM products
GROUP BY price_category;
--  price_category | count 
-- ----------------+-------
--  Budget         |     9
--  Mid-range      |     8
--  Premium        |     3
-- (3 rows)

-- 5. Average price for each price category
SELECT price_category, AVG(price)
FROM products
GROUP BY price_category;

--  price_category |         avg          
-- ----------------+----------------------
--  Budget         |  17.7777777777777778
--  Mid-range      |  98.3662500000000000
--  Premium        | 764.6633333333333333
-- (3 rows)

-- 6.Products where price is greater than 70
SELECT id, title, price
FROM products
WHERE price > 70;

--  id |                                               title                                               | price  
-- ----+---------------------------------------------------------------------------------------------------+--------
--   1 | Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops                                             | 109.95
--   5 | John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet                       | 695.00
--   6 | Solid Gold Petite Micropave                                                                       | 168.00
--  10 | SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s                                               | 109.00
--  11 | Silicon Power 256GB SSD 3D NAND A55 SLC Cache Performance Boost SATA III 2.5                      | 109.00
--  12 | WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive                         | 114.00
--  13 | Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin                                   | 599.00
--  14 | Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor (LC49HG90DMNXZA) - Super Ultrawide Screen QLED  | 999.99
-- (8 rows)

-- he average price of products in each category, but only include categories whose average price is greater than 100.
SELECT category, AVG(price) AS average_price
FROM products
GROUP BY category
HAVING AVG(price) > 100;

--  category   |    average_price     
-- -------------+----------------------
--  jewelery    | 220.9950000000000000
--  electronics | 332.4983333333333333
-- (2 rows)