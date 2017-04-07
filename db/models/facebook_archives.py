from sqlalchemy import (
    Column, String, Integer, DateTime, Text, func
)
from sqlalchemy.schema import Index
from db.models import Base


class FacebookArchive(Base):
    __tablename__ = 'facebook_archives'

    id = Column(Integer, autoincrement=True, primary_key=True)
    hash = Column(String, nullable=False, unique=True)
    created_time = Column(DateTime(timezone=True), nullable=False)
    updated_time = Column(DateTime(timezone=True), nullable=False)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fbid = Column(String, nullable=False)
    from_id = Column(String, nullable=False)
    from_name = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    permalink_url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    founds = Column(String, nullable=True)

    def __repr__(self):
        return '<FacebookArchive(fbid="{}")>'.format(self.fbid)

    def show_detail(self):
        return '<FacebookArchive(updated_time="{}", from_name="{}", message="{}", created="{}", permalink_url="{}")>'.format(self.updated_time, self.from_name, self.message, self.created, self.permalink_url)

    def disp_hash(self):
        return '#{}'.format(self.hash)

Index('facebook_archives_index', FacebookArchive.updated_time)
