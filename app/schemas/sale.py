from pydantic import BaseModel
from datetime import datetime


class ProductShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CustomerShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SaleOut(BaseModel):
    id: int
    qty: int
    created_at: datetime
    product: ProductShort
    customer: CustomerShort

    class Config:
        orm_mode = True
