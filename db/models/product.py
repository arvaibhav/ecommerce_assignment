from sqlalchemy import Column, String, ForeignKey, Integer, UniqueConstraint, Index, Float
from sqlalchemy.orm import relationship
from db.models.base import AbstractBase


class Product(AbstractBase):
    name = Column(String, index=True, unique=True)
    price = Column(Float, name='price')
    categories = relationship("Category", secondary="product_category_association", viewonly=True)


class ProductCategoryAssociation(AbstractBase):
    product_id = Column(Integer, ForeignKey('product.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    __table_args__ = (
        Index('product_category_idx', 'product_id', 'category_id', unique=True),
    )
