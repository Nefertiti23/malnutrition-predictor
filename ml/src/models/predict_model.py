import joblib
import pandas as pd

def load_model(model_path):
    return joblib.load(model_path)

def predict(model, X):
    return model.predict(X)

def predict_proba(model, X):
    return model.predict_proba(X)[:, 1]

if __name__ == "__main__":
    from train_models import get_dataset, make_features

    model = load_model("models/random_forest.joblib")
    
#     # df = get_dataset("data/processed/final_dataset.csv")
#     X, _ = make_features(df)

    sample = pd.DataFrame([{
        'child_age_months': 53.0,
        'child_sex': 0,
        'breastfeeding': 2.0,
        'haz_score': -5.66,
        'waz_score': -4.71,
        'whz_score': -2.71,
        'underweight': 0,
        'wasted': 0,
        'mother_education': 1.0,
        'urban_rural': 0,
        'district': 5.0,
        'wealth_index': 1.0,
        'disability': 0.0,
        'province': 2,
        'birth_weight_known':0,
        'housing_quality': 2.0,
        'water_source': 31.0,
        'sanitation_type': 1.0,
        'education_level': 0.0,
        'household_education': 0.0,
    }])
    preds = predict(model, sample)
    print("Stunted:", bool(preds[0]))
