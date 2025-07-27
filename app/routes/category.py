from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.category import CategoryOut, CategoryCreate
from app.config.db import get_db
from app.crud.category import category_crud

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_all(db)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await category_crud.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryOut)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Optionally add check for duplicate category name here
    existing = await category_crud.get_by_field(db, "name", category_in.name)
    if existing:
        raise HTTPException(
            status_code=400, detail="Category name already exists")
    return await category_crud.create(db, category_in.dict())


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    updated = await category_crud.update(db, category_id, category_in.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await category_crud.delete(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}
