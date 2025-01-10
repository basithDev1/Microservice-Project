DROP USER IF EXISTS 'auth-user'@'localhost';
DROP DATABASE IF EXISTS auth;

-- Create user, database, and table
CREATE USER 'auth-user'@'localhost' IDENTIFIED BY 'Auth123';
CREATE DATABASE auth;
GRANT ALL PRIVILEGES ON auth.* TO 'auth-user'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('basithunny@gmail.com', 'Unny1243');