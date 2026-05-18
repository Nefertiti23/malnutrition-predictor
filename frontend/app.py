from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app) 
# Get the absolute path to the model relative to this script
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "lightgbm.joblib")
model = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    try:
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

# Standard terminal execution (No threading needed here!)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)