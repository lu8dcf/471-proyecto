CREATE DATABASE IF NOT EXISTS ejemplo;
USE ejemplo;
CREATE TABLE IF NOT EXISTS person(
    id INT(100) NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    dni INT(8) NOT NULL,
    email VARCHAR(64) NOT NULL,
    PRIMARY KEY (id)
); 

-- Agregar valores

INSERT INTO person VALUES
(1, 'Juan', 'Alvarez', 1234545, 'juan@gmail.com'),
(2, 'Lara', 'Lepron', 6234545, 'lara@gmail.com');


INSERT INTO person VALUES
(3, 'Pedro', 'Alvaradoz', 1244545, 'juan44@gmail.com'),
(4, 'Laura', 'Leprone', 6274545, 'lara33@gmail.com');


CREATE TABLE IF NOT EXISTS users(
    id INT(10) NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,
    PRIMARY KEY (id)
); 
INSERT INTO users VALUES
(1, 'admin', 'admin')