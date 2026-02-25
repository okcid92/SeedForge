CREATE DATABASE IF NOT EXISTS seedforge;
USE seedforge;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS torrents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hash VARCHAR(40) UNIQUE NOT NULL,
    size BIGINT,
    seeders INT DEFAULT 0,
    leechers INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'downloading',
    progress FLOAT DEFAULT 0.0,
    category_id INT,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO categories (name) VALUES 
    ('Films'),
    ('Séries'),
    ('Musique'),
    ('Logiciels'),
    ('Jeux'),
    ('Livres');
