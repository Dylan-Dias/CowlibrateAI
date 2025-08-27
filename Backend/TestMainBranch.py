# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import pulp
import os

# ---------- Database Setup ----------
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:root@localhost:5432/CowlibrateAI"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------- Models ----------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class CowEntry(Base):
    __tablename__ = "cow_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    milk_yield = Column(Float, nullable=False)
    health = Column(String)
    breed = Column(String)
    lactation_stage = Column(String)
    age = Column(Float)

    owner = relationship("User")

class Feed(Base):
    __tablename__ = "cow_feeds"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    feed_type = Column(String, nullable=False)
    feed_quantity = Column(Float, nullable=False)
    feed_percentage = Column(Float, nullable=False)

    owner = relationship("User")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# ---------- Pydantic Schemas ----------
class CowEntrySchema(BaseModel):
    id: int
    milk_yield: float
    health: str
    breed: str
    lactation_stage: str
    age: float

    class Config:
        orm_mode = True

class FeedSchema(BaseModel):
    id: int
    feed_type: str
    feed_quantity: float
    feed_percentage: float

    class Config:
        orm_mode = True

class OptimizeResult(BaseModel):
    feed_allocation: Dict[int, Dict[str, float]]  # {cow_id: {feed_type: quantity}}
    total_cost: float

# ---------- FastAPI App ----------
app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Dependencies ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user() -> int:
    """
    Placeholder for authentication.
    Replace this with real auth logic to get the current logged-in user ID.
    """
    return 1

# ---------- Helper: fetch user data ----------
def fetch_user_data(user_id: int, db: Session):
    cows = db.query(CowEntry).filter(CowEntry.user_id == user_id).all()
    feeds = db.query(Feed).filter(Feed.user_id == user_id).all()
    return cows, feeds

# ---------- Optimization Endpoint ----------
@app.post("/api/optimize", response_model=OptimizeResult)
def optimize_cow_feeding(
    input_data: dict,  # <-- receive posted JSON
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    cows, feeds = fetch_user_data(current_user, db)

    if not cows or not feeds:
        return {"feed_allocation": {}, "total_cost": 0.0}

    # LP Problem
    prob = pulp.LpProblem("FeedOptimization", pulp.LpMaximize)

    feed_vars = {
        (cow.id, feed.id): pulp.LpVariable(f"cow{cow.id}_feed{feed.id}", lowBound=0)
        for cow in cows for feed in feeds
    }

    prob += pulp.lpSum(feed_vars[(cow.id, feed.id)] * cow.milk_yield for cow in cows for feed in feeds)

    for feed in feeds:
        prob += pulp.lpSum(feed_vars[(cow.id, feed.id)] for cow in cows) <= feed.feed_quantity

    prob.solve()

    allocation = {
        cow.id: {feed.feed_type: feed_vars[(cow.id, feed.id)].varValue or 0.0 for feed in feeds}
        for cow in cows
    }

    total_cost = sum(allocation[cow.id][feed.feed_type] * feed.feed_percentage for cow in cows for feed in feeds)

    return {"feed_allocation": allocation, "total_cost": total_cost}

