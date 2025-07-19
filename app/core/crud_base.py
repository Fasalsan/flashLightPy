from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, TypeVar, Generic, List, Optional
from pydantic import BaseModel
from app.config.db import Base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        return await db.get(self.model, id)

    async def get_by_field(self, db: AsyncSession, field_name: str, value: str) -> Optional[ModelType]:
        stmt = select(self.model).where(
            getattr(self.model, field_name) == value)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj: dict) -> ModelType:
        db_obj = self.model(**obj)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, id: int, obj: dict) -> Optional[ModelType]:
        db_obj = await self.get_by_id(db, id)
        if not db_obj:
            return None
        for key, value in obj.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        db_obj = await self.get_by_id(db, id)
        if not db_obj:
            return False
        await db.delete(db_obj)
        await db.commit()
        return True

    async def get_by_field_many(self, db: AsyncSession, field_name: str, value: str):
        stmt = select(self.model).where(
            getattr(self.model, field_name) == value)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_field(self, db: AsyncSession, field_name: str, value: str):
        stmt = select(self.model).where(
            getattr(self.model, field_name) == value)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_many_by_field(self, db: AsyncSession, field_name: str, value: str) -> List[ModelType]:
        stmt = select(self.model).where(
            getattr(self.model, field_name) == value)
        result = await db.execute(stmt)
        return result.scalars().all()
