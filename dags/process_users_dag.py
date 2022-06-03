from datetime import datetime
from operator import imod
from pathlib import Path

import pandas as pd
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

FILES_BASE_PATH = "/opt/airflow/files"
USERS_CSV_FILENAME = "users.csv"
USERS_JSON_FILENAME = Variable.get("users_json_filename")  # user.json


def _get_users_from_postgres():
    pg_hook = PostgresHook(postgres_conn_id="postgres_conn")
    pg_conn = pg_hook.get_conn()
    cursor = pg_conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    return users


@dag(start_date=datetime(2022, 1, 1), schedule_interval="@daily", catchup=False)
def process_users_dag():
    @task
    def get_users_from_csv():
        path_to_csv = f"{FILES_BASE_PATH}/{USERS_CSV_FILENAME}"
        if not Path(path_to_csv).is_file():
            raise ValueError(f"{USERS_CSV_FILENAME} file is missing.")

        df = pd.read_csv(path_to_csv)
        return df.to_dict(orient="record")

    get_users_from_postgres = PythonOperator(
        task_id="get_users_from_postgres", python_callable=_get_users_from_postgres
    )

    @task
    def create_users_json_file(ti=None):
        user_lists = ti.xcom_pull(
            task_ids=["get_users_from_csv", "get_users_from_postgres"]
        )
        # Flatten list of lists
        users = [user for users_list in user_lists for user in users_list]
        df = pd.DataFrame(users)
        df.to_json(f"{FILES_BASE_PATH}/{USERS_JSON_FILENAME}", orient="records")

    [get_users_from_csv(), get_users_from_postgres] >> create_users_json_file()


dag = process_users_dag()
