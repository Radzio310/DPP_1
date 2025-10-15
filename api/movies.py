from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import csv
import os

router = APIRouter()

class Movie(BaseModel):
    movieId: int
    title: str
    genres: str

def read_movies():
    movies = []
    # Ścieżka względna do pliku CSV
    csv_path = os.path.join(os.path.dirname(__file__), "data/movies.csv")
    with open(csv_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Zamiana movieId na int, bo z CSV przychodzi jako string
            row["movieId"] = int(row["movieId"])
            movies.append(Movie(**row))
    return movies

@router.get("/movies", response_model=List[Movie])
def get_movies():
    return read_movies()