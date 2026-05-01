from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.db import get_db
from app.db import crud
from app.api import schemas

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[schemas.CategoryInDB])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех категорий."""
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.CategoryInDB)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID."""
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

@router.post("/", response_model=schemas.CategoryInDB, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию."""
    # Можно добавить проверку на уникальность названия, но в задании не требуется
    return crud.create_category(db, title=category.title)

@router.put("/{category_id}", response_model=schemas.CategoryInDB)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Обновить название категории."""
    db_category = crud.update_category(db, category_id, title=category.title)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=schemas.CategoryInDB)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию."""
    db_category = crud.delete_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category