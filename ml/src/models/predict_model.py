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

    model = load_model("models/xgboost.joblib")
    
#     # df = get_dataset("data/processed/final_dataset.csv")
#     X, _ = make_features(df)

    sample = pd.DataFrame([
        {'child_age_months': 12, 'mother_education': 0, 'wealth_index': 1, 
         'urban_rural': 1, 'province': 0},
        {'child_age_months': 18, 'mother_education': 0, 'wealth_index': 1, 
          'urban_rural': 1, 'province': 0},
        {'child_age_months': 48, 'mother_education': 3, 'wealth_index': 5, 
         'urban_rural': 0, 'province': 1},
        {'child_age_months': 36, 'mother_education': 2, 'wealth_index': 3, 
         'urban_rural': 0, 'province': 2},
        {'child_age_months': 24, 'mother_education': 1, 'wealth_index': 2, 
         'urban_rural': 1, 'province': 1}
])
    preds = predict(model, sample)
    for pred in preds:
        print("Stunted:", bool(pred))
