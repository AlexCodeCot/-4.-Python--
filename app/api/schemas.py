from pydantic import BaseModel
from typing import Optional

# ---------- Category ----------
class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True  # для Pydantic v1; в v2 используйте model_config

# ---------- Book ----------
class BookBase(BaseModel):
    title: str
    description: Optional[str] = ""
    price: float = 0.0
    url: Optional[str] = ""
    category_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None

class BookInDB(BookBase):
    id: int
    category: Optional[CategoryInDB] = None  # для загрузки связанного объекта

    class Config:
        orm_mode = True