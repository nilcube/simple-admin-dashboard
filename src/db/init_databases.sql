CREATE DATABASE app;

USE app;


CREATE TABLE users(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    user VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(300) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);


CREATE TABLE cookies(
    user_id INT NOT NULL,
    token VARCHAR(150) NOT NULL UNIQUE,
    expires_at DATETIME NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users(user, password, is_admin) VALUES ("root", "default", TRUE);
