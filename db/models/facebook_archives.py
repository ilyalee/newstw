from sqlalchemy import (
    Column, String, Integer, DateTime, Text, func
)
from sqlalchemy.schema import Index
from db.models import Base


class FacebookArchive(Base):
    __tablename__ = 'facebook_archives'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hash = Column(String, nullable=False, unique=True)
    published = Column(DateTime(timezone=True), nullable=False)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fbid = Column(String, nullable=False)
    from_id = Column(String, nullable=False)
    from_name = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String, nullable=False)
    source = Column(String, nullable=False)
    founds = Column(String, nullable=True)

    def __repr__(self):
        return '<FacebookArchive(fbid="{}")>'.format(self.fbid)

    def show_detail(self):
        return '<FacebookArchive(published="{}", from_name="{}", message="{}", created="{}", link="{}")>'.format(self.published, self.from_name, self.message, self.created, self.link)

    def disp_hash(self):
        return '#{}'.format(self.hash)

Index('facebook_archives_index', FacebookArchive.published)
