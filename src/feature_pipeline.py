import pandas as pd
from feature_eng.monthly_usage import (build_monthly_usage, attach_account_id, join_with_snapshots, aggregate_usage_features)
from feature_eng.trend_features import add_trend_features
#from src.feature_eng import snapshots

def main():

    snapshots = pd.read_csv("data/processed/snapshots.csv")
    usage = pd.read_csv("data/raw/ravenstack_feature_usage.csv")
    subscriptions = pd.read_csv("data/raw/ravenstack_subscriptions.csv")

    snapshots["snapshot_date"] = pd.to_datetime(snapshots["snapshot_date"])
    snapshots["snapshot_month"] = pd.to_datetime(snapshots["snapshot_month"])

    monthly_usage = build_monthly_usage(usage)
    monthly_usage = attach_account_id(monthly_usage, subscriptions)

    joined = join_with_snapshots(snapshots, monthly_usage)
    usage_features = aggregate_usage_features(joined)

    usage_features = add_trend_features(usage_features)
    usage_features.to_csv("data/processed/usage_features.csv",index=False)

    print("usage_features.csv created")

if __name__ == "__main__":
    main()
