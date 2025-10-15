# api/main_api.py
from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI

from .movies import router as movies_router
from .links import router as links_router
from .ratings import router as ratings_router
from .tags import router as tags_router

# Importy z db.py (ta sama sesja/ta sama baza!)
from .db import Session, Movie, seed_from_csvs, is_movies_table_empty

app = FastAPI(title="Movies API", version="1.0.0")

app.include_router(movies_router)
app.include_router(links_router)
app.include_router(ratings_router)
app.include_router(tags_router)


@app.on_event("startup")
def startup_seed_if_empty() -> None:
    """
    Przy starcie aplikacji: jeżeli tabela `movies` jest pusta,
    wczytaj CSV z katalogu `api/data/`.
    Dzięki temu /movies nie zwróci pustej listy, gdy baza była świeża.
    """
    # Katalog z danymi obok tego pliku: api/data/*.csv
    data_dir = Path(__file__).resolve().parent / "data"

    with Session() as s:
        if is_movies_table_empty(s):
            if not data_dir.exists():
                # Celowo nie crashujemy aplikacji — tylko log do konsoli
                print(f"[WARN] Brak katalogu danych: {data_dir} — baza pozostanie pusta.")
                return
            print(f"[INFO] Seed bazy z CSV w {data_dir}...")
            seed_from_csvs(s, data_dir)
            count = s.query(Movie).count()
            print(f"[OK] Załadowano dane. Liczba filmów: {count}")


@app.get("/")
def read_root():
    return {"hello": "world"}
