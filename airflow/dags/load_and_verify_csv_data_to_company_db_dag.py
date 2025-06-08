from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'load_and_verify_csv_data_to_company_db',
    description='Loads CSV, verifies DB data, and tests model compatibility',
    schedule='0 12 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
) as dag:

    #  Wait 5 seconds for PostgreSQL readiness
    wait_for_postgres = TimeDeltaSensor(
        task_id='wait_for_postgres_initialization',
        delta=timedelta(seconds=5),
        mode='reschedule'
    )

    load_csv_task = BashOperator(
        task_id='load_csv_to_db',
        bash_command='python /opt/airflow/company_db_setup/load_csv_to_db.py',
    )

    verify_db_task = BashOperator(
        task_id='verify_db_data',
        bash_command='python /opt/airflow/company_db_setup/verify_data.py',
    )

    verify_model_task = BashOperator(
        task_id='verify_model_transform',
        bash_command=(
            'PYTHONPATH=/opt/airflow python /opt/airflow/shared_modules/model/verify_model_transform.py'
        ),
    )

    # Define task sequence
    wait_for_postgres >> load_csv_task >> verify_db_task >> verify_model_task
