from sqlalchemy import Column, String, ForeignKey, Integer, Index
from sqlalchemy.orm import relationship
from db.models.base import AbstractBase


# products = relationship("Product", secondary="product_category_association", viewonly=True)


class Category(AbstractBase):
    name = Column(String, index=True, unique=True)

    # Define relationship with parent categories
    parents = relationship(
        "Category",
        secondary="category_parent_association",
        primaryjoin="CategoryParentAssociation.category_id==Category.id",
        secondaryjoin="CategoryParentAssociation.parent_id==Category.id",
        viewonly=True
    )

    # Define relationship with child subcategories
    subcategories = relationship(
        "Category",
        secondary="category_parent_association",
        primaryjoin="CategoryParentAssociation.parent_id==Category.id",
        secondaryjoin="CategoryParentAssociation.category_id==Category.id",
        viewonly=True
    )


class CategoryParentAssociation(AbstractBase):
    parent_id = Column(Integer, ForeignKey('category.id') )
    category_id = Column(Integer, ForeignKey('category.id') )

    __table_args__ = (
        Index('parent_child_idx', 'parent_id', 'category_id', unique=True),
    )
