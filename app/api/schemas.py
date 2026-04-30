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
    model_config = {"from_attributes": True}

    id: int

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
    model_config = {"from_attributes": True}

    id: int
    category: Optional[CategoryInDB] = None