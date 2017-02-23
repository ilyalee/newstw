#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from fbfeed.filter import FBFeedFilter

def fetchFeed(url, pages, includeText='', search=False):
    feed = FBFeedFilter(url, pages, includeText, search)
    return feed.output()

def flag(t):
    return str(t).lower() in ("yes", "true", "t", "1")
