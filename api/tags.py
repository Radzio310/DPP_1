from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import csv
import os

router = APIRouter()

class Tag(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int  # zmieniłem na int, bo w pliku jest liczba

def read_tags():
    tags = []
    csv_path = os.path.join(os.path.dirname(__file__), "data/tags.csv")
    with open(csv_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["userId"] = int(row["userId"])
            row["movieId"] = int(row["movieId"])
            row["timestamp"] = int(row["timestamp"])
            tags.append(Tag(**row))
    return tags

@router.get("/tags", response_model=List[Tag])
def get_tags():
    return read_tags()