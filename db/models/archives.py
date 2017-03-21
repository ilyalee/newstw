from sqlalchemy import (
    Column, String, BigInteger, DateTime, Text
)
from sqlalchemy.schema import Index
from db.models import Base


class Archive(Base):
    __tablename__ = 'archives'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    hash = Column(String, nullable=False, unique=True)
    published = Column(DateTime(timezone=True), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    link = Column(String, nullable=False)
    source = Column(String, nullable=False)

    def __repr__(self):
        return '<Archive(title="{}")>'.format(self.title)

    def show_detail(self):
        return '<Archive(published="{}", link="{}", summary="{}")>'.format(self.published, self.link, self.summary)

    def disp_hash(self):
        return '#{}'.format(self.hash)

Index('archives_index', Archive.published)
