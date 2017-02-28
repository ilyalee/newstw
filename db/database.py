import settings
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ref: https://github.com/seanpar203/sanic-starter
db_url = settings.DATABASE_TESTING_URL
if settings.TESTING:
    db_url = settings.DATABASE_TESTING_URL
    
engine = create_engine(db_url)

if settings.TESTING:
    from db.models import Base
    Base.metadata.create_all(engine)

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
