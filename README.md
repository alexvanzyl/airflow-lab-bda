# Airflow Lab

Hands-on lab demonstrating reading from multiple sources and writing to JSON file. 

## Prerequisites

- Docker and Docker Compose
- Python 3.8+

## Getting started
For Linux users to ensure files created in `dags`, `logs` and `plugins` will be created with the right user permission execute the below command at the root of the project:

```shell
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
### 1. Spin up the containers
Docker compose V2:
```shell
docker compose up -d
```
for older versions:
```shell
docker-compose up -d
```

### 2. Create a new database in Postgres
```shell
# Execute psql on the running postgres container.
# When prompt for password use "airflow" (without quotes)
docker compose exec postgres psql -U airflow -W

# Once in the psql shell create the database
airflow=# CREATE DATABASE airflow_lab_db;

# You can confirm the DB was created with the below command
airflow=#\l

                                  List of databases
      Name      |  Owner  | Encoding |  Collate   |   Ctype    |  Access privileges  
----------------+---------+----------+------------+------------+---------------------
 airflow        | airflow | UTF8     | en_US.utf8 | en_US.utf8 | 
 airflow_lab_db | airflow | UTF8     | en_US.utf8 | en_US.utf8 | 

# Finally quit out of the shell
airflow=#\q
```

### 3. Create new Postgres connection

- From the Airflow UI [http://localhost:8080/](http://localhost:8080/) Goto `Admin > Connections`
- Click on the "+" (Add new record) button
- Fill in the connection details:
    - Connection Id: `postgres_conn`
    - Connection Type: `Postgres`
    - Host: `postgres`
    - Schema: `airflow_lab_db`
    - Login: `airflow`
    - Password: `airflow`
    - Port: `5432`
    - Extra: `{"cursor": "realdictcursor"}` Reference: [here](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/hooks/postgres/index.html#airflow.providers.postgres.hooks.postgres.CursorType)
- Finally save the connection.

### 4. Seed the database with users
- From the Airflow UI [http://localhost:8080/](http://localhost:8080/) Goto `DAGS`
- Run the `seed_postgres_db_dag` dag; this can be done directly from the table by pressing the play button under "Actions"
- Once done you can pause it if you want