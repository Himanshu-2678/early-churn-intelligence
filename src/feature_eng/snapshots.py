import pandas as pd

def build_snapshots(backbone: pd.DataFrame) -> pd.DataFrame:

    df = backbone.copy()
    df["snapshot_month"] = pd.to_datetime(df["snapshot_month"])

    df["snapshot_date"] = df["snapshot_month"] + pd.offsets.MonthEnd(0)

    # Removes snapshots after churn
    df = df[
        df["churn_date"].isna() |
        (df["snapshot_date"] < df["churn_date"])]

    return df[["account_id", "snapshot_month", "snapshot_date", "label"]]
