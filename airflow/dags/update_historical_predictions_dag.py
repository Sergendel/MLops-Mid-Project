from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    'update_historical_predictions',
    description='Updates historical predictions for Evidently reference data.',
    schedule ='@weekly',  # or '@monthly', or None for manual-only
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
) as dag:

    update_historical_predictions_task = BashOperator(
        task_id='update_historical_predictions',
        bash_command='PYTHONPATH=/opt/airflow python /opt/airflow/scripts/batch_processing/generate_historical_predictions.py',
    )

update_historical_predictions_task
