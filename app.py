from fastapi import FastAPI, Depends, HTTPException

from src.timeline_builder import user_timeline
from src.decay_detector import detect_decay
from src.risk_signal import generate_risk_signal
from src.pipeline import final_result
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models import User, UserEvent
from pydantic import BaseModel
from src.db.models import EarlyChurnPrediction

app = FastAPI()

class TrackEventRequest(BaseModel):
    user_id: int
    week: int
    activity_score: float

@app.get("/")
async def root():  # what is async: It allows the function to run asynchronously, which means it can handle other tasks while waiting for I/O operations to complete.
    return {"message": "Welcome to the Early Churn Intelligence"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/run")
def run_pipeline(db: Session = Depends(get_db)):
    results = final_result()

    if not results:
        return {"status" : "completed",
                "user_id": 0,
                "week": 0,
                "activity_score": 0}
    
    for r in results:
        predictions = EarlyChurnPrediction(user_id = r["user_id"], churn_probability = r["decay_score"], risk_level = r["risk_level"], is_decaying = r["is_decaying"])
        db.add(predictions)
    db.commit()
 
    total_user_cnt = len(results)
    high_risk_cnt = sum(1 for r in results if r['risk_level'] == 'high')
    deacaying_user_cnt = sum(1 for r in results if r['is_decaying'])

    results = {
        "status": "completed",
        "total_users": total_user_cnt,
        "high_risk_users": high_risk_cnt,
        "decaying_users": deacaying_user_cnt
    }

    return results


@app.post("/debug/test-insert")
def test_func(db: Session = Depends(get_db)):
    user = User(is_active = True)
    db.add(user)
    db.commit()
    db.refresh(user)

    event = UserEvent(user_id = user.id, week = 1, activity_score = 0.85)

    db.add(event)
    db.commit()

    return {"user_id": user.id, "activity_score" : event.activity_score}


@app.post("/track-event")
def trackEvents(event: TrackEventRequest, db: Session = Depends(get_db)):

    ## checking if the user exists 
    user = db.query(User).filter(User.id == event.user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not present.")
    
    ## creating the track-event
    user_event = UserEvent(user_id = event.user_id, week = event.week, activity_score = event.activity_score)

    db.add(user_event)
    db.commit()

    return {"Status": "Event recorded", "User_ID": event.user_id, "Week": event.week, "Activity_Score": event.activity_score}

