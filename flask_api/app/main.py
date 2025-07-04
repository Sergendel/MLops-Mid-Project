from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import pandas as pd
import pickle
from shared_modules.transform import ChurnDataTransformer
from sqlalchemy import create_engine

# Load environment variables 
load_dotenv()

# Flask app initialization 
app = Flask(__name__)

# Database connection setup 
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
)

# Load trained model from shared modules
MODEL_PATH = '/app/shared_modules/model/churn_model.pickle'

with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

# Data transformer initialization 
transformer = ChurnDataTransformer()

# Health check endpoint 
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# Prediction endpoint 
@app.route('/predict', methods=['POST'])
def predict():
    #  handle JSON input data
    input_data = request.get_json()

    if input_data is None:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Convert JSON  to DataFrame
        input_df = pd.DataFrame([input_data])

        # Transform data 
        transformed_df = transformer.transform(input_df)

        # Ensure feature order  matches trained model
        model_features = model.feature_names_in_
        transformed_df = transformed_df[model_features]

        # Perform prediction 
        prediction = model.predict(transformed_df)

        # Return prediction  as JSON
        return jsonify({"prediction": prediction.tolist()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run  when called directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
