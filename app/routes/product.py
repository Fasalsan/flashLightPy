import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.crud.product import product_crud
from app.crud.category import category_crud
from app.schemas.product import ProductOut

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=List[ProductOut])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_crud.get_all(db)


@router.get("/{id}", response_model=ProductOut)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await product_crud.get_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/by-category/{category_id}", response_model=List[ProductOut])
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await product_crud.get_by_field_many(db, "category_id", category_id)


@router.post("/", response_model=ProductOut)
async def create_product(
    name: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    category = await category_crud.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    image_path = None
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image type")
        image_path = os.path.join(
            UPLOAD_DIR, image.filename).replace("\\", "/")
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    product_data = {
        "name": name,
        "price": price,
        "category_id": category_id,
        "image": image_path
    }

    return await product_crud.create(db, product_data)


@router.put("/{id}", response_model=ProductOut)
async def update_product(
    id: int,
    name: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    product = await product_crud.get_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category = await category_crud.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    image_path = product.image
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image type")
        # Delete old image if exists
        if product.image and os.path.exists(product.image):
            os.remove(product.image)

        image_path = os.path.join(
            UPLOAD_DIR, image.filename).replace("\\", "/")
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    update_data = {
        "name": name,
        "price": price,
        "category_id": category_id,
        "image": image_path
    }

    return await product_crud.update(db, id, update_data)


@router.delete("/{id}")
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await product_crud.get_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete image file from disk
    if product.image and os.path.exists(product.image):
        os.remove(product.image)

    await product_crud.delete(db, id)
    return {"message": "Product deleted successfully"}
