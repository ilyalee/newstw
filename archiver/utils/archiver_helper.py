#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers import ArchiveProvider, FacebookArchiveProvider


class ArchiverHelper():

    def __init__(self, ap):
        self.ap = ap

    def fetch_report(self, page, limit, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.load_report_by_page(page, limit, keyword, sources)

    async def as_fetch_report(self, page, limit, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_load_report_by_page(page, limit, keywords, sources)

    def fetch_report_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return 0 if category and not sources else self.ap.count_report(keyword, sources)

    async def as_fetch_report_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return 0 if category and not sources else await self.ap.as_count_report(keywords, sources)

    def fetch_report_daily_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.count_report_daily(keyword, sources)

    async def as_fetch_report_daily_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_count_report_daily(keywords, sources)

    def fetch_report_today_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.count_report_today(keyword, sources)

    async def as_fetch_report_today_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_count_report_today(keywords, sources)

    def fetch_report_yesterday_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.count_report_yesterday(keyword, sources)

    async def as_fetch_report_yesterday_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_count_report_yesterday(keywords, sources)

    def fetch_report_weekly_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.count_report_weekly(keyword, sources)

    async def as_fetch_report_weekly_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_count_report_weekly(keywords, sources)

    def fetch_report_month_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.count_report_month(keyword, sources)

    async def as_fetch_report_month_count(self, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_count_report_month(keywords, sources)

    def fetch_report_daily(self, page, limit, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.load_report_daily(page, limit, keywords, sources)

    async def as_fetch_report_daily(self, page, limit, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_load_report_daily(page, limit, keywords, sources)

    def fetch_report_weekly(self, page, limit, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else self.ap.load_report_weekly(page, limit, keywords, sources)

    async def as_fetch_report_weekly(self, page, limit, keywords, category=None):
        sources = self.ap.load_sources_by_category(category)
        return [] if category and not sources else await self.ap.as_load_report_weekly(page, limit, keywords, sources)


aph = ArchiverHelper(ArchiveProvider())
fb_aph = ArchiverHelper(FacebookArchiveProvider())
