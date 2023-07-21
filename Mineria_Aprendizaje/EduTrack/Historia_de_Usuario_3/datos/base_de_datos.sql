-- Crear la base de datos
CREATE DATABASE learning_tracker_h2;

-- Usar la base de datos
USE learning_tracker_h2;

-- Crear la tabla "estudiantes" para almacenar los datos de los estudiantes
CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    codigo_estudiante VARCHAR(10) NOT NULL,
    promedio DECIMAL(4, 2)
);

-- Crear la tabla "materias" para almacenar los datos de las materias
CREATE TABLE materias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
);

-- Crear la tabla "calificaciones" para almacenar las calificaciones de los estudiantes en las materias
CREATE TABLE calificaciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_estudiante INT,
    id_materia INT,
    calificacion DECIMAL(4, 2) NOT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),
    FOREIGN KEY (id_materia) REFERENCES materias(id)
);

-- Inserción de datos de estudiantes y calificaciones con promedio
INSERT INTO estudiantes (nombre, apellido, edad, codigo_estudiante)
SELECT
    CONCAT('Estudiante', LPAD(number, 3, '0')),
    CONCAT('Apellido', LPAD(number, 3, '0')),
    FLOOR(RAND() * (20 - 15 + 1)) + 15,
    LPAD(number, 3, '0')
FROM
    (SELECT @row := @row + 1 AS number
    FROM
        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL
         SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) t,
        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL
         SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) t2,
        (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL
         SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) t3,
        (SELECT @row := -1) r
    LIMIT 100) numbers;

INSERT INTO materias (nombre)
VALUES ('Matemáticas'), ('Ciencias'), ('Historia'), ('Lenguaje');

INSERT INTO calificaciones (id_estudiante, id_materia, calificacion)
SELECT
    est.id,
    mat.id,
    ROUND(RAND() * 100, 2)
FROM
    estudiantes est
    CROSS JOIN materias mat
ORDER BY
    est.id,
    mat.id;

-- Actualizar promedio de calificaciones
UPDATE estudiantes est
SET est.promedio = (
    SELECT AVG(cal.calificacion)
    FROM calificaciones cal
    WHERE cal.id_estudiante = est.id
);

