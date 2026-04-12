use departments;

CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

INSERT INTO departments VALUES (1, 'HR');
INSERT INTO departments VALUES (2, 'IT');
INSERT INTO departments VALUES (3, 'Finance');
INSERT INTO departments VALUES (4, 'Marketing');

CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_id INT,
    salary INT,
    address VARCHAR(100),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

INSERT INTO employee VALUES (101, 'John', 1, 50000, 'Bangalore');
INSERT INTO employee VALUES (102, 'Sara', 2, 60000,'hyderabad');
INSERT INTO employee VALUES (103, 'David', 3, 50000, 'mangalore');
INSERT INTO employee VALUES (104, 'Emma', 1, 40000,'bangalore');
INSERT INTO employee VALUES (105, 'Alex', 2,70000,'anekal');
INSERT INTO employee(emp_id, name, salary,address)
 VALUES (106, 'Bob',70000,'anekal');
INSERT INTO employee VALUES (107, 'Alex', 2,70000,'anekal');

-- employee name and dept name
SELECT e.name, d.dept_name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id;

-- employees who don't belong to any department
SELECT name
FROM employee
WHERE dept_id IS NULL;

-- departments without employees
SELECT d.dept_name
FROM departments d
LEFT JOIN employee e
ON d.dept_id = e.dept_id
WHERE e.emp_id IS NULL;

-- employee count per department
SELECT d.dept_name, COUNT(e.emp_id) AS employee_count
FROM departments d
LEFT JOIN employee e
ON d.dept_id = e.dept_id
GROUP BY d.dept_name;

-- highest salary in each department
SELECT d.dept_name, MAX(e.salary) AS highest_salary
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
GROUP BY d.dept_name;

-- department with more than 2 employees
SELECT d.dept_name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING COUNT(e.emp_id) > 2;

-- employees working in the IT department
SELECT e.name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
WHERE d.dept_name = 'IT';

-- employees working in the HR department
SELECT e.name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
WHERE d.dept_name = 'HR';

-- employees working in the Finance department
SELECT e.name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Finance';

-- employees belonging to Marketing department
SELECT e.name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Marketing';

-- employees belonging to non-IT department
SELECT e.name
FROM employee e
JOIN departments d
ON e.dept_id = d.dept_id
WHERE d.dept_name <> 'IT';