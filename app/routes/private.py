from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routes.auth import get_current_user
from app.config.db import get_db
from app.schemas.user import UserOut

router = APIRouter(prefix="/private", tags=["Private"])


@router.get("/", response_model=UserOut)
async def private_route(current_user=Depends(get_current_user)):
    return current_user
