from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "lightgbm.joblib")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


# Vercel mounts this file at /api, so routes are "/" not "/predict".
@app.route('/', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500

        data = request.get_json()

        age = float(data['child_age_months'])
        education = float(data['mother_education'])
        wealth = float(data['wealth_index'])
        urban_rural = float(data['urban_rural'])
        province = float(data['province'])

        features = np.array([[age, education, wealth, urban_rural, province]])
        prediction = model.predict(features)[0]

        return jsonify({'prediction': int(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
