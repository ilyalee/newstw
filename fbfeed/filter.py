#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeedutils import FBInit, loadGroup, loadPages
from fbfeed.utils.datautils import FBTimeToLocal, dataFilter

class FBFeedFilter:
    def __init__(self, fbid, num, includeText='', search=False):
        self.fbid = fbid
        self.num = int(num)
        self.includeText = includeText
        self.graph = FBInit()
        self.tzinfo = "Asia/Taipei"
        self.search = search

    def _download(self, encoding='utf-8'):
        items = []
        group = loadGroup(self.graph, self.fbid, search=self.search)
        if group:
            items = loadPages(self.graph, self.fbid, "feed", self.num, search=self.search, date_format="U")
        return self._data_prepare(items)

    def _data_prepare(self, items):
        items = FBTimeToLocal("created_time", self.tzinfo, items)
        items = FBTimeToLocal("updated_time", self.tzinfo, items)
        return self._data_filter(items)

    def _data_filter(self, items):
        items = dataFilter(self.includeText, ["message", "story"], items)
        return items

    def output(self):
        return self._download()
