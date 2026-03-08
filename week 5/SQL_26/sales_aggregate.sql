use productsdb;

CREATE TABLE sales (
    id INT PRIMARY KEY,
    product_name VARCHAR(50),
    price INT
);

INSERT INTO sales VALUES (1,'Laptop',55000);
INSERT INTO sales VALUES (2,'Mouse',500);
INSERT INTO sales VALUES (3,'Keyboard',1200);
INSERT INTO sales VALUES (4,'Monitor',15000);
INSERT INTO sales VALUES (5,'Headphones',2000);
INSERT INTO sales VALUES (6,'Speaker',3500);
INSERT INTO sales VALUES (7,'Webcam',2500);
INSERT INTO sales VALUES (8,'Tablet',22000);
INSERT INTO sales VALUES (9,'Smartphone',30000);
INSERT INTO sales VALUES (10,'Charger',800);
INSERT INTO sales VALUES (11,'USB Cable',300);
INSERT INTO sales VALUES (12,'Hard Disk',6000);
INSERT INTO sales VALUES (13,'SSD',7500);
INSERT INTO sales VALUES (14,'Router',2800);
INSERT INTO sales VALUES (15,'Printer',9000);
INSERT INTO sales VALUES (16,'Scanner',7000);
INSERT INTO sales VALUES (17,'Power Bank',1500);
INSERT INTO sales VALUES (18,'Smart Watch',4500);
INSERT INTO sales VALUES (19,'Camera',40000);
INSERT INTO sales VALUES (20,'Tripod',1200);
INSERT INTO sales VALUES (21,'Microphone',3200);
INSERT INTO sales VALUES (22,'Projector',25000);
INSERT INTO sales VALUES (23,'VR Headset',18000);
INSERT INTO sales VALUES (24,'Graphics Card',45000);
INSERT INTO sales VALUES (25,'Cooling Pad',900);

SELECT SUM(price) AS total_sales
FROM sales;

SELECT MIN(price) AS minimum_price
FROM sales;

SELECT MAX(price) AS maximum_price
FROM sales;

SELECT AVG(price) AS average_price
FROM sales;

SELECT COUNT(*) AS total_products
FROM sales;

SELECT 
    SUM(price) AS total_price,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price,
    AVG(price) AS average_price,
    COUNT(*) AS total_products
FROM sales;