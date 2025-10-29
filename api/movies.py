from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db import Session as DBSession, Movie
from typing import List

router = APIRouter(tags=["Movies"])

# Schemat odpowiedzi (opcjonalnie, dla lepszej dokumentacji)
from pydantic import BaseModel

class MovieOut(BaseModel):
    movieId: int
    title: str
    genres: str

    class Config:
        orm_mode = True

# Dependency do pobierania sesji bazy
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.get("/movies", response_model=List[MovieOut])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()