#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.models import ObserverStat
from sqlalchemy import exc
from db.providers import BaseProvider
import arrow
import settings
from utils.data_utils import dict_filter
from utils.async_utils import as_run


class ObserverStatProvider(BaseProvider):

    def __init__(self, cls=None):
        if not cls:
            super().__init__(ObserverStat)
        else:
            super().__init__(cls)
        self.tzinfo = settings.TIMEZONE
        self.order_by_columns = ["created"]

    def save(self, item):
        items = dict_filter(['count', 'total', 'acceptances', 'rejects'], item)
        return super().save(items)

    async def as_save(self, item):
        return await as_run()(self.save)(item)

    def sum(self):
        return super().sum("count")

    async def as_sum(self):
        return await as_run()(self.sum)()

    def sum_observer_today(self):
        start = arrow.now(self.tzinfo).floor('day').datetime
        end = arrow.now(self.tzinfo).ceil('day').datetime
        return self.sum_by_datetime_between("count", "created", start, end)

    async def as_sum_observer_today(self):
        return await as_run()(self.sum_observer_today)()

    def sum_observer_yesterday(self):
        start = arrow.now(self.tzinfo).shift(days=-1).floor('day').datetime
        end = arrow.now(self.tzinfo).shift(days=-1).ceil('day').datetime
        return self.sum_by_datetime_between("count", "created", start, end)

    async def as_sum_observer_yesterday(self):
        return await as_run()(self.sum_observer_yesterday)()

    def sum_observer_month(self):
        start = arrow.now(self.tzinfo).floor('month').datetime
        end = arrow.now(self.tzinfo).ceil('month').datetime
        return self.sum_by_datetime_between("count", "created", start, end)

    async def as_sum_observer_month(self):
        return await as_run()(self.sum_observer_month)()

    def load_observer_all(self, limit=None, offset=None):
        return list(self.find_all(limit, offset))

    async def as_load_observer_all(self, limit=None, offset=None):
        return await as_run()(self.load_observer_all)(limit, offset)

    def load_observer_by_page(self, page=1, limit=10):
        offset = (page - 1) * limit
        return self.load_observer_all(limit, offset)

    async def as_load_observer_by_page(self, page=1, limit=10, keywords=None, sources=None):
        offset = (page - 1) * limit
        return await self.as_load_observer_all(limit, offset)
