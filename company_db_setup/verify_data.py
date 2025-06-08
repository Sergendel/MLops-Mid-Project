import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load credentials explicitly from .env
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


# Explicitly verify tables
explicit_tables = ['table1', 'table2', 'table3']

for table in explicit_tables:
    try:
        df = pd.read_sql(f'SELECT * FROM {table} LIMIT 5;', engine)
        print(f"\n✅ Explicitly verifying '{table}':\n", df)
    except Exception as e:
        print(f"❌ Error explicitly verifying '{table}': {e}")
