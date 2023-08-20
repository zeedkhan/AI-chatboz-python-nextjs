from fastapi import FastAPI, Depends, HTTPException
import mysql.connector
import psycopg2


app = FastAPI()


def connect_to_mysql_and_fetch_data(sql_command):
    # Database connection parameters
    postgres_params = {
        "host": "db_postgres",
        "user": "username",
        "password": "password",
        "database": "main",
        "port": 5432
    }

    mysql_params = {
        "host": "db_mysql",  # This is the service name defined in docker-compose.yml
        "user": "username",
        "password": "password",
        "port": 3306  # MySQL port as defined in docker-compose.yml
    }

    try:
        # postgres

        # postgres_connection = psycopg2.connect(**postgres_params)
        # postgres_cursor = postgres_connection.cursor()
        # postgres_cursor.execute(sql_command)
        # postgres_cursor.close()

        # mysql
        mysql_connection = mysql.connector.connect(**mysql_params)
        mysql_cursor = mysql_connection.cursor()
        mysql_cursor.execute(sql_command)
        mysql_databases = [row[0] for row in mysql_cursor.fetchall()]
        mysql_cursor.close()
        mysql_connection.close()


        return {"mysql_databases": mysql_databases}
    except Exception as e:
        return {"error": str(e)}

# Call the function to connect and fetch data


@app.get('/')
async def get_root():
    return {
        "message": "Hi"
    }


@app.get('/connect')
async def get_con():
    con = connect_to_mysql_and_fetch_data(sql_command="SHOW DATABASES;")
    return {
        "message": con,
    }


@app.get("/create")
async def create_db():
    con = connect_to_mysql_and_fetch_data(sql_command="CREATE DATABASE main_2")
    return {
        "message": con
    }

@app.get("/users")
async def get_users():
    con = connect_to_mysql_and_fetch_data(sql_command="SELECT * FROM mysql.user")
    return {
        "message": con
    }