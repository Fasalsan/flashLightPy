from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import product, category, customer
import os
from app.config.db import engine, Base

app = FastAPI()

# Allow CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

# Include routes
# app.include_router(auth.router)
# app.include_router(private.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(customer.router)

# app.include_router(sale.router)

# Static file serving (optional)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
