from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import csv
import os

router = APIRouter()

class Link(BaseModel):
    movieId: int
    imdbId: str
    tmdbId: str

def read_links():
    links = []
    # Ścieżka względna do pliku CSV
    csv_path = os.path.join(os.path.dirname(__file__), "data/links.csv")
    with open(csv_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Zamiana movieId na int, bo z CSV przychodzi jako string
            row["movieId"] = int(row["movieId"])
            links.append(Link(**row))
    return links

@router.get("/links", response_model=List[Link])
def get_links():
    return read_links()