import settings
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ref: https://github.com/seanpar203/sanic-starter
engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)

@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@contextmanager
def query_session():
    session = Session()
    yield session
