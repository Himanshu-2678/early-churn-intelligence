# This file I maintain to test the data and features at various stages of the pipeline.

import pandas as pd

"""usage = pd.read_csv("data/raw/ravenstack_feature_usage.csv")
print(usage.columns.tolist())"""


"""
df = pd.read_csv("data/processed/usage_features.csv")
print(df.head())
print(df.isna().sum().sort_values(ascending=False).head())
print((df.filter(like="_last_").values >= 0).all())
"""


"""df = pd.read_csv("data/processed/usage_features.csv")

assert "usage_trend_3m" in df.columns
assert "usage_trend_pct_3m" in df.columns

print(df[
    ["usage_count_last_1m", "usage_count_last_3m", "usage_trend_3m"]
].head())
"""

"""snapshots = pd.read_csv("data/processed/snapshots.csv")
snapshots["snapshot_date"] = pd.to_datetime(snapshots["snapshot_date"])

dupes = (
    snapshots
    .groupby(["account_id", "snapshot_date"])
    .size()
    .reset_index(name="cnt")
)

print(dupes[dupes["cnt"] > 1].head())"""


"""accounts = pd.read_csv("data/raw/ravenstack_accounts.csv")
print(accounts.columns.tolist())"""


"""df = pd.read_csv("data/processed/modeling_table.csv")

print(df["months_since_last_usage"].describe())
print(df["months_since_last_usage"].value_counts().head(10))"""


"""df = pd.read_csv("data/processed/modeling_table.csv")
print(df.groupby("label")["months_since_last_usage"].mean())
"""



"""accounts = pd.read_csv("data/raw/ravenstack_accounts.csv")
print(accounts.dtypes)
print(accounts["plan_tier"].unique())
print(accounts["industry"].unique()[:10])
print(accounts["country"].unique()[:10])"""


"""df = pd.read_csv("data/processed/modeling_table.csv")
print(df.columns)"""


"""churn = pd.read_csv("data/raw/ravenstack_churn_events.csv")

print(churn.head())
print(churn.columns)
print(churn.shape)"""


"""subs = pd.read_csv("data/raw/ravenstack_subscriptions.csv")

print(subs.shape)
print(subs["account_id"].nunique())
print(subs.groupby("account_id").size().describe())
print(subs.columns)
"""



"""subs = pd.read_csv("data/raw/ravenstack_subscriptions.csv")
churn = pd.read_csv("data/raw/ravenstack_churn_events.csv")

subs["start_date"] = pd.to_datetime(subs["start_date"], dayfirst=True)
subs["end_date"] = pd.to_datetime(subs["end_date"], dayfirst=True)

churn["churn_date"] = pd.to_datetime(churn["churn_date"])

merged = churn.merge(subs, on="account_id", how="left")

# flag if churn_date matches any end_date per account
match_per_account = (
    merged.groupby("account_id")
    .apply(lambda x: (x["churn_date"] == x["end_date"]).any()))

print("Match rate across churned accounts:", match_per_account.mean())
"""



tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
print(tickets.columns)
print(tickets.shape)
print(tickets.head())
