-- https://stackoverflow.com/questions/56216465/create-postgres-database-if-it-does-not-exist-on-docker-compose-start-up
SELECT datname
FROM pg_database
WHERE datname='main'';
    IF NOT FOUND THEN
        CREATE DATABASE main;
    END IF;'