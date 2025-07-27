# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List
# from app.config.db import get_db
# from app.schemas.sale import SaleCreate, SaleOut
# from app.crud.sale import sale_crud

# router = APIRouter(prefix="/sales", tags=["Sales"])


# @router.post("/", response_model=SaleOut)
# async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_db)):
#     new_sale = await sale_crud.create_sale(db, sale)

#     if not new_sale.product or not new_sale.customer:
#         raise HTTPException(
#             status_code=404, detail="Product or Customer not found")

#     return SaleOut(
#         id=new_sale.id,
#         qty=new_sale.qty,
#         created_at=new_sale.created_at,
#         product=new_sale.product,
#         customer=new_sale.customer,
#         total_price=new_sale.product.price * new_sale.qty,
#     )


# @router.get("/", response_model=List[SaleOut])
# async def list_sales(db: AsyncSession = Depends(get_db)):
#     sales = await sale_crud.get_sales(db)
#     return [
#         SaleOut(
#             id=s.id,
#             qty=s.qty,
#             created_at=s.created_at,
#             product=s.product,
#             customer=s.customer,
#             total_price=s.product.price * s.qty,
#         )
#         for s in sales
#     ]
