from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.sale import Sale
from app.schemas.sale import SaleCreate


class SaleCRUD:
    async def create_sale(self, db: AsyncSession, sale_data: SaleCreate):
        new_sale = Sale(**sale_data.dict())
        db.add(new_sale)
        await db.commit()
        await db.refresh(new_sale)
        return new_sale

    async def get_sales(self, db: AsyncSession):
        result = await db.execute(select(Sale))
        return result.scalars().all()


sale_crud = SaleCRUD()
