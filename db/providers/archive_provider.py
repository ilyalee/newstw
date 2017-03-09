#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc
from db.providers.base_provider import BaseProvider
import arrow
import settings
import functools
import os
from utils.data_utils import dict_blocker, time_corrector
from db.utils.db_utils import sqlite_datetime_compatibility
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils.data_utils import dict_blocker

class ArchiveProvider(BaseProvider):

    def __init__(self):
        super().__init__(Archive)
        self.tzinfo = settings.TIMEZONE

    def load(self, id, blockers=[]):
        item = super().load(id)
        item = dict_blocker(blockers, item)
        (item,) = time_corrector("published", item)
        return item

    async def as_load(self, id, blockers=[]):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(os.cpu_count())
        future = loop.run_in_executor(executor, functools.partial(self.load, id, blockers))
        return await asyncio.ensure_future(future)

    @sqlite_datetime_compatibility(['published'])
    def save_all(self, items):
        items = dict_blocker(["keyword", "updated"], items)
        return super().save_all(items)

    async def as_save_all(self, items):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(os.cpu_count())
        future = loop.run_in_executor(executor, functools.partial(self.save_all, items))
        return await asyncio.ensure_future(future)

    def load_report_all(self, limit=None):
        items = self.find_all(orderby="published", limit=limit)
        items = time_corrector("published", items)
        return items

    async def as_load_report_all(self, limit=None):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(os.cpu_count())
        future = loop.run_in_executor(executor, functools.partial(self.load_report_all, limit))
        return await asyncio.ensure_future(future)

    def load_report_today(self):
        start = arrow.now(self.tzinfo).floor('day').datetime
        end = arrow.now(self.tzinfo).ceil('day').datetime
        items = self.find_items_by_datetime_between("published", start, end)
        items = time_corrector("published", items)
        return items

    async def as_load_report_today(self):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(os.cpu_count())
        future = loop.run_in_executor(executor, self.load_report_today)
        return await asyncio.ensure_future(future)
