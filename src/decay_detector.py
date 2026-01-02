# detecting behavioral decay in user activity 

def detect_decay(timeline) -> dict:
    """
    Detect behavioral decay from a user's activity timeline.

    Returns:
        dict with:
        - past_avg
        - recent_avg
        - decay_score (0 to 1)
        - is_decaying (bool)
        
    """

    if len(timeline) < 4: # because we need atleast 4 weeks to compare 2 for past and 2 for recent
        return {
            "past_avg": None,
            "recent_avg": None,
            "decay_score": 0.0,
            "is_decaying": False}
        
    
    ## splitting the timeline into past and recent
    mid = len(timeline) // 2
    past_period = timeline[:mid]
    recent_period = timeline[mid:]

    past_avg = sum(past_period) / len(past_period)
    recent_avg = sum(recent_period) / len(recent_period)

    if past_avg == 0:
        decay_score = 0.0
    else:
        decay_score = max(0.0, (past_avg - recent_avg) / past_avg) 
    
    if decay_score > 0.3:
        is_decaying = True
    else:
        is_decaying = False

    return {"past_avg": round(past_avg, 2), 
            "recent_avg": round(recent_avg, 2), 
            "decay_score": round(decay_score, 2), 
            "is_decaying": is_decaying}
            
    
## Driver Code
if __name__ == "__main__":
    sample_timeline = [10, 9, 8, 7, 5, 3, 2, 1]
    res = detect_decay(sample_timeline)
    print("Decay Detection Result:", res)