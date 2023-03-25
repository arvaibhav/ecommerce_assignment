from config import DB
from db.models.base import AbstractBase
from sqlalchemy import inspect
from sqlalchemy import create_engine


def create_table():
    classes = AbstractBase.__subclasses__()
    cls: AbstractBase
    for model_class in classes:
        engine = create_engine(DB)
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        if model_class.__tablename__ not in table_names:
            model_class.metadata.create_all(engine, checkfirst=True)
            print(f'Table {model_class.__tablename__} created in {DB}')
        else:
            print(f'Table {model_class.__tablename__} already exists in {DB}')

