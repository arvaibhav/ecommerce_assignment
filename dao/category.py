from typing import List
from sqlalchemy import or_
from db.models.category import CategoryParentAssociation, Category
from db.orm import get_session


class CachedCategoryMapping:
    __mapping = None

    @classmethod
    def mapping(cls):
        if cls.__mapping is None:
            cls.update_cache()
        return cls.__mapping

    @classmethod
    def update_cache(cls):
        # later sync this with redis cache
        with get_session() as session:
            cached_mapping = {
                x.id: {
                    'name': x.name,
                    'subcategories': [],
                    'deep_subcategories': set(),
                } for x in list(session.query(Category).all())
            }
            for category in list(session.query(CategoryParentAssociation).all()):
                cached_mapping[category.parent_id]['subcategories'].append(category.category_id)

            def update_deep_subcategories(_category_id):
                _category = cached_mapping[_category_id]
                for subcategory_id in _category['subcategories']:
                    update_deep_subcategories(subcategory_id)
                    subcategory = cached_mapping[subcategory_id]
                    _category['deep_subcategories'].add(subcategory_id)
                    _category['deep_subcategories'].update(subcategory['deep_subcategories'])

            for category_id in cached_mapping.keys():
                update_deep_subcategories(category_id)

            cls.__mapping = cached_mapping

    @classmethod
    def generate_view(cls, category_id, depth=0):
        category = cls.mapping()[category_id]
        view = {
            "id": category_id,
            "name": category["name"],
            "subcategories": []
        }

        # let max depth level of 3 for subcategories
        if depth < 3:
            for subcategory_id in category["subcategories"]:
                subcategory_view = cls.generate_view(subcategory_id, depth + 1)
                view["subcategories"].append(subcategory_view)

        return view


def create_category(name: str, parent_ids: List[int] = None) -> dict:
    with get_session() as session:
        category = Category(name=name)
        session.add(category)
        session.flush()

        if parent_ids:
            for parent_id in parent_ids:
                association = CategoryParentAssociation(parent_id=parent_id, category_id=category.id)
                session.add(association)

        session.commit()

        CachedCategoryMapping.update_cache()  # later make this as background call
        return CachedCategoryMapping.generate_view(category.id)


def update_category(category_id: int, name: str, parent_ids) -> dict:
    with get_session() as session:
        category = session.query(Category).filter_by(id=category_id).first()
        category.name = name
        category.parents = session.query(Category).filter(
            or_(*[Category.id == category_id for category_id in parent_ids])).all()
        session.flush()
        CachedCategoryMapping.update_cache()  # later make this as background call

        return CachedCategoryMapping.generate_view(category.id)


def delete_category_by_id(category_id: int) -> None:
    with get_session() as session:
        category = session.query(Category).filter_by(id=category_id).first()
        session.delete(category)
        session.flush()
        CachedCategoryMapping.update_cache()  # later make this as background call


def get_category_by_id(category_id: int) -> dict:
    with get_session() as session:
        category = session.query(Category).filter_by(id=category_id).first()
        return CachedCategoryMapping.generate_view(category.id)


def get_categories_by_ids(category_ids: List[int]) -> List[dict]:
    with get_session() as session:
        categories = session.query(Category).filter_by(id=category_ids).all()
        return [
            CachedCategoryMapping.generate_view(category.id)
            for category in categories
        ]


def get_categories_by_filters(limit=100, offset=0):
    with get_session() as session:
        query = session.query(Category)
        count = query.count()
        categories = query.limit(limit).offset(offset).all()
        return [
            CachedCategoryMapping.generate_view(category.id)
            for category in categories
        ], count
