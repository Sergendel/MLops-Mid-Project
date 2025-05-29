from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline to process data and make predictions',
    schedule_interval='0 12 * * *',  # Every day at 12:00 PM
    catchup=False,
    tags=['etl', 'batch', 'mlops'],
) as dag:

    run_etl_pipeline = BashOperator(
        task_id='run_etl_pipeline',
        bash_command='python /path/to/your/scripts/etl_runner.py',
    )

    run_etl_pipeline
