#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from newsfeed.utils.datautils import dictFilter, timeCorrector, dataCleaner, dataFilter, dataInsert

class NewsFeedFilter:
    def __init__(self, url, includeText=''):
        self.data = {}
        self.includeText = includeText
        self.rawdata = feedparser.parse(url)
        self._process()

    def _process(self):
        print(self.includeText)
        keys = ['title', 'published', 'link', 'summary', 'updated']
        items = self.rawdata['entries']
        items = dictFilter(keys, items)
        items = timeCorrector("published", items)
        items = dataCleaner("summary", items)
        items = dataFilter(self.includeText, ["summary", "title"], items)
        items = dataInsert(self.includeText, "keyword", items)
        self.data = items

    def output(self):
        return self.data
