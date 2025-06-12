import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# config
with open(os.path.join(PROJECT_ROOT, 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)

csv_tables = {
    'database_input.csv': 'table1',
    'database_input2.csv': 'table2',
    'database_input3.csv': 'table3'
}

for csv_file, table_name in csv_tables.items():
    # csv_path = os.path.join(PROJECT_ROOT, 'company_db_setup', 'data_files', 'raw_data', csv_file)
    csv_path = os.path.join(PROJECT_ROOT, config['paths']['raw_data_dir'], csv_file)
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅ Loaded '{csv_file}' into '{table_name}'")
