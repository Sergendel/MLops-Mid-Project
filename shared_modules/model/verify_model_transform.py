import os
import pickle
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from shared_modules.transform import ChurnDataTransformer

# Explicitly load environment variables from .env
load_dotenv()

# Explicitly load DB credentials
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')  # Docker default

# Create database connection explicitly
engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

# Explicitly load data directly from PostgreSQL
query = "SELECT * FROM table1 LIMIT 10;"
raw_df = pd.read_sql(query, engine)

# Explicitly transform data
transformer = ChurnDataTransformer()
transformed_df = transformer.transform(raw_df)

# Explicitly load trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'churn_model.pickle')
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

# Explicitly predict using transformed data
prediction = model.predict(transformed_df)

# Explicitly output the transformed data and predictions
print("✅ Explicitly transformed data:")
print(transformed_df)
print("\n✅ Explicit model predictions:", prediction)
