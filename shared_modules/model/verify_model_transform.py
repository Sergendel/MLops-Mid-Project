import pandas as pd
import os
import pickle
import yaml
from dotenv import load_dotenv
from shared_modules.transform import ChurnDataTransformer



# Explicitly load environment variables
load_dotenv()

# Explicitly define PROJECT_ROOT as two directories up (shared_modules/model → Solution)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load paths explicitly from config.yaml at project root
with open(os.path.join(PROJECT_ROOT, 'config.yaml'), 'r') as file:
    config = yaml.safe_load(file)

# Explicitly define paths
RAW_INPUT_CSV = os.path.join(PROJECT_ROOT, config['data_paths']['input_csv'])
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'churn_model.pickle')



# Explicitly load one row from raw CSV
raw_df = pd.read_csv(RAW_INPUT_CSV).iloc[[0]]  # explicitly first row

# Transform explicitly
transformer = ChurnDataTransformer()
transformed_df = transformer.transform(raw_df)

# Explicitly load trained model
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

# Explicitly perform prediction
prediction = model.predict(transformed_df)

# Explicitly output results
print("✅ Explicitly transformed data:")
print(transformed_df)
print("\n✅ Explicit model prediction:", prediction)
