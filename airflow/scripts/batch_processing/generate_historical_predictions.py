import pandas as pd
import pickle
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from shared_modules.transform import ChurnDataTransformer
import yaml

# Load environment 
load_dotenv()

PROJECT_ROOT = "/opt/airflow"

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

# config
config_path = os.path.join(PROJECT_ROOT, 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# load model
model_path = os.path.join(PROJECT_ROOT, config['paths']['churn_model'])
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# get reference data
reference_df = pd.read_sql('SELECT * FROM table1', engine)

# set transformer and transform data
transformer = ChurnDataTransformer()
reference_transformed = transformer.transform(reference_df)

# Model inference to get predictions
reference_transformed['prediction'] = model.predict(reference_transformed)

# Drop existing table to avoid constraint issues
with engine.begin() as conn:
    conn.execute(text('DROP TABLE IF EXISTS table1_historical_predictions CASCADE;'))

# Save predictions for future comparison (data/model drift)
reference_transformed.to_sql('table1_historical_predictions', engine, if_exists='replace', index=False)

print(" Historical predictions table updated successfully.")
