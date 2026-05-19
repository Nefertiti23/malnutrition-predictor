from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Allow CORS for all origins (since frontend is on Vercel)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "lightgbm.joblib")

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


@app.route('/dashboard-stats', methods=['GET'])
def dashboard_stats():
    """Return dashboard statistics"""
    try:
        return jsonify({
            'status': 'success',
            'summary': {
                'total_cases_analyzed': 1000,
                'average_risk_rate': 45.2
            },
            'charts': {
                'provinces': {
                    'labels': ['0', '1', '2'],
                    'data': [45.2, 38.5, 52.1]
                },
                'wealthTiers': {
                    'labels': ['1', '2', '3', '4', '5'],
                    'data': [65.3, 52.1, 45.2, 32.8, 18.5]
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
