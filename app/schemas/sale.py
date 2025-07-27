from datetime import datetime
from pydantic import BaseModel
from app.schemas.product import ProductBase
from app.schemas.customer import CustomerBase


class SaleCreate(BaseModel):
    product_id: int
    customer_id: int
    qty: int


class SaleOut(BaseModel):
    id: int
    qty: int
    created_at: datetime
    product: ProductBase
    customer: CustomerBase
    total_price: int

    class Config:
        orm_mode = True
