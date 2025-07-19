from app.core.crud_base import CRUDBase
from app.models.product import Product

product_crud = CRUDBase[Product, dict](Product)
