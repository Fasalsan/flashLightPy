from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True
