import os
import pandas as pd
import pickle
import yaml
from sqlalchemy import create_engine
from dotenv import load_dotenv
from shared_modules.transform import ChurnDataTransformer

#  correct environment handling
RUNNING_LOCALLY = False  # Set  False in Airflow, True locally

if RUNNING_LOCALLY:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    dotenv_path = os.path.join(PROJECT_ROOT, '.env')
    config_path = os.path.join(PROJECT_ROOT, 'config.yaml')
    load_dotenv(dotenv_path)
    POSTGRES_HOST = 'localhost'
else:
    PROJECT_ROOT = "/opt/airflow"
    config_path = os.path.join(PROJECT_ROOT, 'config.yaml')
    load_dotenv()
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

# config
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

# load model
model_path = os.path.join(PROJECT_ROOT, config['paths']['churn_model'])
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)


# set transformer
transformer = ChurnDataTransformer()
input_tables = ['table1', 'table2', 'table3']

# set predictions folder
predictions_csv_dir = os.path.join(PROJECT_ROOT, config['paths']['predictions_csv_dir'])
#predictions_csv_dir = os.path.join(PROJECT_ROOT, 'company_db_setup/data_files/predictions')
os.makedirs(predictions_csv_dir, exist_ok=True)

for table in input_tables:
    print(f"\n🔹 Processing table: '{table}'")

    # load
    df_raw = pd.read_sql_table(table, engine)

    if df_raw.empty:
        print(f"⚠️ Warning: '{table}'  has no data. Skipping prediction.")
        continue
     
    # transform
    df_transformed = transformer.transform(df_raw)

    if df_transformed.empty:
        print(f"⚠️ Warning: '{table}'  became empty after transformation. Skipping prediction.")
        continue

    df_transformed.columns = [str(col) for col in df_transformed.columns]
    model_features = [str(col) for col in model.feature_names_in_]

    missing_cols = set(model_features) - set(df_transformed.columns)
    for col in missing_cols:
        df_transformed[col] = 0

    df_transformed = df_transformed[model_features]
    df_transformed.columns = df_transformed.columns.astype(str)

    # model inference 
    predictions = model.predict(df_transformed)
    df_transformed['prediction'] = predictions

    output_table_name = f"{table}_predictions"
    df_transformed.to_sql(output_table_name, engine, if_exists='replace', index=False)

    # load
    output_csv_path = os.path.join(predictions_csv_dir, f"{table}_predictions.csv")
    df_transformed.to_csv(output_csv_path, index=False)

    print(f" Predictions for '{table}' saved to '{output_table_name}' in PostgreSQL")
    print(f" Predictions for '{table}' saved to '{output_csv_path}' as CSV\n")
