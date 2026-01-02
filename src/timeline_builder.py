## building user timeline from CSV data
import pandas as pd

def user_timeline(csv_path: str) -> dict:
    
    ## loading the data
    df = pd.read_csv(csv_path)
    timeline = {}

    ## grouping by user_id to create timeline
    for user_id, user_df in df.groupby('user_id'):
        ## sorting by week time
        user_df = user_df.sort_values(by="week") ## it sorts the sessions in the week order

        ## extracting sessions as a list
        timeline[user_id] = user_df["sessions"].tolist()

    return timeline

## Driver Code
if __name__ == "__main__":
    csv_path = "data/raw/user_activity.csv"
    timelines = user_timeline(csv_path)

    ## printing first 3 user timelines
    for i, (user_id, timeline) in enumerate(timelines.items()):
        print(user_id, ":", timeline)
        if i == 2:
            break