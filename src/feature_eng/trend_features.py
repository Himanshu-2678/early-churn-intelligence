import pandas as pd
def add_trend_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Usage trend
    out["usage_trend_3m"] = (out["usage_count_last_1m"] - (out["usage_count_last_3m"] - out["usage_count_last_1m"]) / 2)

    out["usage_trend_pct_3m"] = (out["usage_trend_3m"] / (out["usage_count_last_3m"] + 1))

    # Error trend
    out["error_trend_3m"] = (out["error_count_last_1m"] - (out["error_count_last_3m"] - out["error_count_last_1m"]) / 2)

    # Feature breadth trend 
    out["active_features_drop_3m"] = (out["active_features_last_1m"] - out["active_features_last_3m"])

    return out