import pandas as pd

# adding lifecycle features to the modeling table. 
def add_lifecycle_features(df):

    accounts = pd.read_csv("data/raw/ravenstack_accounts.csv")
    usage = pd.read_csv("data/raw/ravenstack_feature_usage.csv")

    subscriptions = pd.read_csv("data/raw/ravenstack_subscriptions.csv")
    usage = usage.merge(subscriptions[["subscription_id", "account_id"]],
                        on="subscription_id", how="left")
    # Parse dates
    accounts["signup_date"] = pd.to_datetime(accounts["signup_date"])
    usage["usage_date"] = pd.to_datetime(usage["usage_date"])

    # Account age (days)
    df = df.merge(accounts[["account_id", "signup_date"]], on="account_id", how="left")

    df["account_age_days"] = (
        df["snapshot_date"] - df["signup_date"]).dt.days.clip(lower=0)

    # First & last usage dates

    usage_dates = (usage.groupby("account_id").agg(first_usage_date=("usage_date", "min"),last_usage_date=("usage_date", "max")).reset_index())

    df = df.merge(
        usage_dates,
        on="account_id",
        how="left")

    # Months since first / last usage
    df["months_since_first_usage"] = (
        (df["snapshot_date"] - df["first_usage_date"])
        .dt.days / 30).clip(lower=0)

    df["months_since_last_usage"] = (
        (df["snapshot_date"] - df["last_usage_date"])
        .dt.days / 30).clip(lower=0)

    # Avg monthly usage (6m)
    df["avg_monthly_usage_6m"] = (
        df["usage_count_last_6m"] / 6)

    df = df.drop(columns=["signup_date", "first_usage_date", "last_usage_date"])

    return df

# main function to assemble the final modeling table with features + labels.
def main():

    features = pd.read_csv("data/processed/usage_features.csv")
    snapshots = pd.read_csv("data/processed/snapshots.csv")

    # Restore datetime
    features["snapshot_date"] = pd.to_datetime(features["snapshot_date"])
    snapshots["snapshot_date"] = pd.to_datetime(snapshots["snapshot_date"])

    labels = (snapshots.groupby(["account_id", "snapshot_date"], as_index=False).agg(label=("label", "max")))

    # Merge features + labels
    modeling_table = features.merge(labels, on=["account_id", "snapshot_date"], how="left", validate="one_to_one")

    assert modeling_table["label"].notna().all(), "Missing labels after merge"
    modeling_table = add_lifecycle_features(modeling_table)

    # adding account layer to the modeling table.
    accounts = pd.read_csv("data/raw/ravenstack_accounts.csv")

    accounts_subset = accounts[["account_id", "plan_tier", "industry", "country", "seats", "is_trial"]]

    modeling_table = modeling_table.merge(
        accounts_subset,
        on="account_id",
        how="left")
    
    modeling_table.to_csv("data/processed/modeling_table.csv", index=False)

    print("modeling_table.csv created")

if __name__ == "__main__":
    main()




