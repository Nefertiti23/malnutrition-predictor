import joblib
import pandas as pd

from src.models.train_models import get_dataset, make_features

def test_models_load():
    for name in ['random_forest', 'xgboost', 'lightgbm']:
        model = joblib.load(f"models/{name}.joblib")
        assert model is not None

def test_models_predict():
    model = joblib.load("models/random_forest.joblib")
    df = get_dataset("data/processed/final_dataset.csv")
    X, _ = make_features(df)
    preds = model.predict(X[:10])
    assert len(preds) == 10