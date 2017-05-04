#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.models import Archive
from sqlalchemy import exc
from db.providers import BaseProvider
import arrow
import settings
from utils.data_utils import dict_blocker, data_hasher, time_localizer, data_updater, local_humanize
from db.utils.db_utils import sqlite_datetime_compatibility, list_as_str, str2list, id2hashid
from utils.async_utils import as_run


class ArchiveProvider(BaseProvider):

    def __init__(self, cls=None):
        if not cls:
            super().__init__(Archive)
        else:
            super().__init__(cls)
        self.tzinfo = settings.TIMEZONE
        self.search_columns = ["title", "summary"]
        self.order_by_columns = ["published"]

    def load(self, id, blockers=[]):
        item = super().load(id)
        item = dict_blocker(blockers, item)
        (item,) = time_localizer("published", item)
        return item

    async def as_load(self, id, blockers=[]):
        return await as_run()(self.load)(id, blockers)

    @sqlite_datetime_compatibility(['published'])
    @list_as_str(['founds'])
    def save_all(self, items):
        items = dict_blocker(["keyword", "updated"], items)
        return super().save_all(items)

    async def as_save_all(self, items):
        return await as_run()(self.save_all)(items)

    def count_report(self, keywords, sources=None):
        if sources:
            return self.count_items_by_values(sources, "source", keywords)
        else:
            return self.count(keywords)

    async def as_count_report(self, keywords, sources=None):
        return await as_run()(self.count_report)(keywords, sources)

    def count_report_daily(self, keywords, sources=None):
        start = arrow.now(self.tzinfo).shift(days=-1).replace(hour=8).floor('hour').datetime
        end = arrow.now(self.tzinfo).replace(hour=7).ceil('hour').datetime
        if sources:
            return self.count_items_by_values_and_datetime_between(sources, "source", "published", start, end, keywords)
        else:
            return self.count_by_datetime_between("published", start, end, keywords)

    async def as_count_report_daily(self, keywords, sources=None):
        return await as_run()(self.count_report_daily)(keywords, sources)

    def count_report_weekly(self, keywords, sources=None):
        start = arrow.now(self.tzinfo).floor('week').shift(
            weeks=-1, days=-1).replace(hour=8).datetime
        end = arrow.now(self.tzinfo).ceil('week').shift(weeks=-1).replace(hour=7).datetime
        if sources:
            return self.count_items_by_values_and_datetime_between(sources, "source", "published", start, end, keywords)
        else:
            return self.count_by_datetime_between("published", start, end, keywords)

    async def as_count_report_weekly(self, keywords, sources=None):
        return await as_run()(self.count_report_weekly)(keywords, sources)

    def load_report_by_sources(self, sources, limit=None, offset=None, keywords=None):
        items = self.find_items_by_values(sources, "source", limit, offset, keywords)
        items = time_localizer("published", items)
        items = data_updater("founds", "founds", str2list, True, items)
        items = data_updater("id", "id", id2hashid, True, items)
        return items

    async def as_load_report_by_sources(self, sources, limit=None, offset=None, keywords=None):
        return await as_run()(self.load_report_by_sources)(sources, limit, offset, keywords)

    def load_report_all(self, limit=None, offset=None, keyword=None):
        items = self.find_all(limit, offset, keyword)
        items = time_localizer("published", items)
        items = data_updater("founds", "founds", str2list, True, items)
        items = data_updater("id", "id", id2hashid, True, items)
        return items

    async def as_load_report_all(self, limit=None, offset=None, keywords=None):
        run = as_run()
        items = await run(self.load_report_all)(limit, offset, keywords)
        return items

    def load_report_daily(self, page=None, limit=None, keywords=None, sources=None):
        offset = (page - 1) * limit
        start = arrow.now(self.tzinfo).shift(days=-1).replace(hour=8).floor('hour').datetime
        end = arrow.now(self.tzinfo).replace(hour=7).ceil('hour').datetime
        if sources:
            items = self.find_items_by_values_and_datetime_between(
                sources, "source", "published", start, end, limit, offset, keywords)
        else:
            items = self.find_items_by_datetime_between(
                "published", start, end, limit, offset, keywords)
        items = data_updater("founds", "founds", str2list, True, items)
        items = data_updater("id", "id", id2hashid, True, items)
        items = data_updater("published_humanize", "published", local_humanize, True, items)
        return items

    async def as_load_report_daily(self, page=None, limit=None, keywords=None, sources=None):
        return await as_run()(self.load_report_daily)(page, limit, keywords, sources)

    def load_report_weekly(self, page=None, limit=None, keywords=None, sources=None):
        offset = (page - 1) * limit
        start = arrow.now(self.tzinfo).floor('week').shift(
            weeks=-1, days=-1).replace(hour=8).datetime
        end = arrow.now(self.tzinfo).ceil('week').shift(weeks=-1).replace(hour=7).datetime
        if sources:
            items = self.find_items_by_values_and_datetime_between(
                sources, "source", "published", start, end, limit, offset, keywords)
        else:
            items = self.find_items_by_datetime_between(
                "published", start, end, limit, offset, keywords)
        items = data_updater("founds", "founds", str2list, True, items)
        items = data_updater("id", "id", id2hashid, True, items)
        items = data_updater("published_humanize", "published", local_humanize, True, items)
        return items

    async def as_load_report_weekly(self, page=None, limit=None, keywords=None, sources=None):
        return await as_run()(self.load_report_weekly)(page, limit, keywords, sources)

    def load_report_by_page(self, page=1, limit=10, keywords=None, sources=None):
        offset = (page - 1) * limit
        if sources:
            items = self.load_report_by_sources(sources, limit, offset, keywords)
        else:
            items = self.load_report_all(limit, offset, keywords)

        items = data_updater("published_humanize", "published", local_humanize, True, items)
        return items

    async def as_load_report_by_page(self, page=1, limit=10, keywords=None, sources=None):
        offset = (page - 1) * limit
        if sources:
            items = await self.as_load_report_by_sources(sources, limit, offset, keywords)
        else:
            items = await self.as_load_report_all(limit, offset, keywords)
        items = data_updater("published_humanize", "published", local_humanize, True, items)
        return items

    def load_sources_by_category(self, category):
        import configparser
        config = configparser.ConfigParser()
        config.read('config/feeds.cfg')
        sources_pm, _ = zip(*config.items("Print media"))
        sources_em, _ = zip(*config.items("Electronic media"))
        sources_fn = lambda category: [category] if category in set(
            sources_pm) or category in set(sources_em) else None
        return {'pmedia': sources_pm, 'emedia': sources_em}.get(category, sources_fn(category))

    def update(self, item):
        (item,) = data_hasher("hash", ["title", "published", "source"], item)
        (item,) = dict_blocker(["_rawtime", "pass", "founds"], item)
        return super().update("hash", item)

    async def as_update(self, item):
        return await as_run()(self.update)(item)

    def remove(self, id):
        return super().remove(id)

    async def as_remove(self, id):
        return await as_run()(self.remove)(id)
