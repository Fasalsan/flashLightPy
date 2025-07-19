from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.sale import Sale


class SaleCRUD:
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Sale).order_by(Sale.id.desc()))
        return result.scalars().all()

    async def create(self, db: AsyncSession, sale_data: dict):
        new_sale = Sale(**sale_data)
        db.add(new_sale)
        await db.commit()
        await db.refresh(new_sale)
        return new_sale


sale_crud = SaleCRUD()
