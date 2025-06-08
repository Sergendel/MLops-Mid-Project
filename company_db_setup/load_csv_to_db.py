import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import yaml

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')  # Docker default

# Define DB connection explicitly using credentials from .env
# DB connection explicitly defined
engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with open(os.path.join(PROJECT_ROOT, 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)

input_csv_path = os.path.join(PROJECT_ROOT, config['data_paths']['input_csv'])
table_name = 'table1'

# Explicit drop statement (robust way)
with engine.begin() as connection:
    connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;'))

# Load CSV into DB explicitly
df = pd.read_csv(input_csv_path)
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"✅ Successfully loaded '{input_csv_path}' into table '{table_name}'")




# Define DB connection explicitly using credentials from .env
# engine = create_engine(
#     f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'
# )
# engine = create_engine(
#     f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'
#)
