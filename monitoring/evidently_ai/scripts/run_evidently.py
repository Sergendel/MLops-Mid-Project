import pandas as pd
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

reference_df = pd.read_sql('SELECT * FROM table1_historical_predictions', engine)
current_df = pd.read_sql('SELECT * FROM table1_predictions', engine)

# Configure  for only Data Drift (no labels required)
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_df, current_data=current_df)

report_path = '/opt/airflow/company_db_setup/data_files/evidently_report.html'
report.save_html(report_path)

print(f"✅ Evidently report  saved at: {report_path}")
