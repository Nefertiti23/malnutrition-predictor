from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
import pandas as pd

app = Flask(__name__)
# Absolute wild-card CORS registration to accept any dynamic ports (5173 to 5176+)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# 1. Load the ML Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "lightgbm.joblib")
model = joblib.load(MODEL_PATH)

# 2. Load the Cleaned Dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "data", "processed", "final_dataset_clean.csv")
try:
    df = pd.read_csv(DATA_PATH)
    print("SUCCESS: Dataset loaded perfectly from absolute path!")
except Exception as e:
    print(f"Warning: Could not load dataset. Error: {e}")
    df = None


@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    # Handle preflight CORS requests explicitly
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
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


@app.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    if df is None:
        return jsonify({"status": "error", "message": "Dataset file not found."}), 500
        
    try:
        # Match your notebook target stunting column name
        target_col = 'stunted' if 'stunted' in df.columns else df.columns[-1]
        
        # 1. Group Province Safely
        province_stats = {}
        prov_col = 'province' if 'province' in df.columns else None
        if prov_col:
            for k, group in df.groupby(prov_col):
                try:
                    clean_key = str(int(float(k)))
                except Exception:
                    clean_key = str(k)
                province_stats[clean_key] = float(group[target_col].mean())
        
        # 2. Group Wealth Index or House Quality Safely if wealth_index is missing
        wealth_stats = {}
        wealth_col = 'wealth_index' if 'wealth_index' in df.columns else ('housing_quality' if 'housing_quality' in df.columns else None)
        if wealth_col:
            for k, group in df.groupby(wealth_col):
                try:
                    clean_key = str(int(float(k)))
                except Exception:
                    clean_key = str(k)
                wealth_stats[clean_key] = float(group[target_col].mean())
        
        # 3. Aggregations Summary
        total_records = len(df)
        high_risk_percentage = float(df[target_col].mean() * 100) if target_col in df.columns else 0.0

        return jsonify({
            "status": "success",
            "summary": {
                "total_cases_analyzed": total_records,
                "average_risk_rate": round(high_risk_percentage, 2)
            },
            "charts": {
                "provinces": {
                    "labels": list(province_stats.keys()) if province_stats else ["No Data"],
                    "data": [round(val * 100, 2) for val in province_stats.values()] if province_stats else [0]
                },
                "wealthTiers": {
                    "labels": list(wealth_stats.keys()) if wealth_stats else ["No Data"],
                    "data": [round(val * 100, 2) for val in wealth_stats.values()] if wealth_stats else [0]
                }
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)