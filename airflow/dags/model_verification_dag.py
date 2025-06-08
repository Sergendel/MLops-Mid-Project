from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

with DAG(
    'model_verification_dag',
    description='Explicitly verifies model-transform compatibility',
    schedule_interval='@once',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    wait_for_db_verification = ExternalTaskSensor(
        task_id='wait_for_db_verification',
        external_dag_id='db_verification_dag',
        external_task_id='verify_db_data',
        mode='poke',
        timeout=600,
        poke_interval=10,
    )

    verify_model_task = BashOperator(
        task_id='verify_model_transform',
        bash_command='python /opt/airflow/shared_modules/model/verify_model_transform.py',
    )

    wait_for_db_verification >> verify_model_task
