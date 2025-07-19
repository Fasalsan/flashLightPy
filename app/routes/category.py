from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.config.db import get_db
from app.crud.category import category_crud

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/post", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await category_crud.create(db, category.dict())


@router.get("/getAll", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_all(db)


@router.get("/getById/id={id}", response_model=CategoryResponse)
async def get_category_by_id(id: int, db: AsyncSession = Depends(get_db)):
    category = await category_crud.get_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/name={name}", response_model=CategoryResponse)
async def get_category_by_name(name: str, db: AsyncSession = Depends(get_db)):
    category = await category_crud.get_by_field(db, "name", name)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/update/id={id}", response_model=CategoryResponse)
async def update_category(id: int, update_data: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    category = await category_crud.update(db, id, update_data.dict())
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/delete/id={id}")
async def delete_category(id: int, db: AsyncSession = Depends(get_db)):
    success = await category_crud.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
