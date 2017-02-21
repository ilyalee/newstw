#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from newsfeed.filter import NewsFeedFilter

def fetchFeed(url, includeText='', encoding='utf-8'):
    feed = NewsFeedFilter(url, includeText)

    return feed.output()
