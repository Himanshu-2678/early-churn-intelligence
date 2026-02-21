import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score

def main():
    # loading data
    train = pd.read_csv("data/processed/train.csv")
    val = pd.read_csv("data/processed/val.csv")

    # restore the date columns
    train['snapshot_date'] = pd.to_datetime(train['snapshot_date'])
    val['snapshot_date'] = pd.to_datetime(val['snapshot_date'])

    target = 'label'

    drop_columns = ["account_id", "snapshot_date", target]

    # feature selection
    features = [col for col in train.columns if col not in drop_columns]

    X_train, y_train = train[features], train[target]
    X_val, y_val = val[features], val[target]

    # One-hot encoding the categorical columns
    X_train = pd.get_dummies(X_train, drop_first=True)
    X_val = pd.get_dummies(X_val, drop_first=True)

    X_val = X_val.reindex(columns=X_train.columns, fill_value=0)


    # defining baseline model pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(max_iter=1000, random_state=42))
        ])

    # training the model
    pipeline.fit(X_train, y_train)
    
    # evaluating the model
    val_probs = pipeline.predict_proba(X_val)[:, 1]

    roc = roc_auc_score(y_val, val_probs)
    pr  = average_precision_score(y_val, val_probs) # pr: precision-recall

    print(f"ROC-AUC: {roc:.4f}")
    print(f"PR-AUC : {pr:.4f}")

if __name__ == "__main__":
    main()
