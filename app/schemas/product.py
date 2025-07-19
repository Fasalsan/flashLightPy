from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    image: Optional[str]

    class Config:
        orm_mode = True
