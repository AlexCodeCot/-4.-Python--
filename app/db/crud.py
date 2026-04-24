# app/db/crud.py
from sqlalchemy.orm import Session
from app.db import models

# ────────────────────────────── Категории ──────────────────────────────

def create_category(db: Session, title: str):
    """Создать новую категорию."""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    """Получить категорию по id."""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Получить список всех категорий с пагинацией."""
    return db.query(models.Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, title: str):
    """Обновить название категории."""
    db_category = get_category(db, category_id)
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    """Удалить категорию."""
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# ─────────────────────────────── Книги ─────────────────────────────────

def create_book(db: Session, title: str, category_id: int,
                description: str = "", price: float = 0.0, url: str = ""):
    """Добавить новую книгу."""
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    """Получить книгу по id."""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100,
              category_id: int = None):
    """Получить список книг, можно отфильтровать по категории."""
    query = db.query(models.Book)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, **kwargs):
    """Обновить поля книги (title, description, price, url, category_id)."""
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in kwargs.items():
            if hasattr(db_book, key):
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    """Удалить книгу."""
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book