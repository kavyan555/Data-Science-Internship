use productsdb;

CREATE VIEW sales_view AS
SELECT id, product_name, price
FROM sales;

SELECT 
    price,
    CEIL(price) AS ceil_price,
    ABS(price) AS abs_price,
    ROUND(price,2) AS rounded_price,
    SQRT(price) AS square_root,
    POWER(price,2) AS power_value,
    MOD(price,10) AS remainder_value,
    EXP(price/1000) AS exponential_value
FROM sales_view;