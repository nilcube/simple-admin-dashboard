CREATE DATABASE app;

USE app;


CREATE TABLE users(
    _id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    user VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(300) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);


insert into users(user, password) VALUES ("root", "default");
