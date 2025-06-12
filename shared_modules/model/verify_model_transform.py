import os
import pickle
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from shared_modules.transform import ChurnDataTransformer

# load environment variables from .env
load_dotenv()

# load DB credentials
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')  # Docker default

# Create database connection 
engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

#  Load data directly from PostgreSQL
query = "SELECT * FROM table1 LIMIT 10;"
raw_df = pd.read_sql(query, engine)

#  Transform data
transformer = ChurnDataTransformer()
transformed_df = transformer.transform(raw_df)

# Load trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'churn_model.pickle')
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

# Predict using transformed data
prediction = model.predict(transformed_df)

# Output the transformed data and predictions
print("  Transformed data:")
print(transformed_df)
print("\n Model predictions:", prediction)
