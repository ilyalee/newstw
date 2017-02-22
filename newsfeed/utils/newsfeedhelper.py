#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from newsfeed.filter import NewsFeedFilter

def fetchFeed(url, includeText='', fulltext=False):
    feed = NewsFeedFilter(url, includeText, fulltext)
    return feed.output()
