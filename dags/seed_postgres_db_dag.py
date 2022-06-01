from datetime import datetime

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(start_date=datetime(2022, 1, 1), schedule_interval="@once", catchup=False)
def seed_postgres_db_dag():
    create_users_table = PostgresOperator(
        task_id="create_users_table",
        postgres_conn_id="postgres_conn",
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
            """,
    )

    seed_users_table = PostgresOperator(
        task_id="seed_users_table",
        postgres_conn_id="postgres_conn",
        sql="""
            TRUNCATE users;
            INSERT INTO users (firstname, lastname, country, username, password, email)
            VALUES ('Juho', 'Lampo', 'Finland', 'whitetiger106', 'drifter', 'juho.lampo@example.com');
            INSERT INTO users (firstname, lastname, country, username, password, email)
            VALUES ('Tristan', 'Clark', 'Canada', 'bluekoala535', 'deadly', 'tristan.clark@example.com');
            INSERT INTO users (firstname, lastname, country, username, password, email)
            VALUES ('Angie', 'Swiers', 'Netherlands', 'purplebear463', 'surfer1', 'angie.swiers@example.com');
            """,
    )

    create_users_table >> seed_users_table


dag = seed_postgres_db_dag()
