
from app.core.crud_base import CRUDBase

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CRUDCustomer(CRUDBase[Customer, CustomerCreate]):
    async def get_by_phone(self, db, phone: str):
        return await self.get_by_field(db, "phone", phone)

    async def get_by_address(self, db, address: str):
        return await self.get_many_by_field(db, "address", address)


customer_crud = CRUDCustomer(Customer)
