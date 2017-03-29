import settings
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def pg_vacuum(db_url):
    if db_url.startswith('postgres://'):
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        connection = engine.raw_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute("VACUUM ANALYSE archive")
        connection.close()
        return True
    else:
        return False

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
        engine = create_engine(db_url, connect_args={
                               'check_same_thread': False})
    else:
        engine = create_engine(db_url)

if sqlite_memory_mode:
    from db.models import Base
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

try:
    if not pg_vacuum(db_url):
        pass
    else:
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
    session.close()
