from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'load_and_verify_csv_data_to_company_db',
    description='Loads CSV, verifies DB data, and tests model compatibility',
    schedule='@once',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

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

    load_csv_task >> verify_db_task >> verify_model_task
