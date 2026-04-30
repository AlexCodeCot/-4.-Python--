from fastapi import APIRouter, Depends, HTTPException, Query
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
    books = crud.get_books(db, skip=skip, limit=limit, category_id=category_id)
    return books

@router.get("/{book_id}", response_model=schemas.BookInDB)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/", response_model=schemas.BookInDB, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Проверим, существует ли категория
    category = crud.get_category(db, category_id=book.category_id)
    if category is None:
        raise HTTPException(status_code=400, detail="Category does not exist")
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
    db_book = crud.update_book(db, book_id, **book.dict(exclude_unset=True))
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}", response_model=schemas.BookInDB)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book