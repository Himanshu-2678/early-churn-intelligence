import pandas as pd
import numpy as np

def add_account_relative_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds account-relative deviation features using past behavior only.
    Leakage-safe: uses shifted rolling statistics.
    """

    df = df.sort_values(["account_id", "snapshot_date"]).copy()

    group = df.groupby("account_id")

    # ---- Usage count deviation ----
    df["usage_mean_prev_6m"] = (
        group["usage_count_last_1m"]
        .rolling(window=6, min_periods=2)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True))

    df["usage_std_prev_6m"] = (
        group["usage_count_last_1m"]
        .rolling(window=6, min_periods=2)
        .std()
        .shift(1)
        .reset_index(level=0, drop=True))

    df["usage_z_1m"] = (
        (df["usage_count_last_1m"] - df["usage_mean_prev_6m"])
        / (df["usage_std_prev_6m"] + 1e-6))

    # ---- Usage duration deviation ----
    df["duration_mean_prev_6m"] = (
        group["usage_duration_last_1m"]
        .rolling(window=6, min_periods=2)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True))

    df["duration_std_prev_6m"] = (
        group["usage_duration_last_1m"]
        .rolling(window=6, min_periods=2)
        .std()
        .shift(1)
        .reset_index(level=0, drop=True))

    df["duration_z_1m"] = (
        (df["usage_duration_last_1m"] - df["duration_mean_prev_6m"])
        / (df["duration_std_prev_6m"] + 1e-6))

    # ---- Active features deviation ----
    df["features_mean_prev_6m"] = (
        group["active_features_last_1m"]
        .rolling(window=6, min_periods=2)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True))

    df["features_z_1m"] = (
        df["active_features_last_1m"] - df["features_mean_prev_6m"])

    return df
