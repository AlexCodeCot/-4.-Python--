# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.db import create_tables
from app.api.routers import categories, books

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при старте
    create_tables()
    print("База данных готова к работе")
    yield
    # Код, выполняемый при завершении (можно добавить при необходимости)
    print("Приложение остановлено")

app = FastAPI(
    title="Book Catalog API",
    description="Управление книгами и категориями",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Book Catalog API is running"}