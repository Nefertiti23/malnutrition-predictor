import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
import yaml

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                              recall_score, confusion_matrix,
                              roc_auc_score, classification_report)

with open("configs/model_config.yaml") as f:
    config = yaml.safe_load(f)

def get_dataset(path):
    df = pd.read_csv(path)
    return df


def make_features(df):
    # X = features
    # dropping target column, and columns not required for model training
    X = df.drop(['stunted', 'cluster_id', 'household_id'], axis=1)

    # y = target
    y = df['stunted']

    return X, y


def split_data(X, y):
    # separating training and testing data for both features and target. 
    # 80% of the data is for training the model, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
    return X_train, X_test, y_train, y_test


def train_random_forest(X_train, y_train):
    # create an instance of random forest model
    rf = RandomForestClassifier(**config['random_forest'])
    rf.fit(X_train, y_train)

    return rf

def train_xgboost(X_train, y_train):
    bst = XGBClassifier(**config['xgboost'])
    bst.fit(X_train, y_train)

    return bst

def train_lightgbm(X_train, y_train):
    clf = lgb.LGBMClassifier(**config['lightgbm'])
    clf.fit(X_train, y_train)

    return clf


def train_all_models(X_train, y_train):
    models = {
        'Random Forest' : train_random_forest(X_train, y_train),
        'XGBoost' : train_xgboost(X_train, y_train),
        'LightGBM' : train_lightgbm(X_train, y_train),
    }

    return models

def evaluate_model(model, X_test, y_test, name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    return {
        'Model': name,
        'Accuracy': round(accuracy_score(y_test, y_pred) * 100, 2),
        'F1 Score': round(f1_score(y_test, y_pred) * 100, 2),
        'Precision': round(precision_score(y_test, y_pred) * 100, 2),
        'Recall': round(recall_score(y_test, y_pred) * 100, 2),
        'ROC-AUC': round(roc_auc_score(y_test, y_prob) * 100, 2)
    }

def evaluate_all_models(models, X_test, y_test):
    print("Model Evaluation\n")
    results = []
    for name, model in models.items():
        result = evaluate_model(model, X_test, y_test, name)
        results.append(result)
    
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))


if __name__ == "__main__":
    import joblib

    # Load and prepare data
    df = get_dataset("data/processed/final_dataset_clean.csv")

    X, y = make_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Train
    models = train_all_models(X_train, y_train)

    # Evaluate
    evaluate_all_models(models, X_test, y_test)

     # Save
    for name, model in models.items():
        filename = name.lower().replace(" ", "_")
        joblib.dump(model, f"models/{filename}.joblib")
        print(f"Saved to models/{filename}.joblib")