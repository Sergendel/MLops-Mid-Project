import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pickle

# Load environment 
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

# Load reference data 
reference_df = pd.read_sql('SELECT * FROM table1', engine)

#  transform data (assuming transform function available)
from shared_modules.transform import ChurnDataTransformer
transformer = ChurnDataTransformer()
reference_transformed = transformer.transform(reference_df)

# Load model 
model_path = '/shared_modules/model/churn_model.pickle'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Make predictions 
reference_transformed['prediction'] = model.predict(reference_transformed)

#  drop table if exists
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS table1_historical_predictions CASCADE;'))
    conn.commit()

# Now  create the table again
reference_transformed.to_sql('table1_historical_predictions', engine, if_exists='replace', index=False)

print(" Historical predictions table  updated successfully.")
