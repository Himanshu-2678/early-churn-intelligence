import pandas as pd

def build_monthly_usage(usage_df: pd.DataFrame) -> pd.DataFrame:
    df = usage_df.copy()
    df["usage_date"] = pd.to_datetime(df["usage_date"], format="%Y-%m-%d")

    # Month bucket
    df["usage_month"] = (df["usage_date"].dt.to_period("M").dt.to_timestamp())

    monthly = (df.groupby(["subscription_id", "usage_month", "feature_name"],as_index=False).agg(
            total_usage_count=("usage_count", "sum"),
            total_duration_secs=("usage_duration_secs", "sum"),
            total_error_count=("error_count", "sum")))

    return monthly


def attach_account_id(monthly_usage: pd.DataFrame, subscriptions: pd.DataFrame) -> pd.DataFrame:

    subs = subscriptions[["subscription_id", "account_id"]]

    return monthly_usage.merge(subs, on="subscription_id", how="left", validate="many_to_one")


def join_with_snapshots(snapshots: pd.DataFrame, monthly_usage: pd.DataFrame) -> pd.DataFrame:

    df = snapshots.merge(monthly_usage, on="account_id", how="left")

    # removing the future usage (leakage guard)
    df = df[df["usage_month"] <= df["snapshot_date"]]

    df["months_ago"] = (df["snapshot_date"].dt.to_period("M") - df["usage_month"].dt.to_period("M")).apply(lambda x: x.n)

    return df


def aggregate_usage_features(df: pd.DataFrame) -> pd.DataFrame:

    features = []

    for window in [1, 3, 6]:
        tmp = (df[df["months_ago"] < window].groupby(["account_id", "snapshot_date"], as_index=False).agg(
                usage_count=("total_usage_count", "sum"),
                usage_duration_secs=("total_duration_secs", "sum"),
                error_count=("total_error_count", "sum"),
                active_features=("feature_name", "nunique")))

        tmp = tmp.rename(columns={
            "usage_count": f"usage_count_last_{window}m",
            "usage_duration_secs": f"usage_duration_last_{window}m",
            "error_count": f"error_count_last_{window}m",
            "active_features": f"active_features_last_{window}m"})

        features.append(tmp)

    final = features[0]
    for f in features[1:]:
        final = final.merge(f, on=["account_id", "snapshot_date"], how="left")

    return final.fillna(0)
