from typing import List
from http_schema.base import Base
from pydantic import validator


class ProductPostSchema(Base):
    name: str
    category_ids: List[int]
    price: int

    @validator('price')
    def validate_price(cls, price):
        if price < 0:
            raise ValueError(f'price must be > 0')
        return price


class ProductPutSchema(ProductPostSchema):
    id: int
