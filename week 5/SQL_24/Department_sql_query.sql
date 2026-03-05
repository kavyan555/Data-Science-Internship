create database Departments;

use Departments;

create table departments (
    dept_id int primary key,
    name varchar(50),
    count_emp_dept int,
    dept_mail_id varchar(100)
);

insert into departments values
(1,'HR',12,'hr@company.com'),
(2,'Finance',10,'finance@company.com'),
(3,'Marketing',15,'marketing@company.com'),
(4,'IT',25,'it@company.com'),
(5,'Sales',18,'sales@company.com'),
(6,'Operations',20,'operations@company.com'),
(7,'Customer Support',14,'support@company.com'),
(8,'Research',8,'research@company.com'),
(9,'Legal',6,'legal@company.com'),
(10,'Admin',11,'admin@company.com'),
(11,'Security',7,'security@company.com'),
(12,'Procurement',9,'procurement@company.com'),
(13,'Training',13,'training@company.com'),
(14,'Logistics',16,'logistics@company.com'),
(15,'Quality Assurance',10,'qa@company.com');

select * from departments;

select * from departments
where count_emp_dept > 10;

select * from departments
order by count_emp_dept desc;

select * from departments
where count_emp_dept > 10 and count_emp_dept < 20;

select * from departments
where name='HR' or name='Finance';

-- Greater than
select * from departments where count_emp_dept > 15;

-- Less than
select * from departments where count_emp_dept < 10;

-- Equal
select * from departments where dept_id = 5;

-- Not equal
select * from departments where dept_id != 3;

-- Greater than or equal
select * from departments where count_emp_dept >= 15;

-- Less than or equal
select * from departments where count_emp_dept <= 10;

update departments
set count_emp_dept = 30
where name = 'IT';

delete from departments
where dept_id = 9;

alter table departments
add location varchar(50);

truncate table departments;

drop table departments;