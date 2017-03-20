#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers.archive_provider import ArchiveProvider

ap = ArchiveProvider()

def fetch_report(page, limit, keyword):
    return ap.load_report_by_page(page, limit, keyword)

async def as_fetch_report(page, limit, keyword):
    return await ap.as_load_report_by_page(page, limit, keyword)
