from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.config.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    products = relationship("Product", back_populates="category")
