# generating Risk Signal 

def generate_risk_signal(decay_info: dict) -> str:
    
    decay_score = decay_info.get("decay_score", 0.0)

    if decay_score >= 0.6:
        risk_level = "HIGH"
    elif decay_score >= 0.3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {"risk_level" : risk_level, "decay_score" : decay_score}

## Driver Code
if __name__ == "__main__":
    examples = [
        {"decay_score": 0.75},
        {"decay_score": 0.45},
        {"decay_score": 0.10}]
    

    for e in examples:
        print(e, ":", generate_risk_signal(e))