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
    df = get_dataset("data/processed/final_dataset.csv")
    X, _ = make_features(df)
    preds = predict(model, X)
    print(preds)