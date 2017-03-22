import settings
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

creator = None
# ref: https://github.com/seanpar203/sanic-starter

if settings.TESTING:
    db_url = settings.DATABASE_TESTING_URL
else:
    db_url = settings.DATABASE_URL

sqlite_memory_mode = db_url.startswith('sqlite:///:memory:')
sqlite_mode = db_url.startswith('sqlite://')

if sqlite_memory_mode:
    import sqlite3
    creator = lambda: sqlite3.connect('file::memory:?cache=shared',
                                      uri=True, check_same_thread=False)

if creator:
    engine = create_engine('sqlite://', creator=creator)
else:
    if sqlite_mode:
        from sqlalchemy.pool import QueuePool
        engine = create_engine(db_url, poolclass=QueuePool)
    else:
        from sqlalchemy.pool import NullPool
        engine = create_engine(db_url, poolclass=NullPool)

if sqlite_mode:
    from db.models import Base
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

try:
    connection = engine.connect()
    connection.close()
except:
    import sys
    sys.exit("[Connection Error: make sure the database is running.]")


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
