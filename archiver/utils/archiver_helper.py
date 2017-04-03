#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers.archive_provider import ArchiveProvider
from archiver.utils.archiver_utils import load_sources_by_category

ap = ArchiveProvider()


def fetch_report(page, limit, keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else ap.load_report_by_page(page, limit, keyword, sources)

async def as_fetch_report(page, limit, keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else await ap.as_load_report_by_page(page, limit, keywords, sources)


def fetch_report_count(keywords, category):
    sources = load_sources_by_category(category)
    return 0 if category and not sources else ap.count_report(keyword, sources)

async def as_fetch_report_count(keywords, category):
    sources = load_sources_by_category(category)
    return 0 if category and not sources else await ap.as_count_report(keywords, sources)


def fetch_report_daily_count(keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else ap.count_report_daily(keyword, sources)

async def as_fetch_report_daily_count(keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else await ap.as_count_report_daily(keywords, sources)


def fetch_report_weekly_count(keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else ap.count_report_weekly(keyword, sources)

async def as_fetch_report_weekly_count(keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else await ap.as_count_report_weekly(keywords, sources)


def fetch_report_daily(page, limit, keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else ap.load_report_daily(page, limit, keywords, sources)

async def as_fetch_report_daily(page, limit, keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else await ap.as_load_report_daily(page, limit, keywords, sources)


def fetch_report_weekly(page, limit, keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else ap.load_report_weekly(page, limit, keywords, sources)

async def as_fetch_report_weekly(page, limit, keywords, category):
    sources = load_sources_by_category(category)
    return [] if category and not sources else await ap.as_load_report_weekly(page, limit, keywords, sources)
