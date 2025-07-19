from app.core.crud_base import CRUDBase
from app.models.category import Category

category_crud = CRUDBase[Category, dict](Category)
