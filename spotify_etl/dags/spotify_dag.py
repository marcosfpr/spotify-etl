from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from spotify_etl.dags.etl import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['rezende.marcos01@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}    

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='My tracked musics ETL process',
    schedule_interval=timedelta(days=1)
)

run_etl = PythonOperator(
    task_id='spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag
)

run_etl