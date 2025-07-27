from app.core.crud_base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate

category_crud = CRUDBase[Category, CategoryCreate](Category)
