from pydantic import BaseModel
from typing import Optional
from app.schemas.category import CategoryOut


class ProductBase(BaseModel):
    name: str
    price: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    image: Optional[str] = None
    category: CategoryOut  # ✅ Include full category object

    class Config:
        orm_mode = True
