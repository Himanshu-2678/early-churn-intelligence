import pandas as pd

def add_early_event_flags(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["flag_zero_usage_1m"] = (df["usage_count_last_1m"] == 0).astype(int)

    df["flag_usage_drop_40pct"] = (df["usage_count_last_1m"] < 0.4 * df["usage_count_last_3m"]).astype(int)

    df["flag_feature_collapse"] = (df["active_features_last_1m"] <= 1).astype(int)

    df["flag_error_spike"] = (df["error_count_last_1m"] > 2 * df["error_count_last_3m"]).astype(int)

    df["flag_recent_inactivity"] = ((df["months_since_last_usage"] >= 1) & (df["months_since_first_usage"] <= 3)).astype(int)

    return df
