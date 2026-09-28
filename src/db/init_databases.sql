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

CREATE TABLE notes(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    note TEXT NOT NULL DEFAULT (""),
    title TEXT NOT NULL,
    creator_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (creator_id) REFERENCES users(id)

);

INSERT INTO users(user, password, is_admin) VALUES ("root", "default", TRUE);
