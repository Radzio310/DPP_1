# api/main_api.py
from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from .movies import router as movies_router
from .links import router as links_router
from .ratings import router as ratings_router
from .tags import router as tags_router
from .users import router as users_router
from jwt.router import router as jwt_router

from jwt.deps import get_current_user, require_roles

# Importy z db.py (ta sama sesja/ta sama baza!)
from .db import Session, Movie, seed_from_csvs, is_movies_table_empty, is_users_table_empty, load_users

load_dotenv()  # wczytaj .env na starcie procesu
app = FastAPI(title="Movies and Users API", version="1.0.0")

auth_dep = Depends(get_current_user)  # globalna zależność auth

# chronione routery domenowe
app.include_router(movies_router, dependencies=[auth_dep])
app.include_router(links_router, dependencies=[auth_dep])
app.include_router(ratings_router, dependencies=[auth_dep])
app.include_router(tags_router, dependencies=[auth_dep])
app.include_router(users_router)
app.include_router(jwt_router)


@app.get("/secure/ping")
def secure_ping(user = Depends(get_current_user)):
    return {"ok": True, "sub": user.sub, "roles": user.roles}


@app.post("/admin/reindex", dependencies=[Depends(require_roles("ROLE_ADMIN"))])
def admin_reindex():
    return {"status": "started"}


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
        # seed users z pliku api/data/users.csv (jeśli tabela pusta)
        users_csv = data_dir / "users.csv"
        if is_users_table_empty(s) and users_csv.exists():
            print(f"[INFO] Seed users z {users_csv}...")
            load_users(s, users_csv)
        if is_movies_table_empty(s):
            if not data_dir.exists():
                # Celowo nie crash aplikacji — tylko log do konsoli
                print(f"[WARN] Brak katalogu danych: {data_dir} — baza pozostanie pusta.")
                return
            print(f"[INFO] Seed bazy z CSV w {data_dir}...")
            seed_from_csvs(s, data_dir)
            count = s.query(Movie).count()
            print(f"[OK] Załadowano dane. Liczba filmów: {count}")


@app.get("/")
def read_root():
    return {"hello": "world"}
