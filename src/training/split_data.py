import pandas as pd

def main():
    df = pd.read_csv('data/processed/modeling_table.csv')
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

    cutoff_date = pd.Timestamp("2023-09-30")

    train_df = df[df["snapshot_date"] <= cutoff_date]
    val_df   = df[df["snapshot_date"] > cutoff_date]

    assert train_df["snapshot_date"].max() < val_df["snapshot_date"].min()
    assert train_df.shape[0] > 0
    assert val_df.shape[0] > 0

    train_df.to_csv("data/processed/train.csv", index=False)
    val_df.to_csv("data/processed/val.csv", index=False)

    print("Train / Validation split created")
    print("Train size:", train_df.shape)
    print("Val size:", val_df.shape)

if __name__ == "__main__":
    main()