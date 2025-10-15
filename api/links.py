# api/links.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as OrmSession
from typing import List, Optional
from pydantic import BaseModel
from api.db import Session as DBSession, Link as LinkModel

router = APIRouter()

class LinkOut(BaseModel):
    movieId: int
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None

    class Config:
        orm_mode = True

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.get("/links", response_model=List[LinkOut])
def get_links(db: OrmSession = Depends(get_db)):
    return db.query(LinkModel).all()
