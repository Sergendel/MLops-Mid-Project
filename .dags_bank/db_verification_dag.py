from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

with DAG(
    'db_verification_dag',
    description='Explicitly verifies database contents after initialization',
    schedule='@once',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    wait_for_db_init = ExternalTaskSensor(
        task_id='wait_for_db_initialization',
        external_dag_id='db_initialization_dag',
        external_task_id='load_csv_to_db',
        mode='poke',
        timeout=600,
        poke_interval=10,
    )

    verify_db_task = BashOperator(
        task_id='verify_db_data',
        bash_command='python /opt/airflow/company_db_setup/verify_data.py',
    )

    wait_for_db_init >> verify_db_task

