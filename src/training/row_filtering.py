import pandas as pd

def filter_structurally_stable_rows(df: pd.DataFrame) -> pd.DataFrame:

    flag_cols = [c for c in df.columns if c.startswith("flag_")]

    has_any_flag = df[flag_cols].sum(axis=1) > 0

    keep_mask = ~(
        (df["account_age_days"] > 180) &
        (df["months_since_last_usage"] < 1) &
        (~has_any_flag))

    return df[keep_mask].copy()
