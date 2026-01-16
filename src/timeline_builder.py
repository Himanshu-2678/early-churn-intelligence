## building user timeline from DB-loaded DataFrame
import pandas as pd

def user_timeline(df: pd.DataFrame) -> dict:

    timelines = {}

    # group by user_id to create timelines
    for user_id, user_df in df.groupby("user_id"):

        # sort events by week
        user_df = user_df.sort_values(by="week")

        # extract activity scores as a list
        timelines[user_id] = user_df["activity_score"].tolist()

    return timelines


## Driver Code (optional test)
if __name__ == "__main__":
    # temporary test with dummy data
    data = {
        "user_id": [1, 1, 1, 2, 2],
        "week": [1, 2, 3, 1, 2],
        "activity_score": [0.9, 0.7, 0.4, 0.8, 0.6]}

    df = pd.DataFrame(data)
    timelines = user_timeline(df)

    for user_id, timeline in timelines.items():
        print(user_id, ":", timeline)
