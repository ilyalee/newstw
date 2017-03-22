#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc
from db.providers.base_provider import BaseProvider
import arrow
import settings
from utils.data_utils import dict_blocker, time_localizer, data_updater
from db.utils.db_utils import sqlite_datetime_compatibility, list_as_str, str2list
from utils.async_utils import as_run


class ArchiveProvider(BaseProvider):

    def __init__(self):
        super().__init__(Archive)
        self.tzinfo = settings.TIMEZONE
        self.search_columns = ["title", "summary"]

    def load(self, id, blockers=[]):
        item = super().load(id)
        item = dict_blocker(blockers, item)
        (item,) = time_localizer("published", item)
        return item

    async def as_load(self, id, blockers=[]):
        return await as_run(self.load, id, blockers)

    @sqlite_datetime_compatibility(['published'])
    @list_as_str(['founds'])
    def save_all(self, items):
        items = dict_blocker(["keyword", "updated"], items)
        return super().save_all(items)

    async def as_save_all(self, items):
        return await as_run(self.save_all, items)

    def load_report_by_sources(self, sources, limit=None, offset=None):
        items = self.find_items_by_values(sources, "source", limit, offset)
        items = time_localizer("published", items)
        items = data_updater("founds", "founds", str2list, True, items)
        return items

    async def as_load_report_by_sources(self, sources, limit=None, offset=None):
        return await as_run(self.load_report_by_sources, sources, limit, offset)

    def load_report_all(self, limit=None, offset=None, keyword=None):
        items = self.find_all("published", limit, offset, keyword)
        items = time_localizer("published", items)
        items = data_updater("founds", "founds", str2list, True, items)
        return items

    async def as_load_report_all(self, limit=None, offset=None, keyword=None):
        return await as_run(self.load_report_all, limit, offset, keyword)

    def load_report_today(self, limit=None, offset=None, keyword=None):
        start = arrow.now(self.tzinfo).floor('day').datetime
        end = arrow.now(self.tzinfo).ceil('day').datetime
        items = self.find_items_by_datetime_between("published", start, end, limit, offset, keyword)
        items = time_localizer("published", items)
        items = data_updater("founds", "founds", str2list, True, items)
        return items

    async def as_load_report_today(self, limit=None, offset=None, keyword=None):
        return await as_run(self.load_report_today, limit, offset, keyword)

    def load_report_by_page(self, page=1, limit=10, keyword=None):
        offset = (page - 1) * limit
        return self.load_report_all(limit, offset, keyword)

    async def as_load_report_by_page(self, page=1, limit=10, keyword=None):
        offset = (page - 1) * limit
        return await self.as_load_report_all(offset, limit, keyword)
