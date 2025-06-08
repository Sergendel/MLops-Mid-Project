import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml

# Load environment variables explicitly from .env
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# Define DB connection explicitly using credentials from .env
# engine = create_engine(
#     f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'
# )
engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'
)


# Determine explicit project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load relative paths explicitly from YAML config
with open(os.path.join(PROJECT_ROOT, 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)

# CSV folder explicitly defined from config
input_csv_path = os.path.join(PROJECT_ROOT, config['data_paths']['input_csv'])

# Explicitly loading CSV file into DB
csv_file = os.path.basename(input_csv_path)
table_name = 'table1'  # Adjust explicitly if needed

df = pd.read_csv(input_csv_path)
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"✅ Loaded '{csv_file}' into table '{table_name}'")
