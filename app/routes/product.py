from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import get_db
from app.crud.product import product_crud
from app.schemas.product import ProductOut
import os
import shutil

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=ProductOut)
async def create_product(
    name: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_filename = None
    if image:
        image_filename = image.filename
        file_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    product_data = {
        "name": name,
        "price": price,
        "category_id": category_id,
        "image": image_filename,
    }

    product = await product_crud.create(db, product_data)
    return product


@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await product_crud.get_all(db)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_crud.get_by_id(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.get("/by-name/{name}", response_model=ProductOut)
async def get_product_by_name(name: str, db: AsyncSession = Depends(get_db)):
    product = await product_crud.get_by_name(db, name)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    name: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    product = await product_crud.get_by_id(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    image_filename = product.image
    if image:
        image_filename = image.filename
        file_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    update_data = {
        "name": name,
        "price": price,
        "category_id": category_id,
        "image": image_filename,
    }

    updated_product = await product_crud.update(db, product_id, update_data)
    return updated_product


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await product_crud.delete(db, product_id)
    if not deleted:
        raise HTTPException(404, "Product not found")
    return {"detail": "Product deleted successfully"}

# Optional: Add specific function for clarity
