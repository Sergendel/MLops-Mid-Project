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

transformed_csv_path = '/opt/airflow/company_db_setup/data_files/transformed_output.csv'
transformed_table_name = 'transformed_table1'

df = pd.read_csv(transformed_csv_path)
df.to_sql(transformed_table_name, engine, if_exists='replace', index=False)

print(f"✅ Loaded transformed data into '{transformed_table_name}' table.")
