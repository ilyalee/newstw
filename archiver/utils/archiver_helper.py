#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers.archive_provider import ArchiveProvider

ap = ArchiveProvider()

def fetch_report(page, limit):
    return ap.load_report_by_page(page, limit)

async def as_fetch_report(page, limit):
    return await ap.as_load_report_by_page(page, limit)
