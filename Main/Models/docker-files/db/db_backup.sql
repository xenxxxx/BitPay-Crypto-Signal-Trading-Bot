-- Create the crypto_analysis database
CREATE DATABASE IF NOT EXISTS crypto_analysis;
USE crypto_analysis;

-- Create users_db Table
CREATE TABLE IF NOT EXISTS users_db (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create free_signals Table
CREATE TABLE IF NOT EXISTS free_signals (
    sno INT PRIMARY KEY AUTO_INCREMENT,
    signal_title VARCHAR(255) NOT NULL,
    buy_range VARCHAR(50) NOT NULL,
    take_profit VARCHAR(50) NOT NULL,
    stop_loss VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT
);

-- Create comments Table
CREATE TABLE IF NOT EXISTS comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    signal_sno INT,
    user_id INT,
    comment_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create replies Table
CREATE TABLE IF NOT EXISTS replies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    comment_id INT,
    user_id INT,
    reply_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
