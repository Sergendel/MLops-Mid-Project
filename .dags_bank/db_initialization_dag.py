from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'db_initialization_dag',
    description='Explicitly loads CSV into PostgreSQL',
    schedule='@once',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    load_csv_task = BashOperator(
        task_id='load_csv_to_db',
        bash_command='python /opt/airflow/company_db_setup/load_csv_to_db.py',
    )

    load_csv_task
