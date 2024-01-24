# Use the @dag decorator, and a dag function instead of using dag = DAG()
# Use the @task decorator on python functions that contain task logic
# Remove all uses of the PythonOperator

import pendulum
import datetime
import logging

from airflow import DAG
from airflow.secrets.metastore import MetastoreBackend
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

from airflow.decorators import dag,task

#from udacity.common import sql_statements
from sql import sql_statements

# TODO: use the @dag decorator and a dag function declaration 
# dag = DAG(
#     'data_quality_legacy',
#     start_date=pendulum.datetime(2018, 1, 1, 0, 0, 0, 0),
#     end_date=pendulum.datetime(2018, 12, 1, 0, 0, 0, 0),
#     schedule_interval='@monthly',
#     max_active_runs=1
# )
@dag(
    start_date=pendulum.datetime(2018, 1, 1, 0, 0, 0, 0),
    end_date=pendulum.datetime(2018, 12, 1, 0, 0, 0, 0),
    schedule_interval='@monthly',
    max_active_runs=1
)
# TODO: use the @task decorator here

def data_quality():
    @task(sla=datetime.timedelta(hours=1))
    def load_trip_data_to_redshift(*args, **kwargs):
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        redshift_hook = PostgresHook("redshift")
        execution_date = kwargs["execution_date"]
        sql_stmt = sql_statements.COPY_MONTHLY_TRIPS_SQL.format(
            aws_connection.login,
            aws_connection.password,
            year=execution_date.year,
            month=execution_date.month
        )
        redshift_hook.run(sql_stmt)

# TODO: use the @task decorator here
    @task(sla=datetime.timedelta(hours=1))
    def load_station_data_to_redshift(*args, **kwargs):
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        redshift_hook = PostgresHook("redshift")
        sql_stmt = sql_statements.COPY_STATIONS_SQL.format(
            aws_connection.login,
            aws_connection.password,
        )
        redshift_hook.run(sql_stmt)

# TODO: use the @task decorator here
    @task(sla=datetime.timedelta(hours=1))
    def check_greater_than_zero(*args, **kwargs):
        table = kwargs["params"]["table"]
        redshift_hook = PostgresHook("redshift")
        records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Data quality check failed. {table} returned no results")
        num_records = records[0][0]
        if num_records < 1:
            raise ValueError(f"Data quality check failed. {table} contained 0 rows")
        logging.info(f"Data quality on table {table} check passed with {records[0][0]} records")

    create_trips_table = PostgresOperator(
        task_id="create_trips_table",
        postgres_conn_id="redshift",
        sql=sql_statements.CREATE_TRIPS_TABLE_SQL
    )
    load_trips_task = load_trip_data_to_redshift()

    # TODO: get rid of this

    check_trips_task = check_greater_than_zero(
        params={
            'table': 'trips',
        }
    )

    create_stations_table = PostgresOperator(
        task_id="create_stations_table",
        postgres_conn_id="redshift",
        sql=sql_statements.CREATE_STATIONS_TABLE_SQL,
    )
    load_station_task = load_station_data_to_redshift()
    # # TODO: get rid of this
    check_stations_task = check_greater_than_zero(
        params={
            'table': 'stations',
        }
    )
# TODO: get rid of this

    create_trips_table >> load_trips_task
    create_stations_table >> load_station_task
    load_station_task >> check_stations_task
    load_trips_task >> check_trips_task
data_quality_dag = data_quality()