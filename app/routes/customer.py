from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.config.db import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from app.crud.customer import customer_crud

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/getAll", response_model=List[CustomerOut])
async def get_customers(db: AsyncSession = Depends(get_db)):
    return await customer_crud.get_all(db)


@router.get("/getById={id}", response_model=CustomerOut)
async def get_customer(id: int, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.get_by_id(db, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/phone/{phone}", response_model=CustomerOut)
async def get_customer_by_phone(phone: str, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.get_by_phone(db, phone)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/post", response_model=CustomerOut)
async def create_customer(data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    return await customer_crud.create(db, data.dict())


@router.put("/update/id={id}", response_model=CustomerOut)
async def update_customer(id: int, data: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.update(db, id, data.dict())
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/delete/id={id}")
async def delete_customer(id: int, db: AsyncSession = Depends(get_db)):
    customer = await customer_crud.get_by_id(db, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    await customer_crud.delete(db, id)
    return {"message": "Customer deleted successfully"}


@router.get("?address={address}", response_model=List[CustomerOut])
async def get_customers_by_address(address: str, db: AsyncSession = Depends(get_db)):
    customers = await customer_crud.get_by_address(db, address)
    if not customers:
        raise HTTPException(
            status_code=404, detail="No customers found with this address")
    return customers
