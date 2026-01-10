from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://churn_user:churn_pass@localhost:5432/churn_db"

engine = create_engine(DATABASE_URL, echo = True) ## echo = True: prints SQL

SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind = engine)

Base = declarative_base()