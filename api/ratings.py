from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import csv
import os

router = APIRouter()

class Rating(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int  # zmieniłem na int, bo w pliku jest liczba

def read_ratings():
    ratings = []
    csv_path = os.path.join(os.path.dirname(__file__), "data/ratings.csv")
    with open(csv_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["userId"] = int(row["userId"])
            row["movieId"] = int(row["movieId"])
            row["rating"] = float(row["rating"])
            row["timestamp"] = int(row["timestamp"])
            ratings.append(Rating(**row))
    return ratings

@router.get("/ratings", response_model=List[Rating])
def get_ratings():
    return read_ratings()