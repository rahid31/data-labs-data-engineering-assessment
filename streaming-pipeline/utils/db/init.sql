CREATE DATABASE IF NOT EXISTS stg_transactions;

USE stg_transactions;

CREATE TABLE IF NOT EXISTS transactions (
  id VARCHAR(255) PRIMARY KEY,
  user_id INT,
  amount FLOAT,
  created_at DATETIME
);

CREATE TABLE IF NOT EXISTS transaction_aggs (
  minute_key VARCHAR(20) PRIMARY KEY,
  total_count INT
);

CREATE USER IF NOT EXISTS 'admin_user'@'%' IDENTIFIED BY 'admin123!';
GRANT ALL PRIVILEGES ON stg_transactions.* TO 'admin_user'@'%';
FLUSH PRIVILEGES;