import pandas as pd

early_days = 90  # for 6 months

def split_lifecycle(df: pd.DataFrame):

    early_df = df[df["account_age_days"] <= early_days].copy()
    mature_df = df[df["account_age_days"] > early_days].copy()

    return early_df, mature_df
