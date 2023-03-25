from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AbstractBase(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        # let class name itself is default table name
        return ''.join(
            ['_' + i.lower() if i.isupper() else i for i in cls.__name__]
        ).lstrip('_')
