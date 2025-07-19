from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.config.db import get_db
from app.schemas.sale import SaleOut
from app.crud.sale import sale_crud
from app.crud.product import product_crud
from app.crud.customer import customer_crud

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=List[SaleOut])
async def get_sales(db: AsyncSession = Depends(get_db)):
    sales = await sale_crud.get_all(db)
    return sales


@router.post("/", response_model=SaleOut)
async def create_sale(
    product_id: int = Form(...),
    customer_id: int = Form(...),
    qty: int = Form(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    product = await product_crud.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product_id")

    customer = await customer_crud.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Invalid customer_id")

    sale_data = {
        "product_id": product_id,
        "customer_id": customer_id,
        "qty": qty,
    }
    sale = await sale_crud.create(db, sale_data)
    return sale
