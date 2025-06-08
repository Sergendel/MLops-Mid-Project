from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'etl_pipeline',
    description='ETL Pipeline explicitly extracting from PostgreSQL, transforming data, and loading transformed data back',
        schedule='0 12 * * *',  # explicitly daily at 12:00 PM
        start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    extract_task = BashOperator(
        task_id='extract_raw_data',
        bash_command='python /opt/airflow/scripts/raw_etl/extract_raw.py',
    )

    transform_task = BashOperator(
        task_id='transform_data',
        bash_command='PYTHONPATH=/opt/airflow python /opt/airflow/shared_modules/transform.py',
    )

    load_task = BashOperator(
        task_id='load_transformed_data',
        bash_command='python /opt/airflow/scripts/raw_etl/load_transformed_data.py',
    )

    extract_task >> transform_task >> load_task
