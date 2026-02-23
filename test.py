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



"""tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
print(tickets.columns)
print(tickets.shape)
print(tickets.head())"""


"""tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")

print(tickets["priority"].value_counts())
print(tickets["satisfaction_score"].describe())
print(tickets["escalation_flag"].value_counts())
"""


"""tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
print(tickets["priority"].value_counts())"""


"""tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
churn = pd.read_csv("data/raw/ravenstack_churn_events.csv")

tickets["submitted_at"] = pd.to_datetime(tickets["submitted_at"])
churn["churn_date"] = pd.to_datetime(churn["churn_date"])

merged = tickets.merge(churn[["account_id", "churn_date"]], on="account_id", how="inner")

print((merged["submitted_at"] <= merged["churn_date"]).mean())
"""



"""tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
churn = pd.read_csv("data/raw/ravenstack_churn_events.csv")

ticket_counts = tickets.groupby("account_id").size().reset_index(name="ticket_count")

churned_accounts = set(churn["account_id"])

ticket_counts["churned"] = ticket_counts["account_id"].isin(churned_accounts)

print(ticket_counts.groupby("churned")["ticket_count"].mean())
"""



"""tickets = pd.read_csv("data/raw/ravenstack_support_tickets.csv")
churn = pd.read_csv("data/raw/ravenstack_churn_events.csv")

tickets["churned"] = tickets["account_id"].isin(set(churn["account_id"]))

# Escalation rate
print("Escalation rate by churn:")
print(tickets.groupby("churned")["escalation_flag"].mean())

# Avg resolution time
print("\nAvg resolution time:")
print(tickets.groupby("churned")["resolution_time_hours"].mean())

# Avg satisfaction
print("\nAvg satisfaction:")
print(tickets.groupby("churned")["satisfaction_score"].mean())

# Urgent proportion
tickets["is_urgent"] = tickets["priority"] == "urgent"
print("\nUrgent proportion:")
print(tickets.groupby("churned")["is_urgent"].mean())"""


"""df = pd.read_csv("data/processed/modeling_table.csv")
print(df["label"].mean())"""



"""subs = pd.read_csv("data/raw/ravenstack_subscriptions.csv")
subs["start_date"] = pd.to_datetime(subs["start_date"], dayfirst=True)
subs["end_date"] = pd.to_datetime(subs["end_date"], dayfirst=True)

subs = subs.sort_values(["account_id", "start_date"])
subs["next_start"] = subs.groupby("account_id")["start_date"].shift(-1)
subs["overlap"] = subs["next_start"] < subs["end_date"]
print("Overlap rate:", subs["overlap"].mean())

subs["gap_days"] = (subs["next_start"] - subs["end_date"]).dt.days
print(subs["gap_days"].describe())

subs["contract_length_days"] = (subs["end_date"] - subs["start_date"]).dt.days
print(subs["contract_length_days"].describe())
"""


"""import pandas as pd
df_pred = pd.read_csv("data/processed/val_predictions.csv")

y_val = df_pred["y_true"]
y_pred_proba = df_pred["y_score"]

df = pd.read_csv("data/processed/modeling_table.csv")
print("Churn rate:", df["label"].mean())

from sklearn.metrics import average_precision_score

pr_auc = average_precision_score(y_val, y_pred_proba)
print("PR-AUC:", pr_auc)"""


import numpy as np

"""# overall churn rate
base_rate = y_val.mean()

# sort by predicted probability
df_eval = pd.DataFrame({
    "y_true": y_val,
    "y_score": y_pred_proba
}).sort_values("y_score", ascending=False)

top_k = int(0.10 * len(df_eval))

top_10 = df_eval.iloc[:top_k]

top_10_rate = top_10["y_true"].mean()

lift_at_10 = top_10_rate / base_rate

print("Base churn rate:", base_rate)
print("Top 10% churn rate:", top_10_rate)
print("Lift@Top10%:", lift_at_10)


df["tenure_months"] = df["account_age_days"] / 30

df["tenure_bucket"] = pd.cut(
    df["tenure_months"],
    bins=[0, 3, 12, 24, 100],
    labels=["0-3m", "3-12m", "1-2y", "2y+"]
)

from sklearn.metrics import roc_auc_score

for segment in df["tenure_bucket"].dropna().unique():
    mask = df["tenure_bucket"] == segment
    roc = roc_auc_score(y_val[mask], y_pred_proba[mask])
    print(segment, "ROC:", roc)

for plan in df["plan_tier"].unique():
    mask = df["plan_tier"] == plan
    roc = roc_auc_score(y_val[mask], y_pred_proba[mask])
    print(plan, "ROC:", roc)"""



# Load your modeling table
"""df = pd.read_csv("data/processed/modeling_table.csv")

# Convert age to months
df["account_age_months"] = df["account_age_days"] / 30

# Keep only churn-positive rows
churn_df = df[df["label"] == 1].copy()

# Keep first churn signal per account
churn_df = churn_df.sort_values("snapshot_date")
churn_df = churn_df.drop_duplicates(subset=["account_id"], keep="first")

# Compute early churn (<= 6 months)
early_mask = churn_df["account_age_months"] <= 6

total_churn = len(churn_df)
early_churn = early_mask.sum()
early_pct = early_churn / total_churn if total_churn > 0 else 0

print("Total churned accounts:", total_churn)
print("Early churn (<=6m):", early_churn)
print("Percentage early churn:", round(early_pct * 100, 2), "%")"""




"""import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

df = pd.read_csv("data/processed/val_with_preds.csv")

# sanity check
assert "pred_proba" in df.columns, "pred_proba column missing"

# early cohort only (<= 6 months)
early_df = df[df["account_age_days"] <= 90].copy()

y_true = early_df["label"]
y_score = early_df["pred_proba"]

roc = roc_auc_score(y_true, y_score)
pr  = average_precision_score(y_true, y_score)

# Lift@Top10%
early_df = early_df.sort_values("pred_proba", ascending=False)
top_k = int(0.10 * len(early_df))

top_10 = early_df.iloc[:top_k]
lift = top_10["label"].mean() / early_df["label"].mean()


print(df.shape)
print(df["pred_proba"].isna().sum())
print(df["label"].mean())


print("Early cohort size:", len(early_df))
print("Early ROC:", round(roc, 4))
print("Early PR-AUC:", round(pr, 4))
print("Early Lift@10%:", round(lift, 4))"""


"""df = pd.read_csv("data/processed/modeling_table.csv")

flag_cols = [c for c in df.columns if c.startswith("flag_")]
print(flag_cols)
print(df[flag_cols].mean())"""



df = pd.read_csv("data/processed/modeling_table.csv")

cols = ["usage_z_1m", "duration_z_1m", "features_z_1m"]
print(df[cols].describe())
print(df[cols].isna().mean())
