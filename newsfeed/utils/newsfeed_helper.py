#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from newsfeed.filter import NewsFeedFilter

def fetch_feed(url, include_text='', full_text=False):
    feed = NewsFeedFilter(url, include_text, full_text)
    return feed.output()

def flag(t):
    return str(t).lower() in ("yes", "true", "t", "1")
