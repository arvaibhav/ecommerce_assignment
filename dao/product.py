from typing import Optional, List

from sqlalchemy import or_, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import subqueryload

from db import Category
from db.models.product import Product, ProductCategoryAssociation
from db.orm import get_session
from pydantic import BaseModel
from dao.category import CachedCategoryMapping

def add_product_category_association(product_id: int, category_ids: List[int]) -> None:
    with get_session() as session:
        for category_id in category_ids:
            association = ProductCategoryAssociation(product_id=product_id, category_id=category_id)
            session.add(association)
            session.flush()


def remove_product_category_association(product_id: int, category_id: int) -> None:
    with get_session() as session:
        try:
            association = session.query(ProductCategoryAssociation).filter_by(
                product_id=product_id, category_id=category_id).first()
        except NoResultFound:
            return
        session.delete(association)
        session.flush()


def update_product(product_id: int, name: str, price: float, category_ids: List[int]) -> dict:
    with get_session() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        product.name = name
        product.price = price
        if category_ids is not None:
            product.categories = session.query(Category).filter(Category.id.in_(category_ids)).all()
        session.flush()
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category_ids": [category.id for category in product.categories]
        }


def delete_product_by_id(product_id: int) -> None:
    with get_session() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        session.delete(product)
        session.flush()


def get_product_by_id(product_id: int) -> dict:
    with get_session() as session:
        product = session.query(Product).options(subqueryload(Product.categories)).filter_by(
            id=product_id).one_or_none()
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category_ids": [category.id for category in product.categories]  # here I need only ids list
        }


class ProductFilters(BaseModel):
    name_search_text: str = None
    category_ids: List[int] = None


def get_product_by_filters(filters: ProductFilters, limit=10, offset=0) -> (List[dict], int):
    with get_session() as session:
        # SQLAlchemy query to filter products based on the given filters
        query = session.query(Product)
        if filters.name_search_text:
            query = query.filter(Product.name.like('%{}%'.format(filters.name_search_text)))
        if filters.category_ids:
            all_categories = set()
            for category_id in filters.category_ids:
                all_categories.add(category_id)
                all_categories.update(CachedCategoryMapping.mapping()[category_id]['deep_subcategories'])
            query = query.filter(Product.categories.any(Category.id.in_(list(all_categories))))

        count = query.count()
        products = query.limit(limit).offset(offset).all()

        product_list = [
            dict(
                id=product.id,
                name=product.name,
                price=product.price,
                category_ids=[category.id for category in product.categories]
            )
            for product in products
        ]

        return product_list, count


def create_product(name: str, price: float, category_ids: List[int] = None) -> dict:
    with get_session() as session:
        product = Product(name=name, price=price)
        session.add(product)
        session.flush()

        if category_ids:
            for category_id in category_ids:
                association = ProductCategoryAssociation(product_id=product.id, category_id=category_id)
                session.add(association)

        session.commit()
        return {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'category_ids': category_ids
        }
