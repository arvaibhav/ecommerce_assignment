from typing import List
from http_schema.base import Base


class CategoryPostSchema(Base):
    name: str
    parent_ids: List[int]


class CategoryPutSchema(CategoryPostSchema):
    id: int
