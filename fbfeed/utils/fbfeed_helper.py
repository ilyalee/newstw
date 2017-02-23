#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from fbfeed.filter import FbFeedFilter


def fetch_feed(url, pages, include_text='', search=False):
    feed = FbFeedFilter(url, pages, include_text, search)
    return feed.output()


def flag(t):
    return str(t).lower() in ("yes", "true", "t", "1")
