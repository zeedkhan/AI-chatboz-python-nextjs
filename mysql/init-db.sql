-- Create user and grant privileges
GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' WITH GRANT OPTION;

-- Create database
CREATE DATABASE IF NOT EXISTS main;
