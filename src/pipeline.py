import pandas as pd

from src.data_loader import load_activity_from_db
from src.timeline_builder import user_timeline
from src.decay_detector import detect_decay
from src.risk_signal import generate_risk_signal

def final_result():

    ## Step 1: Load data from DB
    df = load_activity_from_db()

    ## Step 2: Build timelines from DataFrame
    timelines = user_timeline(df)

    ## Step 3 & 4: Detect decay and generate risk
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

    return results


## Driver Code
if __name__ == "__main__":
    final_result()
