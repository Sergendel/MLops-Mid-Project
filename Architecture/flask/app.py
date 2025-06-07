# app.py for REST API predictions
from flask import Flask, request, jsonify
from shared_modules.data_preparation import prepare_data
from prediction import make_prediction

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    prepared_data = prepare_data(input_data)
    prediction = make_prediction(prepared_data)
    return jsonify(prediction=prediction)
