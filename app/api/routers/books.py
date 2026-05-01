from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app.api import schemas

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.BookInDB])
def read_books(
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список книг, опционально отфильтрованный по категории."""
    books = crud.get_books(db, skip=skip, limit=limit, category_id=category_id)
    return books

@router.get("/{book_id}", response_model=schemas.BookInDB)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID."""
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book

@router.post("/", response_model=schemas.BookInDB, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создать книгу. Требуется существующая категория."""
    # Проверка бизнес-логики: категория должна существовать
    category = crud.get_category(db, category_id=book.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id {book.category_id} does not exist"
        )
    return crud.create_book(
        db,
        title=book.title,
        category_id=book.category_id,
        description=book.description,
        price=book.price,
        url=book.url
    )

@router.put("/{book_id}", response_model=schemas.BookInDB)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Обновить поля книги. Если передан category_id, проверяется существование категории."""
    # Проверяем, что книга существует
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Если в запросе передан category_id, проверяем его валидность
    if book.category_id is not None:
        category = crud.get_category(db, category_id=book.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {book.category_id} does not exist"
            )

    # Обновляем только те поля, которые были переданы
    updated_book = crud.update_book(db, book_id, **book.dict(exclude_unset=True))
    return updated_book

@router.delete("/{book_id}", response_model=schemas.BookInDB)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу."""
    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book