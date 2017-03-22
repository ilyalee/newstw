#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers.archive_provider import ArchiveProvider
from archiver.utils.archiver_utils import load_sources_by_category

ap = ArchiveProvider()


def fetch_report(page, limit, keywords, category):
    sources = None
    if category:
        sources = load_sources_by_category(category)
    return ap.load_report_by_page(page, limit, keyword, sources)

async def as_fetch_report(page, limit, keywords, category):
    sources = None
    if category:
        sources = load_sources_by_category(category)
    return await ap.as_load_report_by_page(page, limit, keywords, sources)
