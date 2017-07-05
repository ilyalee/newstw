from sqlalchemy import (
    Column, Integer, DateTime, func
)
from sqlalchemy.schema import Index
from db.models import Base


class ObserverStat(Base):
    __tablename__ = 'observer_stats'

    id = Column(Integer, autoincrement=True, primary_key=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    count = Column(Integer, nullable=False, default=0)
    total = Column(Integer, nullable=False, default=0)
    acceptances = Column(Integer, nullable=False, default=0)
    rejects = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return '<ObserverStat(count="{}", acceptances="{}")>'.format(self.count, self.acceptances)

Index('observer_stats_index', ObserverStat.created)
