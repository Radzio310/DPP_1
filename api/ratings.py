# api/ratings.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession
from typing import List
from pydantic import BaseModel
from api.db import Session as DBSession, Rating as RatingModel

router = APIRouter(tags=["Movies"])

class RatingOut(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

    class Config:
        orm_mode = True

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.get("/ratings", response_model=List[RatingOut])
def get_ratings(db: OrmSession = Depends(get_db)):
    return db.query(RatingModel).all()
