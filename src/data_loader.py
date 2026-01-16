## to generate the synthetic data 
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.db.database import engine
import random

def synthetic_data(total_users = 100, total_weeks = 12, seed = 42) -> pd.DataFrame:
    random.seed(seed)
    data = []
    
    for user_id in range(1, total_users + 1):
        user_id = f"{user_id}"

        ## behavior patterns
        behavior_type = random.choice(["stable", "gradual_decline", "sudden_drop"])
        base_activity = random.randint(6, 10)

        for week in range(1, total_weeks + 1):
            if behavior_type == "stable":
                sessions = base_activity + random.randint(-1, 1)
            elif behavior_type == "gradual_decline":
                sessions = base_activity - (week * 0.5) + random.randint(-1, 1)
            else: ## incase of sudden_drop
                if week < total_weeks // 2:
                    sessions = base_activity + random.randint(-1, 1)
                else:
                    sessions = base_activity // 4
            
            sessions = max(0, int(sessions))  
            data.append([user_id, week, sessions])

    df = pd.DataFrame(data, columns=["user_id", "week", "activity_score"])
    return df

# Craeting a function to load data from the DataBase.
def load_activity_from_db():
    try:
        # Try reading from DB
        query = """
        SELECT user_id, week, sessions
        FROM user_events
        ORDER BY user_id, week;
        """
        return pd.read_sql(query, engine)

    except Exception as e:
        print("DB empty or table missing. Generating synthetic data...")

        # Generate synthetic data
        df = synthetic_data()

        # Save it to DB
        df.to_sql(
            "user_events",
            engine,
            if_exists="replace",
            index=False)
        
        return df


## Driver Code
if __name__ == "__main__":
    df = synthetic_data()
    df.to_csv("data\\raw\\user_activity.csv", index=False)
    print("Synthetic data generated and saved to 'data/raw/user_activity.csv'")