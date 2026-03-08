CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(50),
    marks INT
);

INSERT INTO students VALUES
(1,'Rahul',85),
(2,'Anita',92),
(3,'Karan',78),
(4,'Priya',92),
(5,'Arjun',88),
(6,'Neha',78),
(7,'Amit',95),
(8,'Sneha',85);

SELECT 
name,
marks,
RANK() OVER (ORDER BY marks DESC) AS rank_value,
DENSE_RANK() OVER (ORDER BY marks DESC) AS dense_rank_value,
ROW_NUMBER() OVER (ORDER BY marks DESC) AS row_num,
LAG(marks) OVER (ORDER BY marks DESC) AS previous_marks,
LEAD(marks) OVER (ORDER BY marks DESC) AS next_marks
FROM students;