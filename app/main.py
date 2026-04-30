from fastapi import FastAPI
from app.db.db import create_tables
from app.api.routers import categories, books

app = FastAPI(title="Book Catalog API", description="Управление книгами и категориями")

# Создаём таблицы при старте (если их ещё нет)
@app.on_event("startup")
def on_startup():
    create_tables()

# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)

# Корневой эндпоинт (для проверки)
@app.get("/")
def read_root():
    return {"message": "Book Catalog API is running"}