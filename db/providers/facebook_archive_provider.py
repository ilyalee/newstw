#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.models import FacebookArchive
from db.providers import ArchiveProvider
import arrow
from utils.data_utils import dict_blocker, time_localizer, data_updater, local_humanize
from db.utils.db_utils import sqlite_datetime_compatibility, list_as_str, str2list, id2hashid
from utils.async_utils import as_run


class FacebookArchiveProvider(ArchiveProvider):

    def __init__(self):
        super().__init__(FacebookArchive)
        self.search_columns = ["from_name", "message"]
        self.order_by_columns = ["published"]

    def load(self, id, blockers=[]):
        item = super().load(id)
        item = dict_blocker(blockers, item)
        (item,) = time_localizer("published", item)
        return item

    async def as_load(self, id, blockers=[]):
        return await as_run()(self.load)(id, blockers)

    @sqlite_datetime_compatibility(['published'])
    def save_all(self, items):
        items = dict_blocker(["keyword"], items)
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
        config.read('config/fbfeeds.cfg')
        sources, _ = zip(*config.items("Graph Objects"))
        sources_fn = lambda category: [category] if category in set(
            sources) else None
        return sources_fn(category)
