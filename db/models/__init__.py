from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def to_dict(self):
    return {column.name: getattr(self, column.name, None) for column in self.__table__.columns}

Base.to_dict = to_dict

from db.models.archives import Archive
from db.models.facebook_archives import FacebookArchive
