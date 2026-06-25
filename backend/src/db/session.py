"""SQLite session + engine setup."""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .schema import Base


DEFAULT_DB_PATH = Path(__file__).resolve().parents[3] / "backend" / "data" / "eidolon.db"
DB_PATH = Path(os.getenv("DB_PATH", str(DEFAULT_DB_PATH)))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables if not exist."""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return SessionLocal()
