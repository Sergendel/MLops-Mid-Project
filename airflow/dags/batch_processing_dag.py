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

    batch_predict_task.doc_md = """
    ### 📌 **Batch Prediction Task**
    - **Purpose:** Explicitly retrieve data from PostgreSQL, transform it, apply churn prediction model, and persist predictions back.
    - **Tables processed explicitly:** `table1`, `table1_1`, `table1_2`.
    - **Logs:** Detailed info, data shape, previews, and prediction summaries.
    """

    batch_predict_task
