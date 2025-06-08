import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

raw_table_name = 'table1'  # Adjust table name explicitly if needed
output_csv_path = '/opt/airflow/company_db_setup/data_files/raw_data_extracted.csv'

df = pd.read_sql_table(raw_table_name, engine)
df.to_csv(output_csv_path, index=False)

print(f"✅ Extracted raw data from '{raw_table_name}' to '{output_csv_path}'")
