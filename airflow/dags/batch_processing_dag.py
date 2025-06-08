from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_batch_processing',
    description='Daily batch processing pipeline: extracts data from DB, applies transformations, predicts churn, and stores results explicitly.',
    schedule ='0 12 * * *',  # daily at 12:00 PM explicitly
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
) as dag:

    batch_predict_task = BashOperator(
        task_id='batch_predict',
        bash_command='PYTHONPATH=/opt/airflow python /opt/airflow/scripts/batch_processing/batch_predict.py',
    )

    evidently_monitor_task = BashOperator(
        task_id='run_evidently_monitoring',
        bash_command='PYTHONPATH=/opt/airflow python /opt/airflow/monitoring/evidently_ai/scripts/run_evidently.py',
    )

    batch_predict_task >> evidently_monitor_task
