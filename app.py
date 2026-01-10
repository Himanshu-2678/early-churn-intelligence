from fastapi import FastAPI, Depends

from src.data_loader import synthetic_data
from src.timeline_builder import user_timeline
from src.decay_detector import detect_decay
from src.risk_signal import generate_risk_signal
from src.pipeline import final_result
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models import User, UserEvent

app = FastAPI()

@app.get("/")
async def root():  # what is async: It allows the function to run asynchronously, which means it can handle other tasks while waiting for I/O operations to complete.
    return {"message": "Welcome to the Early Churn Intelligence"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/run")
def run_pipeline(total_users = 70, total_weeks = 12):
    results = final_result(total_users = total_users, total_weeks = total_weeks)

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


@app.post("/test-insert")
def test_func(db: Session = Depends(get_db)):
    user = User(is_active = True)
    db.add(user)
    db.commit()
    db.refresh(user)

    event = UserEvent(user_id = user.id, week = 1, activity_score = 0.85)

    db.add(event)
    db.commit()

    return {"user_id": user.id, "activity_score" : event.activity_score}

