use productsdb;

CREATE TABLE amazon_sales (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(50),
    city VARCHAR(50),
    category VARCHAR(50),
    order_value INT,
    order_date DATE
);

INSERT INTO amazon_sales VALUES
(1,101,'Rahul','Bangalore','Electronics',25000,'2025-01-10'),
(2,102,'Anita','Mumbai','Clothing',3500,'2025-01-12'),
(3,103,'Karan','Delhi','Electronics',18000,'2025-01-15'),
(4,104,'Priya','Chennai','Home',6000,'2025-02-01'),
(5,105,'Arjun','Bangalore','Electronics',42000,'2025-02-05'),
(6,101,'Rahul','Bangalore','Books',1200,'2025-02-10'),
(7,106,'Neha','Mumbai','Clothing',4500,'2025-02-12'),
(8,107,'Amit','Delhi','Electronics',22000,'2025-02-20'),
(9,108,'Sneha','Hyderabad','Home',8000,'2025-03-01'),
(10,109,'Ravi','Bangalore','Clothing',3000,'2025-03-05'),
(11,110,'Meena','Chennai','Books',900,'2025-03-10'),
(12,111,'Suresh','Mumbai','Electronics',27000,'2025-03-12'),
(13,112,'Divya','Delhi','Home',7000,'2025-03-15'),
(14,113,'Vikas','Hyderabad','Electronics',35000,'2025-04-01'),
(15,114,'Pooja','Bangalore','Clothing',5000,'2025-04-05'),
(16,115,'Manoj','Mumbai','Home',6500,'2025-04-10'),
(17,116,'Kavya','Chennai','Electronics',24000,'2025-04-15'),
(18,117,'Nikhil','Delhi','Books',1500,'2025-04-18'),
(19,118,'Ritu','Hyderabad','Clothing',3800,'2025-05-01'),
(20,119,'Ajay','Bangalore','Electronics',30000,'2025-05-03'),
(21,120,'Sanjay','Mumbai','Home',7500,'2025-05-06'),
(22,121,'Deepa','Chennai','Clothing',4200,'2025-05-10'),
(23,122,'Varun','Delhi','Electronics',28000,'2025-05-12'),
(24,123,'Asha','Hyderabad','Books',1100,'2025-05-15'),
(25,124,'Ramesh','Bangalore','Home',9000,'2025-05-20');

-- Total sales of the company
SELECT SUM(order_value) AS total_sales
FROM amazon_sales;

-- Total sales by product category
SELECT category, SUM(order_value) AS total_sales
FROM amazon_sales
GROUP BY category;

-- Number of orders per city
SELECT city, COUNT(order_id) AS total_orders
FROM amazon_sales
GROUP BY city;

-- Average order value per customer
SELECT customer_id, AVG(order_value) AS avg_order_value
FROM amazon_sales
GROUP BY customer_id;

-- Highest spending customer
SELECT customer_name, SUM(order_value) AS total_spent
FROM amazon_sales
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 1;

-- Maximum order value in each category
SELECT category, MAX(order_value) AS max_order_value
FROM amazon_sales
GROUP BY category;

-- Cities with sales greater than 50000
SELECT city, SUM(order_value) AS total_sales
FROM amazon_sales
GROUP BY city
HAVING SUM(order_value) > 50000;

-- Number of customers in each city
SELECT city, COUNT(DISTINCT customer_id) AS total_customers
FROM amazon_sales
GROUP BY city;

-- Category with most orders
SELECT category, COUNT(order_id) AS total_orders
FROM amazon_sales
GROUP BY category
ORDER BY total_orders DESC
LIMIT 1;

-- Monthly sales
SELECT MONTH(order_date) AS month, SUM(order_value) AS total_sales
FROM amazon_sales
GROUP BY MONTH(order_date)
ORDER BY month;