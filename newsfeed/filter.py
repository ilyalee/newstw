#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import requests
from newsfeed.utils.datautils import dictFilter, timeCorrector, linkCorrector, dataCleaner, dataFilter, dataInserter, dataUpdaterAll
from crawler.utils.crawlerhelper import fetchNewsAll

class NewsFeedFilter:
    def __init__(self, url, includeText='', fullTextMode=False):
        self.url = url
        self.fullTextMode = fullTextMode
        self.includeText = includeText

    def _download(self, encoding='utf-8'):
        r = requests.get(self.url)
        r.encoding = encoding

        items = {}
        rawdata = feedparser.parse(r.text)
        items = rawdata['entries']
        items = self._data_prepare(items)
        return items

    def _data_prepare(self, items):
        items = dataUpdaterAll("summary", "link", fetchNewsAll, self.fullTextMode, items)
        items = dataInserter(self.fullTextMode, "fulltext", items)
        return self._data_filter(items)

    def _data_filter(self, items):
        keys = ['title', 'published', 'link', 'summary', 'updated', 'fulltext']
        items = dictFilter(keys, items)
        items = timeCorrector("published", items)
        items = timeCorrector("updated", items)
        items = linkCorrector("link", items)
        items = dataCleaner("summary", items)
        items = dataFilter(self.includeText, ["summary", "title"], items)
        items = dataInserter(self.includeText, "keyword", items)
        return items

    def output(self):
        return self._download()
