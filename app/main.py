from fastapi import FastAPI
from sqlalchemy import text                             # <-- добавить импорт
from app.db.db import engine, SessionLocal, create_tables
from app.api.routers import categories, books

app = FastAPI(title="Book Catalog API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    """При старте приложения проверяем/создаём таблицы в БД."""
    create_tables()

@app.get("/health")
def health_check():
    """Эндпоинт для проверки работоспособности сервиса и подключения к БД."""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))                    # <-- исправлено
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Подключаем роутеры книг и категорий
app.include_router(categories.router)
app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Welcome to Book Catalog API"}