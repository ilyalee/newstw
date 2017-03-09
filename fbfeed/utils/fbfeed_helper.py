#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from fbfeed.filter import FbFeedFilter


def fetch_feed(url, pages, include_text='', search=False):
    return FbFeedFilter(url, pages, include_text, search).output()


async def as_fetch_feed(url, pages, include_text='', search=False):
    return await FbFeedFilter(url, pages, include_text, search).as_output()


def flag(t):
    return str(t).lower() in ("yes", "true", "t", "1")
