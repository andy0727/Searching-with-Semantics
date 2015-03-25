-- create user cs249 and database cs249
-- must be run with mysql root account
CREATE DATABASE cs249;
CREATE USER 'cs249' IDENTIFIED BY 'cs249';
Use cs249
GRANT ALL PRIVILEGES ON cs249.* TO 'cs249'@'localhost' WITH GRANT OPTION;
SET NAMES utf8;