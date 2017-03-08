import settings
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ref: https://github.com/seanpar203/sanic-starter
db_url = settings.DATABASE_URL

if settings.TESTING:
    db_url = settings.DATABASE_TESTING_URL

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)

try:
    connection = engine.connect()
    connection.close()
except:
    import sys
    sys.exit("[Connection Error: make sure the database is running.]")

if db_url.startswith('sqlite://'):
    from db.models import Base
    Base.metadata.create_all(engine)


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
