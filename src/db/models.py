from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy import DateTime
from src.db.database import Base

## creating tables
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    signup_date = Column(DateTime, default = datetime.utcnow)
    is_active = Column(Boolean, default = True)


class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week = Column(Integer)
    activity_score = Column(Float)


class EarlyChurnPrediction(Base):
    __tablename__ = "early_churn_prediction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    churn_probability = Column(Float)
    risk_level = Column(String)
    is_decaying = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)