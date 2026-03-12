CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

CREATE DATABASE If Not Exists auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE If Not Exists user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('godzionwin@gmail.com','Admin123')
