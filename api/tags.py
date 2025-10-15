# api/tags.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession
from typing import List
from pydantic import BaseModel
from api.db import Session as DBSession, Tag as TagModel

router = APIRouter()

class TagOut(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class Config:
        orm_mode = True

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.get("/tags", response_model=List[TagOut])
def get_tags(db: OrmSession = Depends(get_db)):
    return db.query(TagModel).all()
