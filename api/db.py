# api/db.py
from __future__ import annotations

from pathlib import Path
import csv
from typing import Iterable, Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session as OrmSession

# === ŚCIEŻKI / ENGINE / SESSION ===

Base = declarative_base()

BASE_DIR: Path = Path(__file__).resolve().parent
DB_PATH: Path = BASE_DIR / "movies.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},  # FastAPI by default używa wielu wątków
    future=True,
)
# nazwa pozostaje "Session", żeby import w movies.py (DBSession) działał bez zmian
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


# === MODELE ORM ===

class Movie(Base):
    __tablename__ = "movies"
    movieId = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=False)
    # Relacje
    links = relationship("Link", back_populates="movie", uselist=False, cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="movie", cascade="all, delete-orphan")


class Link(Base):
    __tablename__ = "links"
    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(String)
    movie = relationship("Movie", back_populates="links")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, index=True, nullable=False)
    movieId = Column(Integer, ForeignKey("movies.movieId"), index=True, nullable=False)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)
    movie = relationship("Movie", back_populates="ratings")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, index=True, nullable=False)
    movieId = Column(Integer, ForeignKey("movies.movieId"), index=True, nullable=False)
    tag = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    movie = relationship("Movie", back_populates="tags")


# Utworzenie tabel (jeśli nie istnieją)
Base.metadata.create_all(engine)


# === FUNKCJE ŁADUJĄCE DANE Z CSV ===

def _open_csv(csv_path: Path) -> Iterable[dict]:
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def load_movies(session: OrmSession, csv_path: Path) -> None:
    for row in _open_csv(csv_path):
        session.add(
            Movie(
                movieId=int(row["movieId"]),
                title=row["title"],
                genres=row["genres"],
            )
        )
    session.commit()


def load_links(session: OrmSession, csv_path: Path) -> None:
    for row in _open_csv(csv_path):
        session.add(
            Link(
                movieId=int(row["movieId"]),
                imdbId=row.get("imdbId") or None,
                tmdbId=row.get("tmdbId") or None,
            )
        )
    session.commit()


def load_ratings(session: OrmSession, csv_path: Path) -> None:
    for row in _open_csv(csv_path):
        session.add(
            Rating(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                rating=float(row["rating"]),
                timestamp=int(row["timestamp"]),
            )
        )
    session.commit()


def load_tags(session: OrmSession, csv_path: Path) -> None:
    for row in _open_csv(csv_path):
        session.add(
            Tag(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                tag=row["tag"],
                timestamp=int(row["timestamp"]),
            )
        )
    session.commit()


# === SEED / NARZĘDZIA ===

def is_movies_table_empty(session: OrmSession) -> bool:
    # szybkie sprawdzenie — wystarczy pierwszy rekord
    return session.query(Movie.movieId).first() is None


def seed_from_csvs(session: OrmSession, data_dir: Path) -> None:
    """
    Ładuje dane z CSV w katalogu `data_dir` w kolejności:
    movies.csv -> links.csv -> ratings.csv -> tags.csv
    Zakłada standardowy format MovieLens.
    """
    load_movies(session, data_dir / "movies.csv")
    load_links(session, data_dir / "links.csv")
    load_ratings(session, data_dir / "ratings.csv")
    load_tags(session, data_dir / "tags.csv")


# === Tryb standalone (jednorazowe zasianie bazy) ===

if __name__ == "__main__":
    data_dir = BASE_DIR / "data"
    if not data_dir.exists():
        raise SystemExit(f"Brak katalogu z danymi: {data_dir}")

    with Session() as s:
        if is_movies_table_empty(s):
            seed_from_csvs(s, data_dir)
            print(f"[OK] Załadowano dane z {data_dir} do {DB_PATH}")
        else:
            print("[INFO] Tabela movies nie jest pusta — pomijam seed.")
