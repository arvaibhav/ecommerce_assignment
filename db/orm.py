from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DB

engine = create_engine(DB)
session_factory = sessionmaker(bind=engine)
readonly_session = session_factory(autoflush=False)


@contextmanager
def get_session() -> Session:
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
