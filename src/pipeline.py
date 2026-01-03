import pandas as pd

from src.data_loader import synthetic_data
from src.timeline_builder import user_timeline
from src.decay_detector import detect_decay
from src.risk_signal import generate_risk_signal
    
def final_result():

    ## Step 1: Generate Synthetic Data
    df = synthetic_data(total_users=70, total_weeks=12)
    df.to_csv("data/raw/user_activity.csv", index=False)

    ## Step 2: Build User Timelines
    timelines = user_timeline("data/raw/user_activity.csv")

    ## Step 3 and 4: Detect Decay and Generate Risk Signals
    results = []

    for user_id, timeline in timelines.items():
        decay_info = detect_decay(timeline)
        risk_info = generate_risk_signal(decay_info)

        results.append({
            "user_id": user_id,
            "past_avg": decay_info["past_avg"],
            "recent_avg": decay_info["recent_avg"],
            "decay_score": decay_info["decay_score"],
            "is_decaying": decay_info["is_decaying"],
            "risk_level": risk_info["risk_level"]
        })

    results_df = pd.DataFrame(results)
    return results_df


## Driver Code
if __name__ == "__main__":
    final_result()
