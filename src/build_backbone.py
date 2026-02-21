import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def main():

    # loading raw data
    accounts = pd.read_csv("data/raw/ravenstack_accounts.csv")
    subscriptions = pd.read_csv("data/raw/ravenstack_subscriptions.csv")
    churn = pd.read_csv("data/raw/ravenstack_churn_events.csv")

    
    # parsing dates
    subscriptions["start_date"] = pd.to_datetime(subscriptions["start_date"], dayfirst=True)
    subscriptions["end_date"] = pd.to_datetime(subscriptions["end_date"], dayfirst=True)
    churn["churn_date"] = pd.to_datetime(churn["churn_date"], dayfirst=True)

    
    # Building month range
    global_start = subscriptions["start_date"].min().replace(day=1)
    global_end = churn["churn_date"].max().replace(day=1)

    months = pd.date_range(start=global_start, end=global_end, freq="MS")

    
    # Backbone: account × month
    backbone = (
        pd.MultiIndex.from_product(
            [accounts["account_id"].unique(), months], names=["account_id", "snapshot_month"]).to_frame(index=False))

    
    # Subscription summary
    subscription_summary = (
        subscriptions.groupby("account_id", as_index=False).agg(start_date=("start_date", "min"), end_date=("end_date", "max")))

    backbone = backbone.merge(
        subscription_summary,
        on="account_id",
        how="left",
        validate="many_to_one")

    
    # Keeping active subscription months only
    backbone = backbone[
        (backbone["snapshot_month"] >= backbone["start_date"]) &
        (backbone["end_date"].isna() | (backbone["snapshot_month"] <= backbone["end_date"]))]

    # Merging the churn date
    churn = churn[["account_id", "churn_date"]]
    backbone = backbone.merge(churn, on="account_id", how="left")
    
    # Label creation (2-month churn window)
    backbone["label"] = (
        backbone["churn_date"].notna() &
        (backbone["churn_date"] > backbone["snapshot_month"]) &
        (backbone["churn_date"] <= backbone["snapshot_month"] + pd.DateOffset(months=2))
    ).astype(int)

    # saving the backbone
    backbone.to_csv("data/processed/backbone.csv", index=False)

    print(backbone["label"].value_counts())

if __name__ == "__main__":
    main()
