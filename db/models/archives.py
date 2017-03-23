from sqlalchemy import (
    Column, String, Integer, DateTime, Text, func
)
from sqlalchemy.schema import Index
from db.models import Base


class Archive(Base):
    __tablename__ = 'archives'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hash = Column(String, nullable=False, unique=True)
    published = Column(DateTime(timezone=True), nullable=False)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    link = Column(String, nullable=False)
    source = Column(String, nullable=False)
    founds = Column(String, nullable=True)

    def __repr__(self):
        return '<Archive(title="{}")>'.format(self.title)

    def show_detail(self):
        return '<Archive(published="{}", link="{}", summary="{}", created="{}")>'.format(self.published, self.link, self.summary, self.created)

    def disp_hash(self):
        return '#{}'.format(self.hash)

Index('archives_index', Archive.published)
