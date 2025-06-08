import pandas as pd
import pickle
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from shared_modules.transform import ChurnDataTransformer

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

model_path = os.path.join(PROJECT_ROOT, 'shared_modules/model/churn_model.pickle')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

reference_df = pd.read_sql('SELECT * FROM table1', engine)

transformer = ChurnDataTransformer()
reference_transformed = transformer.transform(reference_df)

# Predict  (no target labels)
reference_transformed['prediction'] = model.predict(reference_transformed)

#  drop existing table to avoid constraint issues
with engine.begin() as conn:
    conn.execute(text('DROP TABLE IF EXISTS table1_historical_predictions CASCADE;'))

# Save predictions 
reference_transformed.to_sql('table1_historical_predictions', engine, if_exists='replace', index=False)

print(" Historical predictions table  updated successfully.")
