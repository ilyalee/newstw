#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers.archive_provider import ArchiveProvider
from archiver.utils.archiver_utils import load_sources_by_category

ap = ArchiveProvider()


def fetch_report(page, limit, keyword):
    return ap.load_report_by_page(page, limit, keyword)

async def as_fetch_report(page, limit, keyword):
    return await ap.as_load_report_by_page(page, limit, keyword)


def fetch_category_report(page, limit, category):
    offset = (page - 1) * limit
    sources = load_sources_by_category(category)
    return ap.load_report_by_sources(sources, limit, offset)

async def as_fetch_category_report(page, limit, category):
    offset = (page - 1) * limit
    sources = load_sources_by_category(category)
    return await ap.as_load_report_by_sources(sources, limit, offset)
