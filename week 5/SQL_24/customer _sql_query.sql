create database customerdb;

use customerdb;

create table customer(
cust_id int primary key,
name varchar(20),
email varchar(100),
reg_date date);

insert into customer values
(101, 'Alex', 'alex34@gmail.com', '2020-02-02'),
(102, 'Bob', 'bob54@gmail.com', '2020-12-02'),
(103, 'Charlie', 'charlie@gmail.com', '2022-02-23'),
(104, 'Dexter', 'dexter@gmail.com', '2022-05-02'),
(105, 'Emily', 'emily@gmail.com', '2023-02-02'),
(106, 'Kiran', 'kiran@gmail.com', '2023-08-25'),
(107, 'Manu', 'manu@gmail.com', '2024-01-23'),
(108, 'Meena', 'meena@gmail.com', '2024-02-02'),
(109, 'Rahul', 'rahul@gmail.com', '2025-06-02'),
(110, 'Sneha', 'sneha@gmail.com', '2026-02-02');

select * from customer;

select * from customer where cust_id=108;

select * from customer 
order by reg_date desc;

select * from customer
where cust_id=101 and name='Alex';

select * from customer
where reg_date='2025-01-01' or name= 'Bob';

SELECT * 
FROM customer
WHERE reg_date BETWEEN '2025-01-01' AND '2026-12-12';

update customer
set email='alex@gmail.com'
where cust_id=101;

alter table customer
add location varchar(50);

delete from customer where cust_id=107;

truncate table customer;
select * from customer;

drop table customer;

drop database customerdb;