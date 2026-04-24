# app/db/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://octagon:12345@localhost:5432/octagon_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Генератор сессий для внедрения зависимостей (например, в FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создаёт все таблицы, описанные в моделях (если их ещё нет)."""
    Base.metadata.create_all(bind=engine)