-- Crear la base de datos
CREATE DATABASE learning_tracker;

-- Usar la base de datos
USE learning_tracker;

-- Crear la tabla de estudiantes
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    grade INT,
    average_grade FLOAT
);

-- Generar 100 registros de datos aleatorios
INSERT INTO students (name, age, grade, average_grade)
SELECT
    CONCAT('Estudiante ', LPAD(FLOOR(RAND() * 1000), 3, '0')),
    FLOOR(RAND() * 10) + 15,
    FLOOR(RAND() * 12) + 1,
    ROUND(RAND() * 100, 2)
FROM
    (SELECT @i := 0) AS init
CROSS JOIN
    information_schema.tables AS t1
CROSS JOIN
    information_schema.tables AS t2
WHERE
    (@i := @i + 1) <= 100;
