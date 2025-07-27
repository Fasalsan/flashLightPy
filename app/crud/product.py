from app.core.crud_base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate

product_crud = CRUDBase[Product, ProductCreate](Product)
