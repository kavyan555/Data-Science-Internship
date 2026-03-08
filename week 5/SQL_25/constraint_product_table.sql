create database productsdb;

use productsdb;

create table products (
    product_id int primary key,
    product_name varchar(100) not null,
    price decimal(10,2) check (price > 0),
    category varchar(50) default 'accessories'
);

insert into products (product_id, product_name, price, category)
values (1, 'Watch', 2500, 'electronics');

insert into products 
values (2, 'Bracelet', 500, 'fashion');

insert into products (product_id, product_name, price, category)
values (3, 'Sunglasses', 600, 'fashion');

insert into products (product_id, product_name, price, category)
values (4, 'Cap', 300, 'accessories');

insert into products (product_id, product_name, price, category)
values (5, 'chain', 800, 'fashion');

-- not null constraint
INSERT INTO products (product_id, price)
VALUES (6, 500);

-- check constraint
INSERT INTO products VALUES (7, 'Bag', -200, 'fashion');

-- primary key
INSERT INTO products VALUES (1, 'Shoes', 2000, 'fashion');

truncate table products;

