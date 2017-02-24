from sqlalchemy import (
    Column, String, Integer, DateTime, Text
)

from db.models import Base
from arrow import Arrow

class Archive(Base):
    __tablename__ = 'archives'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hash = Column(String, nullable=False)
    published = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    link = Column(String, nullable=False)

    def __repr__(self):
        return '<Archive: {}>'.format(self.title)

    def disp(self):
        return '<{}> {}：「{}」'.format(self.published, self.link, self.summary)

    def disp_hash(self):
        return '#{}'.format(self.hash)
